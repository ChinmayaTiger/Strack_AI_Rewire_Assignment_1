"""Configuration constants and path definitions for the Bronze layer ingestion pipeline."""
from pathlib import Path

# Base repository directories
STARTER_CODE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = STARTER_CODE_DIR.parent
DATA_DIR = REPO_ROOT / "data"

# Storage targets
BRONZE_DIR = STARTER_CODE_DIR / "data" / "bronze"
QUARANTINE_DIR = STARTER_CODE_DIR / "data" / "quarantine"
LOGS_DIR = STARTER_CODE_DIR / "logs"

# Audit log target
AUDIT_LOG_PATH = LOGS_DIR / "ingestion_audit.jsonl"

# Sample batch directories
SAMPLE_BATCHES_DIR = DATA_DIR / "sample_batches"
BATCH_2_DIR = SAMPLE_BATCHES_DIR / "batch_2_duplicate_redelivery"
BATCH_3_DIR = SAMPLE_BATCHES_DIR / "batch_3_schema_drift"
BATCH_4_DIR = SAMPLE_BATCHES_DIR / "batch_4_schema_drift_skill_update"
BATCH_5_DIR = SAMPLE_BATCHES_DIR / "batch_5_data_quality"

# Entities and their primary business keys
ENTITIES = {
    "customers": "customer_id",
    "orders": "order_id",
    "sales_transactions": "order_id",
    "products": "product_id",
    "stores": "store_id",
    "returns": "return_id",
}

# Baseline batch 1 files mapping (all 5 entities)
BATCH_1_FILES = {
    "customers": DATA_DIR / "customers.csv",
    "products": DATA_DIR / "products.csv",
    "stores": DATA_DIR / "stores.csv",
    "sales_transactions": DATA_DIR / "sales_transactions.csv",
    "returns": DATA_DIR / "returns.csv",
}

# Complete batch configurations
BATCHES = {
    "batch_1": BATCH_1_FILES,
    "batch_2": {
        "sales_transactions": BATCH_2_DIR / "sales_transactions_batch2_duplicate.csv",
    },
    "batch_3": {
        "customers": BATCH_3_DIR / "customers_batch3_loyalty_tier.csv",
    },
    "batch_4": {
        "customers": BATCH_4_DIR / "customers_batch4_unexpected_column.csv",
    },
    "batch_5": {
        "customers": BATCH_5_DIR / "customers_batch5_null_customer_id.csv",
    },
}