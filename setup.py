from os import path
from setuptools import setup

import cuaima


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    long_description = f.read()

install_requires = [
    'pythonosc~=1.7.4',
]

setup(
    name='cuaima',
    version=cuaima.__version__,
    author='jxpp',
    author_email='jxpp@chigui.re',
    description='A live coding DSL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    url='https://github.com/jxpp/cuaima',
    test_suite='tests',
)
