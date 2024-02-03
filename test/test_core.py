from unittest.mock import patch
from pagekey_docgen.core import (
    get_files_list,
    create_output_directory,
    remove_output_directory,
    render_file,
)


@patch('os.walk', return_value=[
    ('.', ['folder1'], ['file1.txt']),
    ('./folder1', [], ['file.txt']),
])
def test_get_files_list_returns_all_files_when_directory_exists(mock_walk):
    my_path = 'docs/'
    the_list = get_files_list(my_path)
    mock_walk.assert_called_with(my_path)
    assert len(the_list) == 2
    assert 'file1.txt' in the_list
    assert 'file.txt' in the_list

@patch('os.makedirs')
def test_create_output_directory_creates_single_directory(mock_mkdirs):
    create_output_directory()
    mock_mkdirs.assert_called_with('build')

@patch('shutil.rmtree')
def test_remove_output_directory_removes_directory(mock_rmtree):
    remove_output_directory()
    mock_rmtree.assert_called_with('build')

@patch('shutil.copy')
def test_render_file_with_valid_file_adds_file_to_output_directory(mock_cp):
    a_file = 'index.md'
    render_file(a_file)
    mock_cp.assert_called_with(a_file, 'build')

@patch('os.makedirs')
@patch('shutil.copy')
def test_render_file_with_nested_file_adds_file_to_output_directory(mock_cp, mock_mkdirs):
    a_file = 'subsystem/index.md'
    render_file(a_file)
    mock_mkdirs.assert_called_with('build/subsystem', exist_ok=True)
    mock_cp.assert_called_with(a_file, 'build/subsystem')
