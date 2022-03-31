from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("marked_odds_opt.pyx", compiler_directives={"language_level": 3}))
