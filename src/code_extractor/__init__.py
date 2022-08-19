"""
Allows to save python functions and classes and load them without knowing the code.

This exports:
    - extract_code: to extract code to a string
    - load_code: to load code from a string extracted by this package
    - dump, dumps, load, loads: familiar API from the pickle and marshal modules
"""
__version__ = "0.2.0"

from .extractor.extract import extract_code
from .loader.load import load_code
from .pickle import dump, dumps, load, loads
