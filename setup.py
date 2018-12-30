#!/usr/bin/env python


from setuptools import setup

meta = {}
exec(open('./sg/version.py').read(), meta)
meta['long_description'] = open('./README.md').read()

setup(
    name='sg.py',
    version=meta['__VERSION__'],
    description='Simple static site generator.',
    long_description=meta['long_description'],
    long_description_content_type='text/markdown',
    keywords='markdown site generator cli',
    author='Bastian Venthur',
    author_email='mail@venthur.de',
    url='https://github.com/venthur/sg',
    python_requires='>=3',
    install_requires=[
        'markdown',
    ],
    extras_require={
      'dev': [
          'pytest',
          'pytest-cov',
          'flake8',
      ]
    },
    packages=['sg'],
    entry_points={
        'console_scripts': [
            'sg = sg.__main__:main'
        ]
    },
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
