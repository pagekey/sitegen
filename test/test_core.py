from unittest.mock import mock_open, patch
from pagekey_docgen.core import (
    get_files_list,
    create_output_directory,
    remove_output_directory,
    render_file,
    get_repo_root,
    render_template,
    get_file_as_string,
    write_string_to_file,
)
from test.test_config import get_fake_config


MODULE_UNDER_TEST = 'pagekey_docgen.core'

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
    mock_cp.assert_called_with(a_file, 'build/sphinx')

@patch('os.makedirs')
@patch('shutil.copy')
def test_render_file_with_nested_file_adds_file_to_output_directory(mock_cp, mock_mkdirs):
    a_file = 'subsystem/index.md'
    render_file(a_file)
    mock_mkdirs.assert_called_with('build/sphinx/subsystem', exist_ok=True)
    mock_cp.assert_called_with(a_file, 'build/sphinx/subsystem')

def test_get_repo_root_returns_valid_path():
    mock_file_path = "/path/to/mock/core.py"
    with patch('__main__.__file__', mock_file_path):
        the_root = get_repo_root(mock_file_path)
        assert the_root == "/path/to/mock"

@patch(f'{MODULE_UNDER_TEST}.write_string_to_file')
@patch(f'{MODULE_UNDER_TEST}.get_repo_root', return_value='the_root')
def test_render_template_works_when_file_valid(mock_get_repo_root, mock_write_string_to_file):
    fake_template = "{{ config.author }} is the author"
    fake_config = get_fake_config()
    with patch(f'{MODULE_UNDER_TEST}.get_file_as_string', return_value=fake_template) as mock_get_file_as_string:
        render_template("Makefile", fake_config)
        mock_get_repo_root.assert_called()
        mock_get_file_as_string.assert_called_with('the_root/templates/Makefile')
        mock_write_string_to_file.assert_called_with('build/sphinx/Makefile', fake_config.author + ' is the author')

@patch('builtins.open', new_callable=mock_open, read_data='Mocked file content')
def test_get_file_as_string(mock_file_open):
    filename = "my_file.txt"

    file_content = get_file_as_string("my_file.txt")

    mock_file_open.assert_called_once_with(filename, 'r')
    assert file_content == 'Mocked file content'

@patch('builtins.open', new_callable=mock_open, read_data='Mocked file content')
def test_write_string_to_file(mock_file_open):
    filename = "my_file.txt"
    data = "the data"

    write_string_to_file(filename, data)

    mock_file_open.assert_called_with(filename, 'w')
    mock_file_open.return_value.write.assert_called_once_with(data)
