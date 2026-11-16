# Pysmell ported to Python 3

Python code smell detector by Chen et al., used by Zhang et al. (2024) to
build the phase 1 dataset. In this pipeline it is used to select instances
(phase 1 checks and phase 2 detection on the PyExamine corpus), to check the
adapted units, and, in the validation and metrics steps, to check whether
the smell left the refactored code.

## Source

- Repository: <https://github.com/chenzhifei731/Pysmell>
- Commit: `233afebac24c910be89d065ffa661ec72458a62c` (2018-07-06)
- Source files: `pysmell/detection/astChecker.py` (metrics) and
  `pysmell/detection/detector.py` (thresholds)

## Why port it

The original is Python 2 and does not run in this environment. Even with
Python 2 installed it would not work: the Zhang et al. dataset is Python 3,
and the Python 2 parser does not read f-strings. The original also has no
command line; it is a script that reads metric CSVs generated beforehand.

The changes made by the port are listed in the header of `astChecker.py` and
in `compat.py`. They are few, and none of them touches the metric logic or
the thresholds.

Two pitfalls, already handled, that come back if someone "modernizes" the
code:

1. **Do not replace `astunparse` with `ast.unparse`.** `astunparse` puts
   parentheses around every nested lambda and `ast.unparse` does not. That
   shortens the NOC metric and loses Long Lambda Function instances (with
   `ast.unparse`, 4 of the 11 LLF snippets of Zhang et al. are no longer
   detected).
2. **Do not rename `visit_TryExcept` to `visit_Try`.** In Python 3 the node
   is called `ast.Try`, so this visitor never fires, and that is what is
   wanted: the original method does not call `generic_visit` in the normal
   flow, so renaming it makes the detector skip the body of every `try`
   block and lose instances (e.g. `Natsar-main/modules/tele.py`).

## Threshold strategy

Pysmell has three sets of thresholds. This project uses **Tuning Machine**,
the same as Zhang et al. (section 3.1 of the paper), which has the highest
precision according to Chen et al. (2018). The three sets are in `detect.py`
and can be chosen with `--strategy`, but the default is `tuning`.

## Validation

The Zhang et al. dataset is NOT versioned in this repository (it is
third-party code; see `.gitignore`). Download it from Zenodo and unzip it
into `data/dataset_zhang/`, so that `data/dataset_zhang/dataset/files/`
exists:

- <https://doi.org/10.5281/zenodo.13335000>

`validate_port.py` runs the port on the 311 files of the dataset and
compares the result with `results of RQ1.xlsx` and with the numbers in the
paper:

```bash
python -m pysmell.validate_port
```

Current result (Python 3.14.6, astunparse 1.6.3):

| | Paper | Port |
|---|---|---|
| .py files | 311 | 311 |
| Zhang et al. snippets reproduced (4 smells) | 83 | **83** |
| Detections in Repositories (10 smells) | 57 | **57** |
| Detections in Code (10 smells) | 630 | 394 |

The 83 snippets and the Repositories total match exactly. The difference in
Code remains unexplained and does not affect the sample: all 45 Zhang et al.
instances under the Code label are reproduced. Part of it may come from the
3 files that do not parse in Python 3 (`Code/main-3.py`,
`Repositories/machine.py`, `Repositories/sokoban.py`), none of which holds
an instance in the dataset. Another hypothesis, not verified, is that the
folder has 138 files in Code and 173 in Repositories, while the paper says
140 and 171 (the total of 311 matches).

Run it again after changing `astChecker.py`, `compat.py` or `detect.py`.
The script exits with code 1 if any Zhang et al. snippet stops being
reproduced.

## Usage

```bash
# study smells (STUDY_SMELLS in detect.py), tuning strategy
python -m pysmell.detect path/to/code.py
python -m pysmell.detect folder/ --output result.csv

# the 10 smells of Chen et al.
python -m pysmell.detect folder/ --all

# include measurements below the threshold (compare original and refactored)
python -m pysmell.detect file.py --metrics
```

As a library:

```python
from pysmell.detect import detect_file, measure_file, measure_source
```

## Files

- `astChecker.py` - port of the metric extractor (AST visitors).
- `compat.py` - astunparse shim and list of Python 2 AST types.
- `detect.py` - thresholds of the original `detector.py` plus command line.
- `validate_port.py` - checks the port against the Zhang et al. dataset.
- `_xlsx.py` - minimal .xlsx reader, only for the Zhang et al. spreadsheets.
