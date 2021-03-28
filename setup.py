#!/usr/bin/env python


from setuptools import setup

meta = {}
exec(open('./blag/version.py').read(), meta)
meta['long_description'] = open('./README.md').read()

setup(
    name='blag',
    version=meta['__VERSION__'],
    description='blog-aware, static site generator',
    long_description=meta['long_description'],
    long_description_content_type='text/markdown',
    keywords='markdown blag blog static site generator cli',
    author='Bastian Venthur',
    author_email='mail@venthur.de',
    url='https://github.com/venthur/blag',
    project_urls={
        'Documentation': 'https://blag.readthedocs.io/',
        'Source': 'https://github.com/venthur/blag',
    },
    python_requires='>=3.8',
    package_data={
        'blag': ['templates/*'],
    },
    install_requires=[
        'markdown',
        'feedgenerator',
        'jinja2',
        'pygments',
    ],
    packages=['blag'],
    entry_points={
        'console_scripts': [
            'blag = blag.blag:main'
        ]
    },
    license='MIT',
)
