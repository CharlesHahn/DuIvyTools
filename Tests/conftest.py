"""
pytest configuration and shared fixtures for DuIvyTools tests.

Written for DuIvyTools unit testing.
"""

import os
import sys

import pytest

# Add source path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Test data path
TEST_DATA_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "test_data"))


@pytest.fixture
def test_data_path():
    """Return the path to test data directory."""
    return TEST_DATA_PATH


@pytest.fixture
def xvg_test_path():
    """Return the path to xvg test files."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "xvg_test"))


@pytest.fixture
def xpm_test_path():
    """Return the path to xpm test files."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "xpm_test"))


@pytest.fixture
def ndx_test_path():
    """Return the path to ndx test files."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "ndx_test"))


@pytest.fixture
def gro_test_path():
    """Return the path to gro test files."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "find_center_test"))


@pytest.fixture
def sample_xvg_file(xvg_test_path):
    """Return path to sample xvg file (gyrate.xvg)."""
    return os.path.join(xvg_test_path, "gyrate.xvg")


@pytest.fixture
def sample_xpm_continuous(xpm_test_path):
    """Return path to continuous type xpm file (gibbs.xpm)."""
    return os.path.join(xpm_test_path, "gibbs.xpm")


@pytest.fixture
def sample_xpm_discrete(xpm_test_path):
    """Return path to discrete type xpm file (hbond.xpm)."""
    return os.path.join(xpm_test_path, "hbond.xpm")


@pytest.fixture
def sample_ndx_file(ndx_test_path):
    """Return path to sample ndx file."""
    return os.path.join(ndx_test_path, "hbond.ndx")


@pytest.fixture
def sample_gro_file(gro_test_path):
    """Return path to sample gro file."""
    return os.path.join(gro_test_path, "test.gro")


@pytest.fixture
def sample_mdp_file(test_data_path):
    """Return path to sample mdp file."""
    return os.path.join(test_data_path, "test.mdp")


@pytest.fixture
def sample_pdb_file(test_data_path):
    """Return path to sample pdb file."""
    return os.path.join(test_data_path, "test.pdb")


@pytest.fixture
def sample_dssp_file(test_data_path):
    """Return path to sample dssp file (gmx2023 format)."""
    return os.path.join(test_data_path, "2023dssp.dat")


@pytest.fixture
def sample_covar_file(test_data_path):
    """Return path to sample covariance file."""
    return os.path.join(test_data_path, "covapic.dat")
