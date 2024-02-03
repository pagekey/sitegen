import argparse
import os
import sys
from typing import List

from pagekey_docgen.core import (
    get_files_list,
    remove_output_directory,
    create_output_directory,
    render_file,
)


class DocsDirNotFoundException(Exception):
    pass

def main(args_list: List[str] = sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='pagekey-docgen', description='Generate documentation site from directory.')
    parser.add_argument('docs_dir', metavar='docs_dir', type=str, help='The path to the documents directory')

    args = parser.parse_args(args_list)
    
    if not os.path.exists(args.docs_dir):
        raise DocsDirNotFoundException()
    
    remove_output_directory()
    create_output_directory()

    files = get_files_list(args.docs_dir)

    for cur_file in files:
        render_file(cur_file)
