from unittest.mock import patch
from pagekey_docgen.core import (
    get_files_list,
    create_output_directory,
    remove_output_directory,
    render_file,
)


@patch('os.walk', return_value=[
    ('.', ['dir'], ['file1.txt']),
    ('dir', [], ['file2.txt']),
])
def test_get_files_list_returns_all_files_when_directory_exists(mock_walk):
    my_path = 'docs/'
    the_list = get_files_list(my_path)
    mock_walk.assert_called_with(my_path)
    assert len(the_list) == 2
    assert 'file1.txt' in the_list
    assert 'dir/file2.txt' in the_list

@patch('os.makedirs')
def test_create_output_directory_creates_single_directory(mock_mkdirs):
    create_output_directory()
    mock_mkdirs.assert_called_with('build')

@patch('shutil.rmtree')
@patch("os.path.exists", return_value=True)
def test_remove_output_directory_removes_directory_when_exists(mock_exists, mock_rmtree):
    remove_output_directory()
    mock_exists.assert_called()
    mock_rmtree.assert_called_with('build')

@patch('shutil.rmtree')
@patch("os.path.exists", return_value=False)
def test_remove_output_directory_does_nothing_when_directory_dne(mock_exists, mock_rmtree):
    remove_output_directory()
    mock_exists.assert_called()
    mock_rmtree.assert_not_called()

@patch('shutil.copy')
def test_render_file_with_valid_file_adds_file_to_output_directory(mock_cp):
    a_file = 'index.md'
    render_file(a_file)
    mock_cp.assert_called_with(a_file, 'build/index.html')

@patch('os.makedirs')
@patch('shutil.copy')
def test_render_file_with_nested_file_adds_file_to_output_directory(mock_cp, mock_mkdirs):
    a_file = 'subsystem/index.md'
    render_file(a_file)
    mock_mkdirs.assert_called_with('build/subsystem', exist_ok=True)
    mock_cp.assert_called_with(a_file, 'build/subsystem/index.html')
