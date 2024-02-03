from unittest.mock import patch

import pytest
from pagekey_docgen.cli import DocsDirNotFoundException, main


@patch("os.path.exists", return_value=False)
def test_main_fails_when_directory_dne(mock_exists):
    docs_dir = ["docs/"]
    with pytest.raises(DocsDirNotFoundException):
        main(docs_dir)
    mock_exists.assert_called()
