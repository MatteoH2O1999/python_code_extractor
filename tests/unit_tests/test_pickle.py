import pytest

from unittest.mock import patch, MagicMock

import code_extractor.pickle


def test_dumps():
    with patch("pickle.dumps") as mock_pickle, patch(
        "code_extractor.pickle.pickle_code.extract_code"
    ) as mock_extract:
        mock_extract.return_value = "Test string"
        mock_object = MagicMock()

        code_extractor.pickle.dumps(mock_object, 2, False)

        mock_extract.assert_called_once_with(mock_object)
        mock_pickle.assert_called_once_with(
            obj="Test string", protocol=2, fix_imports=False
        )


def test_dump():
    with patch("pickle.dump") as mock_pickle, patch(
        "code_extractor.pickle.pickle_code.extract_code"
    ) as mock_extract:
        mock_extract.return_value = "Test string"
        mock_object = MagicMock()
        mock_file = MagicMock()

        code_extractor.pickle.dump(mock_object, mock_file, 2, False)

        mock_extract.assert_called_once_with(mock_object)
        mock_pickle.assert_called_once_with(
            obj="Test string", protocol=2, fix_imports=False, file=mock_file
        )


def test_loads_success():
    with patch("pickle.loads") as mock_pickle, patch(
        "code_extractor.pickle.pickle_code.load_code"
    ) as mock_load, patch("json.loads") as mock_json:
        mock_pickle.return_value = "Test string"
        mock_json.return_value = "Extracted json"
        mock_loaded = MagicMock()
        mock_load.return_value = mock_loaded
        mock_object = b"Test input"

        ret = code_extractor.pickle.loads(mock_object, False, "utf-8", "strict")

        assert ret is mock_loaded
        mock_pickle.assert_called_once_with(
            mock_object, fix_imports=False, encoding="utf-8", errors="strict"
        )
        mock_json.assert_called_once_with("Test string")
        mock_load.assert_called_once_with("Test string")


def test_loads_failure():
    with patch("pickle.loads") as mock_pickle, patch(
        "code_extractor.pickle.pickle_code.load_code"
    ) as mock_load, patch("json.loads") as mock_json:
        mock_pickle.return_value = "Test string"
        mock_json.side_effect = ValueError()
        mock_loaded = MagicMock()
        mock_load.return_value = mock_loaded
        mock_object = b"Test input"

        ret = None
        with pytest.raises(ValueError):
            ret = code_extractor.pickle.loads(mock_object, False, "utf-8", "strict")

        assert ret is None
        mock_pickle.assert_called_once_with(
            mock_object, fix_imports=False, encoding="utf-8", errors="strict"
        )
        mock_json.assert_called_once_with("Test string")
        mock_load.assert_not_called()


def test_load_success():
    with patch("pickle.load") as mock_pickle, patch(
        "code_extractor.pickle.pickle_code.load_code"
    ) as mock_load, patch("json.loads") as mock_json:
        mock_pickle.return_value = "Test string"
        mock_json.return_value = "Extracted json"
        mock_loaded = MagicMock()
        mock_load.return_value = mock_loaded
        mock_file = MagicMock()

        ret = code_extractor.pickle.load(mock_file, False, "utf-8", "strict")

        assert ret is mock_loaded
        mock_pickle.assert_called_once_with(
            file=mock_file, fix_imports=False, encoding="utf-8", errors="strict"
        )
        mock_json.assert_called_once_with("Test string")
        mock_load.assert_called_once_with("Test string")


def test_load_failure():
    with patch("pickle.load") as mock_pickle, patch(
        "code_extractor.pickle.pickle_code.load_code"
    ) as mock_load, patch("json.loads") as mock_json:
        mock_pickle.return_value = "Test string"
        mock_json.side_effect = ValueError()
        mock_loaded = MagicMock()
        mock_load.return_value = mock_loaded
        mock_file = MagicMock()

        ret = None
        with pytest.raises(ValueError):
            ret = code_extractor.pickle.load(mock_file, False, "utf-8", "strict")

        assert ret is None
        mock_pickle.assert_called_once_with(
            file=mock_file, fix_imports=False, encoding="utf-8", errors="strict"
        )
        mock_json.assert_called_once_with("Test string")
        mock_load.assert_not_called()
