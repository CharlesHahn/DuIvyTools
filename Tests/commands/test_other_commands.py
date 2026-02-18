"""
Test cases for otherCommands.py module.

Tests for:
- mdp_gen: generate MDP templates
- show_style: generate style files
- find_center: find geometric center
- dccm_ascii: convert covariance to DCCM
- dssp: process DSSP data
- ndx_add: add index groups
- ndx_split: split index groups
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from Commands.otherCommands import mdp_gen, show_style, dccm_ascii, ndx_add


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def test_data_dir():
    """Return test data directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "test_data"))


@pytest.fixture
def find_center_test_dir():
    """Return find_center test directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "find_center_test"))


@pytest.fixture
def ndx_test_dir():
    """Return ndx test directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "ndx_test"))


class MockParameters:
    """Mock Parameters class for testing."""
    
    def __init__(self, **kwargs):
        self.input = kwargs.get('input', None)
        self.output = kwargs.get('output', None)
        self.engine = kwargs.get('engine', 'matplotlib')
        self.mode = kwargs.get('mode', None)
        self.columns = kwargs.get('columns', [])
        self.additional_list = kwargs.get('additional_list', None)
        self.begin = kwargs.get('begin', None)
        self.end = kwargs.get('end', None)
        self.dt = kwargs.get('dt', 1)
        self.xlabel = kwargs.get('xlabel', None)
        self.ylabel = kwargs.get('ylabel', None)
        self.title = kwargs.get('title', None)
        self.z_precision = kwargs.get('z_precision', None)


# ============================================================================
# Test mdp_gen
# ============================================================================

class TestMdpGen:
    """Test cases for mdp_gen command."""
    
    def test_mdp_gen_list_templates(self, capsys):
        """Test listing available MDP templates."""
        parm = MockParameters(output=None)
        cmd = mdp_gen(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert ".mdp" in captured.out
    
    def test_mdp_gen_invalid_template(self):
        """Test error with invalid template name."""
        parm = MockParameters(output='invalid_template.mdp')
        cmd = mdp_gen(parm)
        
        # Should just warn and print list, not exit
        cmd()  # No SystemExit expected
    
    def test_mdp_gen_valid_template(self, tmp_path):
        """Test generating valid MDP template."""
        # Change to temp directory to avoid file conflicts
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            parm = MockParameters(output='nvt.mdp')
            cmd = mdp_gen(parm)
            cmd()
            
            # File should be created (possibly with timestamp suffix)
            mdp_files = [f for f in os.listdir(tmp_path) if f.endswith('.mdp')]
            assert len(mdp_files) > 0
        finally:
            os.chdir(original_cwd)


# ============================================================================
# Test show_style
# ============================================================================

class TestShowStyle:
    """Test cases for show_style command."""
    
    def test_show_style_list_matplotlib(self, capsys):
        """Test listing matplotlib style files."""
        parm = MockParameters(engine='matplotlib', output=None)
        cmd = show_style(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert "matplotlib" in captured.out
        assert ".mplstyle" in captured.out
    
    def test_show_style_list_plotly(self, capsys):
        """Test listing plotly style files."""
        parm = MockParameters(engine='plotly', output=None)
        cmd = show_style(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert "plotly" in captured.out
        assert ".json" in captured.out
    
    def test_show_style_list_gnuplot(self, capsys):
        """Test listing gnuplot style files."""
        parm = MockParameters(engine='gnuplot', output=None)
        cmd = show_style(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert "gnuplot" in captured.out
        assert ".gpstyle" in captured.out
    
    def test_show_style_invalid_file(self):
        """Test error with invalid style file name."""
        parm = MockParameters(output='invalid_style.xyz')
        cmd = show_style(parm)
        
        with pytest.raises(SystemExit):
            cmd()


# ============================================================================
# Test dccm_ascii
# ============================================================================

class TestDccmAscii:
    """Test cases for dccm_ascii command."""
    
    def test_dccm_ascii_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=None, output='dccm.xpm')
        cmd = dccm_ascii(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_dccm_ascii_no_output(self, test_data_dir):
        """Test error when no output file specified."""
        covar_file = os.path.join(test_data_dir, "covapic.dat")
        parm = MockParameters(input=[covar_file], output=None)
        cmd = dccm_ascii(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_dccm_ascii_file_not_exists(self):
        """Test error when input file does not exist."""
        parm = MockParameters(input=['nonexistent.dat'], output='dccm.xpm')
        cmd = dccm_ascii(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_dccm_ascii_basic(self, test_data_dir, tmp_path):
        """Test basic dccm_ascii execution."""
        covar_file = os.path.join(test_data_dir, "covapic.dat")
        output_file = tmp_path / "dccm.xpm"
        
        parm = MockParameters(
            input=[covar_file],
            output=str(output_file),
            z_precision=3
        )
        cmd = dccm_ascii(parm)
        cmd()
        
        assert output_file.exists()


# ============================================================================
# Test ndx_add
# ============================================================================

class TestNdxAdd:
    """Test cases for ndx_add command."""
    
    def test_ndx_add_no_additional_list(self):
        """Test error when no additional_list specified."""
        parm = MockParameters(additional_list=None, columns=[[1, 2, 3]])
        cmd = ndx_add(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_ndx_add_no_columns(self):
        """Test error when no columns specified."""
        parm = MockParameters(additional_list=['TestGroup'], columns=[])
        cmd = ndx_add(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_ndx_add_mismatched_lengths(self):
        """Test error when group names and columns counts don't match."""
        parm = MockParameters(
            additional_list=['Group1', 'Group2'],
            columns=[[1, 2, 3]]  # Only one column list
        )
        cmd = ndx_add(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_ndx_add_basic(self, tmp_path):
        """Test basic ndx_add execution."""
        output_file = tmp_path / "test.ndx"
        parm = MockParameters(
            additional_list=['TestGroup'],
            columns=[[1, 2, 3, 4, 5]],
            output=str(output_file)
        )
        cmd = ndx_add(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_ndx_add_multiple_groups(self, tmp_path):
        """Test ndx_add with multiple groups."""
        output_file = tmp_path / "test.ndx"
        parm = MockParameters(
            additional_list=['Group1', 'Group2'],
            columns=[[1, 2, 3], [4, 5, 6]],
            output=str(output_file)
        )
        cmd = ndx_add(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_ndx_add_to_existing(self, ndx_test_dir, tmp_path):
        """Test adding group to existing NDX file."""
        ndx_file = os.path.join(ndx_test_dir, "hbond.ndx")
        output_file = tmp_path / "output.ndx"
        
        parm = MockParameters(
            input=[ndx_file],
            additional_list=['NewGroup'],
            columns=[[100, 101, 102]],
            output=str(output_file)
        )
        cmd = ndx_add(parm)
        cmd()
        
        assert output_file.exists()
