# `reference`

This directory contains "reference" files --
stuff that is not directly shipped with RAIMAD,
but parsed by scripts under `scripts` to generate
parts of RAIMAD code.

## `reference/vendor/klayout`

Contains verbatim source code files from KLayout.
There can be re-downloaded using `scripts/get_klayout_dither_patterns.sh`.
These are parsed by `scripts/patch_klayout_dither_patterns.py`
to get the names of KLayout's builtin line styles and dither
patterns (called "stipple patterns" in the UI)
and patch them into `src/raimad/cif/lyp.py`.
KLayout's own license is also contained here.

## `reference/raidithers`

These are XBM (X Bitmap) images of RAIMAD's own dither patterns
that are parsed by `scripts/patch_raidithers.py` to generate
the definitions
in `src/raimad/cif/lyp.py`.
XBM is a bit of an arcane image format,
but it can both be edited in GIMP and easily parsed in pure Python,
which is why I chose it.

