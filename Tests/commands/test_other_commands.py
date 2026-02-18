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
- ndx_show: show index group names
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from Commands.otherCommands import mdp_gen, show_style, dccm_ascii, ndx_add, find_center, dssp, ndx_split, ndx_show


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def fixtures_path():
    """Return fixtures base directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "fixtures"))


@pytest.fixture
def gro_fixtures_path():
    """Return gro fixtures directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "fixtures", "gro"))


@pytest.fixture
def ndx_fixtures_path():
    """Return ndx fixtures directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "fixtures", "ndx"))


@pytest.fixture
def dssp_fixtures_path():
    """Return dssp fixtures directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "fixtures", "dssp"))


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
    
    def test_dccm_ascii_no_output(self, fixtures_path):
        """Test error when no output file specified."""
        covar_file = os.path.join(fixtures_path, "dccm", "covapic.dat")
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
    
    def test_dccm_ascii_basic(self, fixtures_path, tmp_path):
        """Test basic dccm_ascii execution."""
        covar_file = os.path.join(fixtures_path, "dccm", "covapic.dat")
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
    
    def test_ndx_add_to_existing(self, ndx_fixtures_path, tmp_path):
        """Test adding group to existing NDX file."""
        ndx_file = os.path.join(ndx_fixtures_path, "hbond.ndx")
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


# ============================================================================
# Test find_center
# ============================================================================

class TestFindCenter:
    """Test cases for find_center command."""
    
    def test_find_center_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=None)
        cmd = find_center(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_find_center_no_gro_file(self):
        """Test error when no GRO file in input."""
        parm = MockParameters(input=['test.txt'])
        cmd = find_center(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_find_center_gro_only(self, gro_fixtures_path, capsys):
        """Test find_center with GRO file only (no index)."""
        gro_file = os.path.join(gro_fixtures_path, "test.gro")
        parm = MockParameters(input=[gro_file])
        cmd = find_center(parm)
        cmd()
        
        captured = capsys.readouterr()
        # Should output atom info (ResID Name Atom) when finding nearest atom
        assert "ResID" in captured.out or "SOL" in captured.out or "center" in captured.out.lower()
    
    def test_find_center_with_mode_all_atoms(self, gro_fixtures_path, capsys):
        """Test find_center with AllAtoms mode."""
        gro_file = os.path.join(gro_fixtures_path, "test.gro")
        parm = MockParameters(input=[gro_file], mode="AllAtoms")
        cmd = find_center(parm)
        cmd()
        
        captured = capsys.readouterr()
        # Should output atom info
        assert "ResID" in captured.out or "SOL" in captured.out or "center" in captured.out.lower()
    
    def test_find_center_with_ndx_interactive(self, gro_fixtures_path, ndx_fixtures_path, capsys):
        """Test find_center with index file (interactive input)."""
        gro_file = os.path.join(gro_fixtures_path, "test.gro")
        ndx_file = os.path.join(ndx_fixtures_path, "hbond.ndx")
        
        parm = MockParameters(input=[gro_file, ndx_file])
        cmd = find_center(parm)
        
        # Mock the input() function to return "Protein" (select by name)
        with patch('builtins.input', return_value='Protein'):
            cmd()
        
        captured = capsys.readouterr()
        # Should show group names and output atom info
        assert "Protein" in captured.out or "ResID" in captured.out or "center" in captured.out.lower()
    
    def test_find_center_with_ndx_numeric_selection(self, gro_fixtures_path, ndx_fixtures_path, capsys):
        """Test find_center with numeric group selection."""
        gro_file = os.path.join(gro_fixtures_path, "test.gro")
        ndx_file = os.path.join(ndx_fixtures_path, "hbond.ndx")
        
        parm = MockParameters(input=[gro_file, ndx_file])
        cmd = find_center(parm)
        
        # Mock input to return "0" (first group by index)
        with patch('builtins.input', return_value='0'):
            cmd()
        
        captured = capsys.readouterr()
        # Should have output atom info
        assert "ResID" in captured.out or "selected" in captured.out.lower() or "center" in captured.out.lower()


# ============================================================================
# Test dssp
# ============================================================================

class TestDssp:
    """Test cases for dssp command."""
    
    def test_dssp_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=None)
        cmd = dssp(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_dssp_file_not_exists(self):
        """Test error when input file does not exist."""
        parm = MockParameters(input=['nonexistent.dat'])
        cmd = dssp(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_dssp_basic(self, dssp_fixtures_path, tmp_path):
        """Test basic dssp processing."""
        dssp_file = os.path.join(dssp_fixtures_path, "2023dssp.dat")
        
        # Change to temp directory for output
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            parm = MockParameters(input=[dssp_file])
            cmd = dssp(parm)
            cmd()
            
            # Should generate xpm and xvg files
            files = os.listdir(tmp_path)
            assert any(f.endswith('.xpm') for f in files)
            assert any(f.endswith('.xvg') for f in files)
        finally:
            os.chdir(original_cwd)
    
    def test_dssp_with_output(self, dssp_fixtures_path, tmp_path):
        """Test dssp with custom output name."""
        dssp_file = os.path.join(dssp_fixtures_path, "2023dssp.dat")
        output_file = tmp_path / "custom_dssp.xpm"
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            parm = MockParameters(input=[dssp_file], output=str(output_file))
            cmd = dssp(parm)
            cmd()
            
            files = os.listdir(tmp_path)
            assert any('custom_dssp' in f for f in files)
        finally:
            os.chdir(original_cwd)
    
    def test_dssp_with_labels(self, dssp_fixtures_path, tmp_path):
        """Test dssp with custom labels."""
        dssp_file = os.path.join(dssp_fixtures_path, "2023dssp.dat")
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            parm = MockParameters(
                input=[dssp_file],
                xlabel="Time (ps)",
                ylabel="Residue No.",
                title="Secondary Structure"
            )
            cmd = dssp(parm)
            cmd()
            
            files = os.listdir(tmp_path)
            assert any(f.endswith('.xpm') for f in files)
        finally:
            os.chdir(original_cwd)


# ============================================================================
# Test ndx_split
# ============================================================================

class TestNdxSplit:
    """Test cases for ndx_split command."""
    
    def test_ndx_split_no_additional_list(self):
        """Test error when no additional_list specified."""
        parm = MockParameters(additional_list=None)
        cmd = ndx_split(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_ndx_split_wrong_format(self):
        """Test error with wrong additional_list format."""
        parm = MockParameters(additional_list=['OnlyOneValue'])
        cmd = ndx_split(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_ndx_split_basic(self, tmp_path):
        """Test basic ndx_split execution."""
        # Create a test ndx file with a group that can be split
        ndx_file = tmp_path / "test.ndx"
        ndx_file.write_text("[ TestGroup ]\n1 2 3 4 5 6 7 8 9 10\n")
        output_file = tmp_path / "split.ndx"
        
        parm = MockParameters(
            input=[str(ndx_file)],
            additional_list=['TestGroup', '2'],
            output=str(output_file)
        )
        cmd = ndx_split(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_ndx_split_by_index(self, tmp_path):
        """Test ndx_split by group index instead of name."""
        ndx_file = tmp_path / "test.ndx"
        ndx_file.write_text("[ TestGroup ]\n1 2 3 4 5 6 7 8 9 10\n")
        output_file = tmp_path / "split.ndx"
        
        # Use index '0' to refer to first group
        parm = MockParameters(
            input=[str(ndx_file)],
            additional_list=['0', '2'],
            output=str(output_file)
        )
        cmd = ndx_split(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_ndx_split_unequal_division(self, tmp_path):
        """Test error when cannot equally divide group."""
        ndx_file = tmp_path / "test.ndx"
        ndx_file.write_text("[ TestGroup ]\n1 2 3 4 5 6 7 8 9 10\n")
        output_file = tmp_path / "split.ndx"
        
        # Try to split 10 atoms into 3 groups (10 % 3 != 0)
        parm = MockParameters(
            input=[str(ndx_file)],
            additional_list=['TestGroup', '3'],
            output=str(output_file)
        )
        cmd = ndx_split(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_ndx_split_nonexistent_group(self, tmp_path):
        """Test ndx_split with nonexistent group."""
        ndx_file = tmp_path / "test.ndx"
        ndx_file.write_text("[ TestGroup ]\n1 2 3 4\n")
        
        parm = MockParameters(
            input=[str(ndx_file)],
            additional_list=['NonExistent', '2'],
            output=str(tmp_path / "split.ndx")
        )
        cmd = ndx_split(parm)
        
        # This should fail because the group doesn't exist
        # The ndx parser returns (None, None) for non-existent groups
        # which causes a TypeError when checking len(indexs)
        with pytest.raises((SystemExit, TypeError)):
            cmd()


# ============================================================================
# Test ndx_show
# ============================================================================

class TestNdxShow:
    """Test cases for ndx_show command."""
    
    def test_ndx_show_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=None)
        cmd = ndx_show(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_ndx_show_basic(self, ndx_fixtures_path, capsys):
        """Test basic ndx_show execution."""
        ndx_file = os.path.join(ndx_fixtures_path, "hbond.ndx")
        parm = MockParameters(input=[ndx_file])
        cmd = ndx_show(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert "Protein" in captured.out
        assert "1ZIN" in captured.out
    
    def test_ndx_show_multiple_files(self, ndx_fixtures_path, capsys):
        """Test ndx_show with multiple index files."""
        ndx_file1 = os.path.join(ndx_fixtures_path, "hbond.ndx")
        ndx_file2 = os.path.join(ndx_fixtures_path, "index.ndx")
        
        parm = MockParameters(input=[ndx_file1, ndx_file2])
        cmd = ndx_show(parm)
        cmd()
        
        captured = capsys.readouterr()
        # Should show groups from both files
        assert "Protein" in captured.out
