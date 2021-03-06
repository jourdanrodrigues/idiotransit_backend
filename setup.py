# from codecs import open
from os import path

from setuptools import setup, find_packages

project_path = path.abspath(path.dirname(__file__))

# Get the long description from the README file (no README yet)
# with open(path.join(project_path, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()
long_description = ''

setup(
    name='IdioTransit',
    version='0.0.1',
    description='Share the idiocy of drivers.',
    long_description=long_description,
    author='Jourdan Rodrigues',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Other Audience',
        'Natural Language :: Portuguese (Brazilian)',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.11',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
    keywords='rating transit driving quality',
    packages=find_packages(),
    install_requires=[
        'Django==1.11.4',
    ],
    extras_require={
        'test': ['coverage']
    }
)
