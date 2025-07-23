#!/usr/bin/env python3
"""
Setup script for assignment_backend package.
Alternative to Poetry for environments that don't have it installed.
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="assignment-backend",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python program to fetch research papers from PubMed and identify pharmaceutical/biotech company affiliations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Text Processing :: Markup :: XML",
    ],
    python_requires=">=3.8",
    install_requires=[req for req in requirements if not req.startswith("pytest") and not req.startswith("black") and not req.startswith("flake8") and not req.startswith("mypy")],
    extras_require={
        "dev": ["pytest>=7.4.3", "pytest-cov>=4.1.0", "black>=23.11.0", "flake8>=6.1.0", "mypy>=1.7.1"]
    },
    entry_points={
        "console_scripts": [
            "get-papers-list=assignment_backend.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 