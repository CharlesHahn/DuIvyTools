""" 
author : charlie
date : 20220220
"""

from setuptools import setup

INSTALL_REQUIRES = ["matplotlib", "numpy", "scipy", "argparse"]

TEST_REQUIRES = [
    # testing and coverage
    # "pytest",
    # "coverage",
    # "pytest-cov",
    # to be able to run `python setup.py checkdocs`
    # "collective.checkdocs",
    # "pygments",
]


__version__ = "0.4.2"
long_description = ""

with open("README.md", "r") as fo:
    long_description = fo.read()


setup(
    name="DuIvyTools",
    version=__version__,
    author="CharlesHahn",
    author_email="",
    description="A tool for GROMACS results analysis and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CharlesHahn/DuIvyTools",
    download_url="https://github.com/CharlesHahn/DuIvyTools",
    platforms="cross-platform",
    packages=["DuIvyTools"],
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "test": TEST_REQUIRES + INSTALL_REQUIRES,
    },
    package_data={"DuIvyTools":["data/*.data", "data/*.mdp"]},
    exclude_package_data={"DuIvyTools":["test/*"]},
    entry_points={"console_scripts": ["dit = DuIvyTools.DIT:main"]},
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
    ],
)
