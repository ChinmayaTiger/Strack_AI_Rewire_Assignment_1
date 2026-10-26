"""Project configuration: paths and batch definitions.

Scaffolding only. Paths already point at the sibling data/ and .claude/skills/
folders one level up from starter-code/ so you can build here without
touching the reference project's own src/, tests/, bronze/. Everything
this template writes (bronze output, logs) stays inside starter-code/
so it never collides with the existing solution.

Fill in ON_EXISTING_KEY, ENTITY_BUSINESS_KEYS and BATCHES below as you
implement each task - they are intentionally incomplete.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]   # assignment package root
TEMPLATE_ROOT = Path(__file__).resolve().parents[1]   # .../starter-code

DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_BATCHES_DIR = DATA_DIR / "sample_batches"
SKILLS_DIR = PROJECT_ROOT / "skills"

BRONZE_DIR = TEMPLATE_ROOT / "bronze"
QUARANTINE_DIR = TEMPLATE_ROOT / "quarantine"
LOGS_DIR = TEMPLATE_ROOT / "output" / "logs"
AUDIT_LOG_PATH = LOGS_DIR / "ingestion_audit.jsonl"

# The business/natural key for each entity - see Assignment Section 4.1 and
# the idempotency skill. Used by your dedup/merge logic (Task 3) and your
# data-quality validation (Task 7).
ENTITY_BUSINESS_KEYS = {
    "customers": "customer_id",
    "products": "product_id",
    "stores": "store_id",
    "sales_transactions": "order_id",
    "returns": "return_id",
}

# TODO (Task 3 / skill_gap_notes-style decision): when a redelivered row's
# business key already exists in bronze, do you keep the stored row or
# replace it with the incoming one? This can be a single global policy or
# vary per entity - document your choice in the README.
# ON_EXISTING_KEY = {"customers": "keep", "sales_transactions": "keep"}

# TODO: describe each batch you will run, e.g.
# BATCHES = [
#     {"batch_id": "batch_1", "entities": {"customers": DATA_DIR / "customers.csv", ...}},
#     {"batch_id": "batch_2", "entities": {"sales_transactions": SAMPLE_BATCHES_DIR / "batch_2_duplicate_redelivery" / "sales_transactions_batch2_duplicate.csv"}},
#     ...
# ]
BATCHES = []
