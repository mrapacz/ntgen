import os

import setuptools
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ntgen",
    version="0.1.0",
    description=("ntgen: generate your NamedTuple definition"),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Maciej Rapacz",
    author_email="mrapacz+ntgen@protonmail.com",
    url="https://github.com/mrapacz/ntgen",
    license="MIT",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    entry_points={"console_scripts": ["ntgen=ntgen.__main__:console_entry"]},
    install_requires=["python_version >= '3.7'", "pyannotate == 1.2.0", "typed-argument-parser == 1.4",],
)
