#!/usr/bin/env python3

from setuptools import setup

def get_version():
    with open("hyper_prompt/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hyper-prompt",
    version=get_version(),
    description="Highly Customize-able prompt for your shell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Savio Fernandes",
    author_email="savio@saviof.com",
    license="MIT",
    url="https://github.com/artbycrunk/hyper-prompt",
    download_url = 'https://github.com/artbycrunk/hyper-prompt/archive/1.1.0.tar.gz',
    keywords = ['prompts', 'shell', 'bash', "zsh"],
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
