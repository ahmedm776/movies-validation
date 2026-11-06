# Execution record

Baseline: original notebook code except install and profiling; data path changed to
public mirror. Completed. Final YEAR entirely null,7,514 rows. Historical notebook
also showed7,514rows and0nonnull YEAR, independently agreeing with the reproduced defect.

Improved script: one intermediate run failed on nullable Int64 votes median792.5.
Fixed votes conversion to float64 for median imputation; reran successfully including
profiling. Final source is the executed version. Output accounting and exact counts
are in run_report.json;4 tests passed. Expected raw GX failures retained honestly.

The attached original notebook is a native saved export with historical outputs,
not fresh-run outputs. No fabricated notebook execution counts or plots were added.
The portfolio script is separately assistant-improved. Mirror identity to the full
Drive CSV was verified on 2026-11-05 (PROVENANCE_2026-11-05.md): identical size
(3,112,190 bytes) and SHA-256, so mirror findings are byte-identical recovery of his
dataset. This verification changes provenance only, not any code, fixture or number.

Final revision rerun including profiling AND optional pedagogical branch. Conservative
default retains9490rows,579missing years and1991IQRflags without dropping them.
Optional pedagogical branch separately leaves6967rows after2523exclusions.
All4tests pass on final source. This revised archive supersedes the earlier package.
