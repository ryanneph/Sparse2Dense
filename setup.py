from setuptools import setup
from distutils.extension import Extension

setup(
    name = "Sparse2Dense",
    version="1.0.0",
    url = "",
    author = "Ryan Neph",
    author_email = "neph320@gmail.com",
    description = "Convert COO sparse volumes (index:value pairs) to dense volumes",
    packages = ['sparse2dense'],
    install_requires = ['numpy', 'scipy'],
    ext_modules = [Extension('sparserecon', ['sparse2dense/sparserecon.c'])],
)
