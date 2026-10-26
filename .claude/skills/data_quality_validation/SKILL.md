---
name: data-quality-validation
description: >
  Validate incoming batch DataFrames for critical data quality issues (such as null
  or blank business keys) before writing to Bronze. Route valid rows to Bronze and
  quarantined rows to a dedicated quarantine store with reason and lineage metadata.
---

# Skill Name: Data Quality Validation and Quarantine Routing

## Purpose
Ensure low-quality or corrupt records (e.g., records missing critical primary business identifiers) are intercepted before polluting the Bronze layer, while retaining the corrupt records in an auditable quarantine storage with diagnostic metadata.

## Problem This Skill Solves
In an AI-native data lakehouse, ingesting records with null or blank primary keys breaks downstream joins, indexing, deduplication, and silver/gold layer aggregations. Rather than failing the entire batch, valid records must be committed, and invalid records isolated with actionable reasons.

## When to Use
- Applied to every incoming batch immediately after ingestion metadata tagging and prior to idempotent writing.
- Applicable to all entities using their respective business keys.

## Rules & Decisions
1. **Business Key Integrity**: A record is considered INVALID if its `business_key` is:
   - SQL `NULL`
   - Empty string `""`
   - Whitespace string `"   "`
2. **Split Output**: Partition the input into two DataFrames:
   - `valid_df`: Rows satisfying all data quality checks.
   - `quarantined_df`: Rows violating any rule, tagged with a descriptive `quarantine_reason` column.
3. **Metadata Preservation**: Quarantined rows MUST retain all original attributes and all ingestion metadata (`batch_id`, `source_file`, `ingestion_timestamp`).

## Expected Outcome
- Clean records advance to Bronze storage without interruption.
- Corrupted records are written to Parquet in the quarantine directory.
