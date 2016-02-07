#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import fwdform

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = fwdform.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

long_description = open('README.rst').read()

setup(
    name='django-fwdform',
    version=version,
    description="""Simple and painless form processing for static sites.""",
    long_description=long_description,
    author='Mishbah Razzaque',
    author_email='mishbahx@gmail.com',
    url='https://github.com/mishbahr/django-fwdform',
    packages=[
        'fwdform',
    ],
    include_package_data=True,
    install_requires=[
        'django-appconf',
        'requests>=1.0',
        'hashids>=1.0',
        'django-cors-headers>=1.0',
    ],
    license='BSD',
    zip_safe=False,
    keywords='django-fwdform',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
