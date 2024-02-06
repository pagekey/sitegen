from pagekey_docgen.config import load_config


def test_load_config_works_with_valid_string():
    yaml_config = """
        project: 'PROJECT_NAME_HERE'
        copyright: '2024, AUTHOR_NAME_HERE'
        author: 'AUTHOR_NAME_HERE'
        release: 'PROJECT_RELEASE_HERE'
    """
    config = load_config(yaml_config)

    assert config.project == 'PROJECT_NAME_HERE'
    assert config.copyright == '2024, AUTHOR_NAME_HERE'
    assert config.author == 'AUTHOR_NAME_HERE'
    assert config.release == 'PROJECT_RELEASE_HERE'
