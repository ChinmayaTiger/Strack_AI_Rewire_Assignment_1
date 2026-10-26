"""Main orchestration entry point.

Runs one or more batches end to end:
1. Ingest entity CSV and enrich with metadata.
2. Compare schema against existing Bronze table and detect drift.
3. Validate data quality and route invalid records to quarantine.
4. Deduplicate valid records against existing Bronze table via business key.
5. Append new records to Bronze with schema merging.
6. Record audit metrics to JSONL log and display summary.
"""
import argparse
from pathlib import Path
from pyspark.sql import SparkSession

from .config import BATCHES, BRONZE_DIR, QUARANTINE_DIR, ENTITIES
from .spark_session import get_spark
from .ingest import ingest_entity
from .schema_utils import compare_schemas, reconcile_schema, log_drift_event
from .data_quality import validate_data_quality
from .idempotent_writer import read_existing_keys, dedup_against_existing, write_bronze
from .audit import write_audit_record


def run_batch(spark: SparkSession, batch_id: str) -> None:
    """Run a single batch end to end across all configured entities."""
    if batch_id not in BATCHES:
        raise ValueError(f"Unknown batch_id: {batch_id}. Available batches: {list(BATCHES.keys())}")

    batch_manifest = BATCHES[batch_id]
    print(f"\n==========================================")
    print(f" Starting Ingestion Pipeline: {batch_id}")
    print(f"==========================================")

    for entity, file_path in batch_manifest.items():
        resolved_path = Path(file_path).resolve()
        if not resolved_path.exists():
            print(f"[WARN] File not found for entity '{entity}': {resolved_path}. Skipping.")
            continue

        business_key = ENTITIES.get(entity)
        if not business_key:
            raise ValueError(f"No business key configured for entity: '{entity}'")

        bronze_entity_path = str((BRONZE_DIR / entity).resolve())
        quarantine_entity_path = str((QUARANTINE_DIR / entity).resolve())

        # 1. Ingest entity CSV and tag metadata
        incoming_df = ingest_entity(spark, entity, str(resolved_path), batch_id)
        rows_read = incoming_df.count()

        # 2. Schema drift check against existing bronze
        drift_events = []
        existing_bronze_dir = Path(bronze_entity_path)
        has_existing_data = existing_bronze_dir.exists() and (
            any(existing_bronze_dir.glob("*.parquet")) or any(existing_bronze_dir.glob("**/*.parquet"))
        )

        if has_existing_data:
            existing_bronze_df = spark.read.option("mergeSchema", "true").parquet(bronze_entity_path)
            diff = compare_schemas(existing_bronze_df.schema, incoming_df.schema)
            if diff.get("added_columns") or diff.get("type_changes"):
                drift_event = log_drift_event(entity, batch_id, diff)
                drift_events.append(drift_event)
                print(f"  [DRIFT DETECTED] Entity '{entity}' added columns: {diff.get('added_columns')}")
            incoming_df = reconcile_schema(incoming_df, existing_bronze_df.schema)

        # 3. Data Quality validation and quarantine routing
        valid_df, quarantined_df = validate_data_quality(incoming_df, business_key)
        quarantined_count = quarantined_df.count()

        if quarantined_count > 0:
            (
                quarantined_df.write
                .mode("append")
                .option("mergeSchema", "true")
                .format("parquet")
                .save(quarantine_entity_path)
            )
            print(f"  [QUARANTINED] {quarantined_count} records sent to {quarantine_entity_path}")

        # 4. Deduplicate against existing Bronze business keys
        existing_keys = read_existing_keys(spark, bronze_entity_path, business_key)
        deduped_df = dedup_against_existing(valid_df, existing_keys, business_key)

        valid_count = valid_df.count()
        rows_to_write = deduped_df.count()
        duplicates_skipped = valid_count - rows_to_write

        # 5. Write to Bronze
        write_bronze(deduped_df, bronze_entity_path)

        # 6. Append audit record
        write_audit_record(
            batch_id=batch_id,
            entity=entity,
            source_file=resolved_path.name,
            rows_read=rows_read,
            rows_written=rows_to_write,
            duplicates_skipped=duplicates_skipped,
            drift_events=drift_events,
            quarantined=quarantined_count,
        )

        # Console Summary
        print(
            f"  Entity: {entity:<10} | Read: {rows_read:<4} | Written: {rows_to_write:<4} | "
            f"Dupes Skipped: {duplicates_skipped:<4} | Quarantined: {quarantined_count:<4}"
        )

    print(f"==========================================\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one bronze ingestion batch.")
    parser.add_argument("--batch", required=True, help="batch_id to run, e.g. batch_1")
    args = parser.parse_args()

    spark = get_spark()
    try:
        run_batch(spark, args.batch)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()