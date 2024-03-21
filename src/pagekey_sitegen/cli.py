import argparse
import os
import shutil
import sys
from typing import List
from pagekey_sitegen.config import TemplateName, load_config

from pagekey_sitegen.core import (
    get_file_as_string,
    get_files_list,
    get_repo_root,
    remove_output_directory,
    create_output_directory,
    render_file,
    render_template,
)


class DocsDirNotFoundException(Exception):
    pass

def main(args_list: List[str] = sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='pagekey-sitegen', description='Generate documentation site from directory.')
    parser.add_argument('docs_dir', metavar='docs_dir', type=str, help='The path to the documents directory')

    args = parser.parse_args(args_list)
    
    if not os.path.exists(args.docs_dir):
        raise DocsDirNotFoundException()
    
    remove_output_directory()
    create_output_directory()

    files = get_files_list(args.docs_dir)

    # Grab config
    config_path = os.path.join(args.docs_dir, 'site.yaml')
    config_raw = get_file_as_string(config_path)
    config = load_config(config_raw)

    # Render templates
    repo_root = get_repo_root()
    templates_dir = os.path.join(repo_root, 'templates', config.template.value)
    for template in os.listdir(templates_dir):
        render_template(template, config)

    # Render source files
    for cur_file in files:
        render_file(cur_file, config)

    # Generate the site
    os.chdir(f'build/{config.template.value}')
    if config.template == TemplateName.SPHINX:
        os.system('make html')

        # Move the generated site to the top level of the build directory
        shutil.move('_build/html', '..')
    elif config.template == TemplateName.NEXT:
        print("config next")
