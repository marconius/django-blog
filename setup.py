#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '1.0.0'

setup(
    name = "django-blog",
    version = VERSION,

    packages = find_packages(),
    install_requires = ['django', 'django-summernote==0.5.13'],
    include_package_data= True,
    zip_safe = False,

    # metadata
    author = 'Marco Gagliano',
    author_email = 'marco@cuthemustard.com',
    description = 'A blog for Django for quick installing',
    url = 'https://github.com/marconius/django-blog',
    license = 'BSD',
    keywords = 'blog django',
)
