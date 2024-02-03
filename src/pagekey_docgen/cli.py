import argparse
import os
import sys
from typing import List


class DocsDirNotFoundException(Exception):
    pass

def main(args_list: List[str] = sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='pagekey-docgen', description='Generate documentation site from directory.')
    parser.add_argument('docs_dir', metavar='docs_dir', type=str, help='The path to the documents directory')

    args = parser.parse_args(args_list)
    
    if not os.path.exists(args.docs_dir):
        raise DocsDirNotFoundException()
