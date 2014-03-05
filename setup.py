from distutils.core import setup

setup(
    name='Ash',
    version='0.1.3',
    author='Dang Mai',
    author_email='contact@dangmai.net',
    scripts=['bin/ash.py'],
    url='https://github.com/dangmai/python-ash',
    license='LICENSE.txt',
    description='Thin wrapper for virtualenv for easy environment management',
    long_description=open('README.rst').read()
)
