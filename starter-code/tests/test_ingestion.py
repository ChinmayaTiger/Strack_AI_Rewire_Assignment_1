"""Tests for src/ingest.py (Task 1-2, Batch 1 baseline)."""
from pathlib import Path
from src.config import BATCH_1_FILES, ENTITIES
from src.ingest import ingest_entity
from src.idempotent_writer import write_bronze


def test_batch_1_loads_all_five_entities(spark, tmp_path):
    """Run Batch 1 across all five entities and assert expected row counts:
    customers=80, products=10, stores=15, sales_transactions=360, returns=46.
    """
    expected_counts = {
        "customers": 80,
        "products": 10,
        "stores": 15,
        "sales_transactions": 360,
        "returns": 46,
    }

    for entity, file_path in BATCH_1_FILES.items():
        assert Path(file_path).exists(), f"File for {entity} not found at {file_path}"

        df = ingest_entity(spark, entity, str(file_path), "batch_1")
        entity_bronze_path = str(tmp_path / entity)
        write_bronze(df, entity_bronze_path)

        written_df = spark.read.parquet(entity_bronze_path)
        actual_count = written_df.count()
        assert actual_count == expected_counts[entity], (
            f"Entity {entity} count mismatch: got {actual_count}, expected {expected_counts[entity]}"
        )