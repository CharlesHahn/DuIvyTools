""" 
author : charlie
date : 20220220
"""

from setuptools import setup

INSTALL_REQUIRES = ["matplotlib", "numpy", "scipy", "argparse", "cycler"]

TEST_REQUIRES = [
    # testing and coverage
    # "pytest",
    # "coverage",
    # "pytest-cov",
    # to be able to run `python setup.py checkdocs`
    # "collective.checkdocs",
    # "pygments",
]


__version__ = "0.1.0"
long_description = ""

with open("README.md", "r") as fo:
    long_description = fo.read()

with open("GSAT/__init__.py", "r") as fo:
    init = fo.readlines()
for line in init:
    if "__version__" in line:
        __version__ = line.split('"')[-2]

setup(
    name="GMX_Simple_Analysis_Tool",
    version=__version__,
    author="CharlesHahn",
    author_email="",
    description="Some tools for GMX results analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CharlesHahn/GMX_Simple_Analysis_Tool",
    download_url="https://github.com/CharlesHahn/GMX_Simgle_Analysis_Tool/",
    platforms="cross-platform",
    packages=["GMX_Simple_Analysis_Tool"],
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "test": TEST_REQUIRES + INSTALL_REQUIRES,
    },
    entry_points={"console_scripts": ["dit = GSAT.GSAT:main"]},
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GPLv2 License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
    ],
)
