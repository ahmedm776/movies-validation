# Movies Dataset Validation

Data-quality validation for a movies dataset (9,999 rows x 9 columns):
an expectation suite (Great Expectations checkpoint plus Cerberus
validators), baseline runs, a verification report, and full provenance.
Pairs a preserved original DSAI202 Assignment 1 notebook (source-only)
with a later, tested validation pipeline.

## Contents

- `original_assignment1.ipynb` - original coursework notebook, source-only
  (historical outputs stripped).
- `portfolio_movies.py`, `run_baseline.py` - validation pipeline and
  baseline runner.
- `test_movies.py` / `tests.log` - unit tests.
- `expectation_suite.json`, `validation_summary.json`, `run_report.json`,
  `baseline_status.json` - executed-run records.
- `VERIFICATION.md`, `PROVENANCE_2026-11-05.md` - verification and
  provenance write-ups.
- `profile-preview.png` - preview image of the generated profile report
  (summary statistics only).

## Verification scope

- Tested 2026-11-04 on Python 3.10. Public mirror input: 9,999 rows,
  9 columns.
- Mirror: https://joannabieri.com/mathdatascience/data/movies.csv
- Candidate dataset source:
  https://www.kaggle.com/datasets/bharatnatrayn/movies-dataset-for-feature-extracion-prediction
- The mirror is byte-verified identical to the dataset copy used for the
  original assignment (SHA-256 match, see PROVENANCE_2026-11-05.md), so the
  mirror findings are findings on that dataset. Dataset redistribution
  rights were not established: no CSV, row-level outputs, or the full
  profiling HTML are redistributed here.

## Conservative portfolio default

- Parse start year while retaining YEAR_RAW unchanged and missing years as
  missing.
- Use actual Cerberus validators and exact genre tokens; the
  Great Expectations suite and checkpoint execute.
- Preserve all statistical extremes, flagged by IQR_FLAG, not removed as
  erroneous.
- No median imputation or scaling in default output; the raw snapshot is
  preserved at runtime.
- Explicitly separate the 80 missing-genre exclusions and 429 duplicates on
  transformed fields.

## Attribution

- The original DSAI202 assignment notebook is preserved as recovered; its
  team/solo context is not recorded, so no sole-authorship claim is made for
  it. The original assignment carried course rules on AI-generated
  submission work: nothing here is an assignment submission or presented as
  one.
- The validation pipeline, tests and reports are later portfolio work,
  built with AI-assistant help and presented as such.

## Run and test

Raw dataset files are not bundled. Download the CSV from the mirror linked above,
then use the declared Great Expectations 0.18.x environment in requirements.lock.txt
(the current Great Expectations 1.x API is incompatible with this script).

```bash
pip install -r requirements.lock.txt
python portfolio_movies.py /path/to/movies.csv --output final-output
python test_movies.py
```

The conservation test reads the generated final-output directory. It is not a
standalone test of an empty checkout. The pipeline reproduces 9,490 default rows
from the 9,999-row source; no training is involved.
