import os
from unittest.mock import call, patch

import pytest
from pagekey_docgen.cli import DocsDirNotFoundException, main


MODULE_UNDER_TEST = "pagekey_docgen.cli"

@patch("os.path.exists", return_value=False)
def test_main_fails_when_directory_dne(mock_exists):
    docs_dir = ["docs/"]
    with pytest.raises(DocsDirNotFoundException):
        main(docs_dir)
    mock_exists.assert_called()

@patch('shutil.move')
@patch('os.system')
@patch('os.chdir')
@patch(f"{MODULE_UNDER_TEST}.render_template")
@patch(f"{MODULE_UNDER_TEST}.render_file")
@patch(f"{MODULE_UNDER_TEST}.get_file_as_string")
@patch(f"{MODULE_UNDER_TEST}.get_files_list", return_value=[
    "file1.txt",
    "dir/file2.txt",
])
@patch(f"{MODULE_UNDER_TEST}.create_output_directory")
@patch(f"{MODULE_UNDER_TEST}.remove_output_directory")
@patch("os.path.exists", return_value=True)
def test_main_renders_each_file_when_directory_valid(
    mock_exists,
    mock_remove_output_directory,
    mock_create_output_directory,
    mock_get_files_list,
    mock_get_file_as_string,
    mock_render_file,
    mock_render_template,
    mock_chdir,
    mock_system,
    mock_move,
):
    docs_dir = "docs/"
    main([docs_dir])
    mock_exists.assert_called()

    mock_remove_output_directory.assert_called()
    mock_create_output_directory.assert_called()
    mock_get_files_list.assert_called_with(docs_dir)

    mock_get_file_as_string.assert_called_with(os.path.join(docs_dir, 'site.yaml'))
    # The files get copied
    assert mock_render_file.call_args_list[0] == call("file1.txt")
    assert mock_render_file.call_args_list[1] == call("dir/file2.txt")
    # The templates get copied
    assert call("Makefile") in mock_render_template.call_args_list
    assert call("make.bat") in mock_render_template.call_args_list
    assert call("conf.py") in mock_render_template.call_args_list

    # Should run `make html` to generate sphinx site
    mock_chdir.assert_called_with('build/sphinx')
    mock_system.assert_called_with('make html')
    mock_move.assert_called_with('_build/html', '..')
