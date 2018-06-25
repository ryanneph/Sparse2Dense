from setuptools import setup
from Cython.Build import cythonize

setup(
    name = "Sparse2Dense",
    version="1.0.0",
    url = "",
    author = "Ryan Neph",
    author_email = "neph320@gmail.com",
    description = "Convert COO sparse volumes (index:value pairs) to dense volumes",
    packages = ['sparse2dense'],
    install_requires = ['Cython >= 0.28.2', 'numpy >= 1.14.2', 'scipy >= 1.0.1'],
    ext_modules = cythonize("sparse2dense/sparserecon.pyx"),
)
