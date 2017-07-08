import os

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))


def file_path(package, file_name):
    """
    Return absolute path for given file in certain project package.
    """
    directory = os.path.join(ROOT_DIR, *package.split('.'))
    return os.path.join(directory, file_name)
