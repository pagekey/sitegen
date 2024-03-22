

import os
from unittest.mock import MagicMock, call, mock_open, patch

from pagekey_sitegen.generator import SiteConfig, SiteGenerator, TemplateName, get_file_as_string, get_files_list, write_string_to_file


def sample_site_config():
    """
    Sample site config for testing.
    """
    return SiteConfig(
        project='My Project',
        copyright='My Copyright',
        author='My Author',
        release='My Release',
        package='My Package',
        template=TemplateName.SPHINX
    )

class TestSiteConfig:

    def test_from_path(self):
        pass


class TestSiteGenerator:

    def test_init(self):
        pass

    @patch('pagekey_sitegen.generator.SiteGenerator._build_sphinx')
    @patch('pagekey_sitegen.generator.SiteGenerator._render_template')
    @patch('pagekey_sitegen.generator.SiteGenerator._render_source')
    @patch('pagekey_sitegen.generator.SiteGenerator._setup_build_dir')
    @patch('pagekey_sitegen.generator.SiteConfig.from_path')
    @patch('pagekey_sitegen.generator.get_files_list')
    def test_generate(self,
        mock_get_files_list,
        mock_config_from_path, 
        mock_setup_build_dir,
        mock_render_source, 
        mock_render_template,
        mock_build_sphinx,
    ):
        mock_get_files_list.side_effect = [['template1.txt'],['source1.txt']]
        SiteGenerator('.').generate()
        mock_render_template.assert_called_with('template1.txt')
        mock_render_source.assert_called_with('source1.txt')

    def test_render_template(self):
        pass

    def test_render_source(self):
        pass


@patch('os.walk', return_value=[
    ('.', ['dir'], ['file1.txt']),
    ('dir', [], ['file2.txt']),
])
def test_get_files_list(mock_walk):
    my_path = 'docs/'
    the_list = get_files_list(my_path)
    mock_walk.assert_called_with(my_path)
    assert len(the_list) == 2
    assert os.path.abspath('file1.txt') in the_list
    assert os.path.abspath('dir/file2.txt') in the_list


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
