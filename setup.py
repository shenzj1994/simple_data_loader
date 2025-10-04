"""
Setup script for simple_data_loader package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="simple-data-loader",
    version="1.0.0",
    author="Zhongjie Shen",
    author_email="askme@zshen.ca",
    description="A simple Python package for loading data from CSV and XLSX files",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shenzj1994/simple-data-loader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    keywords="data loading, csv, xlsx, pandas, data analysis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/simple-data-loader/issues",
        "Source": "https://github.com/yourusername/simple-data-loader",
        "Documentation": "https://github.com/yourusername/simple-data-loader#readme",
    },
)
