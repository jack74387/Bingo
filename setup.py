#!/usr/bin/env python3
"""
Setup script for ZMQ Bingo Game
"""

from setuptools import setup, find_packages
import os

# 讀取README文件作為長描述
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# 讀取requirements文件
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="zmq-bingo-game",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A multiplayer Bingo game implemented with ZeroMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/zmq-bingo-game",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment :: Board Games",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bingo-server=zmq_bingo:main",
            "bingo-client=zmq_bingo:main",
        ],
    },
    keywords="bingo game multiplayer zmq zeromq network",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/zmq-bingo-game/issues",
        "Source": "https://github.com/yourusername/zmq-bingo-game",
    },
)