# Dataset provenance verification (2026-11-05)

Question: is the public mirror CSV used for all findings in this package byte-identical
to Ahmed's own original dataset in his Google Drive?

Method: downloaded both files fresh on 2026-11-05 and compared size and SHA-256.

- User's original: Google Drive file id 1qUdPhjzgLqQgb9e3B5yfBtm0f72Cb1be
  (movies.csv, last modified 2026-03-15 per Drive metadata), 3,112,190 bytes,
  SHA-256 f3666b7b60c1a23f8daecda305b4ddb661c6f3f0d7a692efa810d93b912f8902
- Public mirror: https://joannabieri.com/mathdatascience/data/movies.csv,
  3,112,190 bytes,
  SHA-256 f3666b7b60c1a23f8daecda305b4ddb661c6f3f0d7a692efa810d93b912f8902

Result: BYTE-IDENTICAL. The mirror equals the user's Drive CSV, so every finding in
this package previously labelled "for this mirror" is a finding on his actual dataset.
No code, fixture, test or number in the package changed as a result of this check;
this note upgrades provenance documentation only. Dataset rights for public release
remain unestablished, as before.
