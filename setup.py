#!/usr/bin/env python3

from setuptools import setup

setup(
    name="hyper-prompt",
    version="1.1.0",
    description="Highly Customize-able prompt for your shell",
    author="Savio Fernandes",
    author_email="savio@saviof.com",
    license="MIT",
    url="https://github.com/artbycrunk/hyper-prompt",
    download_url = 'https://github.com/artbycrunk/hyper-prompt/archive/1.1.0.tar.gz',
    keywords = ['PROMPTS', 'SHELL', 'BASH', "ZSH"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    packages=[
        "hyper_prompt",
        "hyper_prompt.segments",
        "hyper_prompt.themes",
    ],
    install_requires=[
        "argparse",
    ],
    extras_require={
        'develop':[
            'pytest',
            'pytest-cov'
        ]
    },
    entry_points="""
    [console_scripts]
    hyper-prompt=hyper_prompt.cli:main
    """,
)
