# For import all controllers dynamically
from os import listdir
from os.path import abspath, dirname, isfile, join

base_path = abspath(dirname(__file__))
controllers = [
    f.removesuffix(".py")
    for f in listdir(base_path)
    if f != "__init__.py" and isfile(join(base_path, f))
]
__all__ = controllers  # type: ignore
