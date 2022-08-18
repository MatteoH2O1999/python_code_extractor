<h1 align="center">Python code extractor</h1>

<p align="center">
<a href="https://github.com/MatteoH2O1999/python_code_extractor/actions/workflows/test.yml"><img src="https://github.com/MatteoH2O1999/python_code_extractor/actions/workflows/test.yml/badge.svg" alt="Test package"></a>
<a href="https://github.com/MatteoH2O1999/python_code_extractor/actions/workflows/release.yml"><img src="https://github.com/MatteoH2O1999/python_code_extractor/actions/workflows/release.yml/badge.svg" alt="Release package"></a>
<a href="https://github.com/MatteoH2O1999/python_code_extractor/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/code_extractor" alt="PyPI - License"></a>
<a href="https://codecov.io/gh/MatteoH2O1999/python_code_extractor"><img src="https://codecov.io/gh/MatteoH2O1999/python_code_extractor/branch/main/graph/badge.svg?token=MV9PYET185" alt="codecov"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
<a href="https://badge.fury.io/py/code_extractor"><img src="https://badge.fury.io/py/code_extractor.svg" alt="PyPI version"></a>
<a href="https://badge.fury.io/py/code_extractor"><img src="https://img.shields.io/pypi/pyversions/code_extractor" alt="PyPI - Python Version"></a>
<a href="https://pepy.tech/project/code_extractor"><img src="https://pepy.tech/badge/code_extractor" alt="Downloads"></a>
</p>

Python code extractor

## Dependencies

Written in pure `Python` and has no dependencies other than the base libraries.

## Installation

From source code:

```commandline
pip install .
```

From `PyPI`:

```commandline
pip install code-extractor
```

## Import

### Main functions

```python
import code_extractor
from code_extractor import extract_code, load_code
```

### Pickle API

```python
import code_extractor.pickle
```

or as a drop-in for `pickle`:
```python
import code_extractor.pickle as pickle
```

## Usage

Given the following:

```python
class Class:
    def __init__(self):
        self.test = 42

def function():
    return 42
```

Use

```pycon
>>> import code_extractor
>>> extracted_class = code_extractor.extract_code(Class)
>>> extracted_function = code_extractor.extract_code(function)
>>> reconstructed_class = code_extractor.load_code(extracted_class)
>>> instance = reconstructed_class()
>>> instance.test
42
>>> reconstructed_function = code_extractor.load_code(extracted_function)
>>> reconstructed_function()
42
```

## Pickle module

```pycon
>>> import code_extractor
>>> code_extractor.dump(...)
>>> code_extractor.dumps()
>>> code_extractor.load(...)
>>> code_extractor.loads(...)
```

Or

```pycon
>>> import code_extractor.pickle as pickle
>>> pickle.dump(...)
>>> pickle.dumps(...)
>>> pickle.load(...)
>>> pickle.loads(...)
```

