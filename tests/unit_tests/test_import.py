import inspect

import code_extractor
import code_extractor.pickle as code_pickler


def test_import_module():
    assert getattr(code_extractor, "extract_code", None) is not None
    assert getattr(code_extractor, "load_code", None) is not None
    assert inspect.isfunction(code_extractor.extract_code)
    assert inspect.isfunction(code_extractor.load_code)


def test_import_pickle():
    assert getattr(code_pickler, "dumps", None) is not None
    assert getattr(code_pickler, "dump", None) is not None
    assert getattr(code_pickler, "loads", None) is not None
    assert getattr(code_pickler, "load", None) is not None
    assert inspect.isfunction(code_pickler.load)
    assert inspect.isfunction(code_pickler.loads)
    assert inspect.isfunction(code_pickler.dump)
    assert inspect.isfunction(code_pickler.dumps)
