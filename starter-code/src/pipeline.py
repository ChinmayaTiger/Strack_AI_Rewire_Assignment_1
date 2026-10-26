"""Main orchestration entry point.

Scaffolding only - wires the modules above together and runs one or more
batches end to end. Fill in as you complete each task; this is meant to be
runnable incrementally (e.g. Task 1+2 first, then add Task 3, etc.), not
all at once.

Suggested usage once implemented:
    python -m src.pipeline --batch batch_1
    python -m src.pipeline --batch batch_1   # re-run: idempotency check
    python -m src.pipeline --batch batch_3   # schema drift: loyalty_tier
    python -m src.pipeline --batch batch_4   # your modified schema-drift skill
    python -m src.pipeline --batch batch_5   # your new data-quality skill
"""
import argparse

from .config import BATCHES
from .spark_session import get_spark

# TODO: import ingest_entity, add_ingestion_metadata, schema_utils functions,
# idempotent_writer functions, and (for Task 7) data_quality.validate_data_quality
# once each is implemented.


def run_batch(spark, batch_id: str) -> None:
    """Run a single batch end to end across all its entities.

    TODO: implement using the BATCHES definitions in config.py:
      1. For each entity in this batch: ingest_entity(...)
      2. schema_utils: compare against last known bronze schema, reconcile
      3. (Batch 5 onward) data_quality.validate_data_quality(...)
      4. idempotent_writer: dedup_against_existing + write_bronze
      5. audit.write_audit_record(...) with the counts from steps 1-4
    Print a short summary (rows read/written/duplicates skipped/quarantined)
    so a human can see the outcome without opening the audit log.
    """
    raise NotImplementedError(f"run_batch: implement for batch_id={batch_id!r}")


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
