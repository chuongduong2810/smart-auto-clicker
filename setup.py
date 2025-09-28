#!/usr/bin/env python3
"""
Setup script for Smart Auto Clicker
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="smart-auto-clicker",
    version="1.0.0",
    description="An intelligent auto-clicking application with recording and playback capabilities",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Smart Auto Clicker Team",
    author_email="",
    url="https://github.com/chuongduong2810/smart-auto-clicker",
    py_modules=["smart_auto_clicker"],
    install_requires=read_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "smart-auto-clicker=smart_auto_clicker:main",
        ],
    },
    keywords="auto-clicker automation gui mouse click recording",
)