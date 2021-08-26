#!/usr/bin/env python
"""
Setup script.
"""

from setuptools import setup


setup(name = "AEMET",
    version = "1.0.0",
    description = "Consultas AEMET",
    long_description = "Libreria en python para consultar los datos de la AEMET",
    author = "Adria Ariste",
    author_email = 'adria@ariste.info',
    url = "https://github.com/aariste/AEMET-Python",
    download_url = "https://github.com/aariste/AEMET-Python/archive/master.zip",
    platforms = ['any'],

    license = "",

    package_dir = {'': 'src/'},
    packages = [''],
)

