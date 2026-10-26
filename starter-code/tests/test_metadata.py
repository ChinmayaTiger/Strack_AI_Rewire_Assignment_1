"""Tests for src/metadata.py (Task 2). Stubs only - implement the asserts."""
import pytest


@pytest.mark.skip(reason="TODO: implement once add_ingestion_metadata is written")
def test_metadata_columns_present_and_populated(spark):
    # TODO: build a small fixture DataFrame, call add_ingestion_metadata,
    # assert batch_id / source_file / ingestion_timestamp are present and
    # non-null on every row, and that original columns are unchanged.
    pass


@pytest.mark.skip(reason="TODO: implement once add_ingestion_metadata is written")
def test_metadata_never_overwrites_a_source_column(spark):
    # TODO: build a fixture with a column literally named batch_id and
    # decide/assert what your implementation does about the collision.
    pass
