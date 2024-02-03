import os
import shutil


def get_files_list(path: str):
    """Walk directory and get all files recursively.
    
    Args:
      path: Directory path to walk.
    """
    result = []
    for root, dirs, files in os.walk(path):
        result.extend(files)
    return result

def create_output_directory():
    """Create output directory to copy the generated site into."""
    os.makedirs('build')

def remove_output_directory():
    """Remove the output directory recursively.
    
    Clean the project.
    """
    if os.path.exists('build'):
        shutil.rmtree('build')

def render_file(path: str):
    """Render a docs file to the final HTML site.

    Args:
      path: Path to file to be rendered.
    """
    dirname = os.path.dirname(path)
    if len(dirname) < 1:
        # File is at the top-level of the repo - keep it simple
        dest_dir_relpath = 'build'
    else:
        # Handle nested files
        src_dir_relpath = os.path.relpath(os.path.dirname(path))
        dest_dir_relpath = os.path.join('build', src_dir_relpath)
    # Create directories containing this file if not exists
    os.makedirs(dest_dir_relpath, exist_ok=True)
    # Copy the file over
    # TODO / NOTE: eventually this will do templating too
    shutil.copy(path, dest_dir_relpath)
