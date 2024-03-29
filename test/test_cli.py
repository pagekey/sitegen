import os
from unittest.mock import call, patch

import pytest
from pagekey_sitegen.cli import DocsDirNotFoundException, main


MODULE_UNDER_TEST = "pagekey_sitegen.cli"

@patch("os.path.exists", return_value=False)
def test_main_fails_when_directory_dne(mock_exists):
    command_list = ["build", "docs/"]
    with pytest.raises(DocsDirNotFoundException):
        main(command_list)
    mock_exists.assert_called()

@patch(f"{MODULE_UNDER_TEST}.SiteGenerator")
@patch("os.path.exists", return_value=True)
def test_site_generator_called_when_directory_exists(mock_exists, mock_site_generator):
    command_list = ["build", "docs/"]
    main(command_list)
    mock_exists.assert_called()
    mock_site_generator.assert_called()
