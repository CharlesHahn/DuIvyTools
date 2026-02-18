"""
pytest configuration and shared fixtures for DuIvyTools tests.

Written for DuIvyTools unit testing.

Directory structure:
Tests/
├── conftest.py          # pytest configuration and shared fixtures
├── test_utils.py        # utils module tests
├── parsers/             # FileParser layer tests
├── commands/            # Commands layer tests
├── fixtures/            # Test input data (organized by file type)
│   ├── xvg/
│   ├── xpm/
│   ├── ndx/
│   ├── gro/
│   ├── mdp/
│   ├── dssp/
│   └── dccm/
└── _deprecated/         # Old tests and outputs (to be deleted)
"""

import os
import sys

import pytest

# Add source path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Fixtures base path
FIXTURES_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "fixtures"))


# ============================================================================
# Path fixtures
# ============================================================================

@pytest.fixture
def fixtures_path():
    """Return the base path to fixtures directory."""
    return FIXTURES_PATH


@pytest.fixture
def xvg_fixtures_path():
    """Return the path to xvg fixture files."""
    return os.path.join(FIXTURES_PATH, "xvg")


@pytest.fixture
def xpm_fixtures_path():
    """Return the path to xpm fixture files."""
    return os.path.join(FIXTURES_PATH, "xpm")


@pytest.fixture
def ndx_fixtures_path():
    """Return the path to ndx fixture files."""
    return os.path.join(FIXTURES_PATH, "ndx")


@pytest.fixture
def gro_fixtures_path():
    """Return the path to gro fixture files."""
    return os.path.join(FIXTURES_PATH, "gro")


@pytest.fixture
def mdp_fixtures_path():
    """Return the path to mdp fixture files."""
    return os.path.join(FIXTURES_PATH, "mdp")


@pytest.fixture
def dssp_fixtures_path():
    """Return the path to dssp fixture files."""
    return os.path.join(FIXTURES_PATH, "dssp")


@pytest.fixture
def dccm_fixtures_path():
    """Return the path to dccm fixture files."""
    return os.path.join(FIXTURES_PATH, "dccm")


# ============================================================================
# XVG file fixtures
# ============================================================================

@pytest.fixture
def sample_xvg_file(xvg_fixtures_path):
    """Return path to sample xvg file (gyrate.xvg)."""
    return os.path.join(xvg_fixtures_path, "gyrate.xvg")


@pytest.fixture
def sample_xvg_files(xvg_fixtures_path):
    """Return paths to multiple sample xvg files."""
    return [
        os.path.join(xvg_fixtures_path, "gyrate.xvg"),
        os.path.join(xvg_fixtures_path, "rmsd.xvg"),
    ]


@pytest.fixture
def energy_xvg_files(xvg_fixtures_path):
    """Return paths to energy xvg files for energy_compute tests."""
    return [
        os.path.join(xvg_fixtures_path, "prolig_energy.xvg"),
        os.path.join(xvg_fixtures_path, "pro_energy.xvg"),
        os.path.join(xvg_fixtures_path, "lig_energy.xvg"),
    ]


@pytest.fixture
def bar_xvg_files(xvg_fixtures_path):
    """Return paths to bar xvg files."""
    return [
        os.path.join(xvg_fixtures_path, "bar_0_0.xvg"),
        os.path.join(xvg_fixtures_path, "bar_0_1.xvg"),
        os.path.join(xvg_fixtures_path, "bar_1_0.xvg"),
        os.path.join(xvg_fixtures_path, "bar_1_1.xvg"),
    ]


@pytest.fixture
def rama_xvg_file(xvg_fixtures_path):
    """Return path to Ramachandran xvg file."""
    return os.path.join(xvg_fixtures_path, "rama.xvg")


# ============================================================================
# XPM file fixtures
# ============================================================================

@pytest.fixture
def sample_xpm_continuous(xpm_fixtures_path):
    """Return path to continuous type xpm file (gibbs.xpm)."""
    return os.path.join(xpm_fixtures_path, "gibbs.xpm")


@pytest.fixture
def sample_xpm_discrete(xpm_fixtures_path):
    """Return path to discrete type xpm file (hbond.xpm)."""
    return os.path.join(xpm_fixtures_path, "hbond.xpm")


@pytest.fixture
def sample_xpm_dssp(xpm_fixtures_path):
    """Return path to DSSP xpm file."""
    return os.path.join(xpm_fixtures_path, "dssp.xpm")


# ============================================================================
# NDX file fixtures
# ============================================================================

@pytest.fixture
def sample_ndx_file(ndx_fixtures_path):
    """Return path to sample ndx file."""
    return os.path.join(ndx_fixtures_path, "hbond.ndx")


@pytest.fixture
def sample_index_ndx_file(ndx_fixtures_path):
    """Return path to index ndx file."""
    return os.path.join(ndx_fixtures_path, "index.ndx")


# ============================================================================
# GRO file fixtures
# ============================================================================

@pytest.fixture
def sample_gro_file(gro_fixtures_path):
    """Return path to sample gro file."""
    return os.path.join(gro_fixtures_path, "test.gro")


@pytest.fixture
def sample_pdb_file(gro_fixtures_path):
    """Return path to sample pdb file."""
    return os.path.join(gro_fixtures_path, "test.pdb")


# ============================================================================
# MDP file fixtures
# ============================================================================

@pytest.fixture
def sample_mdp_file(mdp_fixtures_path):
    """Return path to sample mdp file."""
    return os.path.join(mdp_fixtures_path, "test.mdp")


# ============================================================================
# DSSP file fixtures
# ============================================================================

@pytest.fixture
def sample_dssp_file(dssp_fixtures_path):
    """Return path to sample dssp file (gmx2023 format)."""
    return os.path.join(dssp_fixtures_path, "2023dssp.dat")


# ============================================================================
# DCCM file fixtures
# ============================================================================

@pytest.fixture
def sample_covar_file(dccm_fixtures_path):
    """Return path to sample covariance file."""
    return os.path.join(dccm_fixtures_path, "covapic.dat")


# ============================================================================
# Deprecated aliases (for backward compatibility)
# ============================================================================

# These are kept for any tests that might still use the old fixture names
# They will be removed in a future update

@pytest.fixture
def test_data_path():
    """Deprecated: Use fixtures_path instead."""
    return FIXTURES_PATH


@pytest.fixture
def xvg_test_path():
    """Deprecated: Use xvg_fixtures_path instead."""
    return os.path.join(FIXTURES_PATH, "xvg")


@pytest.fixture
def xpm_test_path():
    """Deprecated: Use xpm_fixtures_path instead."""
    return os.path.join(FIXTURES_PATH, "xpm")


@pytest.fixture
def ndx_test_path():
    """Deprecated: Use ndx_fixtures_path instead."""
    return os.path.join(FIXTURES_PATH, "ndx")


@pytest.fixture
def gro_test_path():
    """Deprecated: Use gro_fixtures_path instead."""
    return os.path.join(FIXTURES_PATH, "gro")