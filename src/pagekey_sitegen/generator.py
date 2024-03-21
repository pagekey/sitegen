import fileinput
import os

from enum import Enum
import shutil

from jinja2 import Template
from pydantic import BaseModel
import yaml

import pagekey_sitegen


class TemplateName(Enum):
    SPHINX = "sphinx"
    NEXT = "next"


class SiteConfig(BaseModel):

    @staticmethod
    def from_path(path: str):
        config_path = os.path.join(path, 'site.yaml')
        with open(config_path, 'r') as f:
            text_raw = f.read()
        parsed_config = yaml.safe_load(text_raw)
        site_config = SiteConfig(**parsed_config)
        return site_config

    project: str
    copyright: str
    author: str
    release: str
    package: str
    template: TemplateName


class SiteGenerator:
    def __init__(self, path: str):
        self.path = path
        self.config = SiteConfig.from_path(path)
        package_root = os.path.dirname(pagekey_sitegen.__file__)
        self.templates_dir = os.path.join(package_root, 'templates', self.config.template.value)
    def generate(self):
        if os.path.exists('build'):
            shutil.rmtree('build')
        os.makedirs('build')
        # Render templates
        template_files = get_files_list(self.templates_dir)
        for template in template_files:
            self.render_template(os.path.abspath(template))

        # Render source files
        source_files = get_files_list(self.path)
        for cur_file in source_files:
            self.render_source(cur_file)

        # Call whatever executable to generate the site
        os.chdir(f'build/{self.config.template.value}')
        if self.config.template == TemplateName.SPHINX:
            os.system('make html')
            # Move the generated site to the top level of the build directory
            shutil.move('_build/html', '..')
        elif self.config.template == TemplateName.NEXT:
            print("TODO generate next static export here")
    def render_template(self, filename: str):
        src_path = os.path.join(self.templates_dir, self.config.template.value, filename)
        dest_path = os.path.join('build', self.config.template.value, os.path.basename(filename))
        if not os.path.exists(f'build/{self.config.template.value}'):
            os.makedirs(f'build/{self.config.template.value}')
        file_contents = get_file_as_string(src_path)
        template = Template(file_contents)
        output_string = template.render(config=self.config)
        write_string_to_file(dest_path, output_string)
    def render_source(self, filename: str):
        dirname = os.path.dirname(filename)
        if len(dirname) < 1:
            # File is at the top-level of the repo - keep it simple
            dest_dir_relpath = os.path.join('build', self.config.template.value)
        else:
            # Handle nested files
            src_dir_relpath = os.path.relpath(os.path.dirname(filename))
            dest_dir_relpath = os.path.join('build', self.config.template.value, src_dir_relpath)
        # Create directories containing this file if not exists
        os.makedirs(dest_dir_relpath, exist_ok=True)
        # Copy the file over
        # TODO / NOTE: eventually this will do templating too
        shutil.copy(filename, dest_dir_relpath)
        if self.config.template == TemplateName.SPHINX:
            # Replace mermaid code blocks in md with sphinx-compatible ones
            dest_file = os.path.join(dest_dir_relpath, os.path.basename(filename))
            if dest_file.endswith('.md'):
                with fileinput.FileInput(dest_file, inplace=True, backup='.bak') as file:
                    for line in file:
                        print(line.replace('```mermaid', '```{mermaid}'), end='')


def get_files_list(path: str):
    """Walk directory and get all files recursively.
    
    Args:
      path: Directory path to walk.
    """
    result = []
    for root, dirs, files in os.walk(path):
        for cur_file in files:
            cur_file_path = os.path.relpath(os.path.join(root, cur_file))
            result.append(cur_file_path)
    return result


def get_file_as_string(filename: str):
    with open(filename, 'r') as file:
        return file.read()


def write_string_to_file(filename: str, data: str):
    with open(filename, 'w') as file:
        file.write(data)
