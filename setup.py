# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# This call to setup() does all the work
setup(
    name="job-hunting",
    version="0.2.17",
    description="Package that automate selection and subscription of jobs",
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding="utf-8").read(),
    url="https://job-hunting.readthedocs.io/",
    author="Jeferson/MxJeff",
    author_email="mx.jeferson.10@hotmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=['jobhunting', 'jobhunting.Models', 'jobhunting.utils', 'jobhunting.controllers', 'jobhunting.const'],
    include_package_data=True,
    install_requires=["selenium", 'python-dotenv', "scrapper-boilerplate"]
)
