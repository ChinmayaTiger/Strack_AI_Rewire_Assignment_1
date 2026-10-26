# Starter Template — Bronze Ingestion Assignment

This is a **blank scaffold**, not a solution. It gives you the project
structure, module boundaries, and function signatures the assignment
expects (see `../Stack AI Rewire - Data Engineering  - Bronze Layer - Assignment Doc.docx` and
`../Helper Guide.docx`) so you can focus on
implementing against the skills rather than deciding how to organize the
code. Every function raises `NotImplementedError` — that is intentional.

It sits alongside, and reads from, the project's existing `data/` and
`.claude/skills/` folders one level up. It writes its own output under
`starter-code/bronze/`, `starter-code/quarantine/` and
`starter-code/output/logs/`, so nothing you do here touches the
project's existing reference solution or bronze output.

## Structure

```
starter-code/
├── src/
│   ├── spark_session.py     Task 1 — SparkSession factory
│   ├── config.py            Task 1 — paths, business keys, batch defs
│   ├── ingest.py             Task 1-2 — read a source CSV, tag it
│   ├── metadata.py           Task 2 — ingestion metadata columns
│   ├── schema_utils.py       Task 4 (and Task 6) — schema drift
│   ├── idempotent_writer.py  Task 3 — dedup / merge / write bronze
│   ├── data_quality.py       Task 7 — YOUR new skill (empty placeholder)
│   ├── audit.py              Task 5 — audit log
│   └── pipeline.py           main entry point wiring it all together
├── tests/                     one stub file per task, all skipped until
│                               you implement the corresponding module
├── requirements.txt
├── pytest.ini
└── README.md (this file)
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Suggested order of work

Follow the tasks in the assignment document in order — each stub module
notes which task and which `.claude/skills/*/SKILL.md` file it depends on:

1. **Task 1** — `spark_session.py`, `config.py`: get a SparkSession running
   and decide your paths/batch list.
2. **Task 2** — `ingest.py`, `metadata.py`: load Batch 1 and tag every row.
   Run `pytest tests/test_ingestion.py tests/test_metadata.py` (remove the
   `@pytest.mark.skip` lines as you implement each test).
3. **Task 3** — `idempotent_writer.py`: re-run Batch 1, then Batch 2
   (`data/sample_batches/batch_2_duplicate_redelivery/`), confirm no
   duplicates.
4. **Task 4** — `schema_utils.py`: Batch 3
   (`data/sample_batches/batch_3_schema_drift/`), confirm `loyalty_tier` is
   detected, logged and backfilled correctly.
5. **Task 5** — `audit.py`: wire an audit record into every batch/entity run.
6. **Task 6** (required activity) — before touching Batch 4
   (`data/sample_batches/batch_4_schema_drift_skill_update/`), read
   `.claude/skills/schema_drift/SKILL.md`, find the gap it leaves for a *second*
   drift event on an already-evolved schema, and **modify that skill file
   yourself**. Only then extend `schema_utils.py` to satisfy it.
7. **Task 7** (required activity) — before touching Batch 5
   (`data/sample_batches/batch_5_data_quality/`), **write
   `.claude/skills/data_quality_validation/SKILL.md` yourself** (it does not exist
   yet — this template does not provide it), then implement
   `data_quality.py` against your own skill.

## Running

Once implemented:

```bash
python -m src.pipeline --batch batch_1
python -m src.pipeline --batch batch_1   # re-run: should be a no-op
python -m src.pipeline --batch batch_2
python -m src.pipeline --batch batch_3
python -m src.pipeline --batch batch_4   # after Task 6
python -m src.pipeline --batch batch_5   # after Task 7
```

## Testing

```bash
pytest
```

All tests are `@pytest.mark.skip`'d out of the box. Remove the skip marker
for each test only once you've implemented the module it covers — do not
delete the assertions-to-write comments without actually writing the
assertions.

## What this template deliberately does NOT include

- No working pipeline logic — every `src/` function raises
  `NotImplementedError`.
- No modifications to `../.claude/skills/schema_drift/SKILL.md` — it is still the
  original, unmodified baseline; you edit that file directly as part of
  Task 6 (there is only one copy, shared by the whole project).
- No `../.claude/skills/data_quality_validation/SKILL.md` — you create it yourself,
  as a new folder under the project's `.claude/skills/`, as part of Task 7.
- No bronze output, audit log, or test assertions — those are produced by
  your implementation, not provided.
