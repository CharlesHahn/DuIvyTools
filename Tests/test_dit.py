"""
Test cases for DIT.py module (CLI entry point).

Tests for:
- DIT class initialization
- DIT.run() with various arguments
- main() function
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from DIT import DIT, main


# ============================================================================
# Test DIT class initialization
# ============================================================================

class TestDITInit:
    """Test cases for DIT class initialization."""
    
    def test_dit_init_creates_classes_dict(self):
        """Test that DIT.__init__ creates classes dictionary."""
        dit = DIT()
        assert hasattr(dit, 'classes')
        assert isinstance(dit.classes, dict)
    
    def test_dit_init_has_expected_commands(self):
        """Test that DIT has all expected commands in cmds list."""
        dit = DIT()
        expected_cmds = [
            "xvg_show", "xvg_compare", "xvg_ave", "xvg_energy_compute",
            "xvg_combine", "xvg_show_distribution", "xvg_show_scatter",
            "xvg_show_stack", "xvg_box_compare", "xvg_ave_bar", "xvg_rama",
            "xpm_show", "xpm2csv", "xpm2dat", "xpm_diff", "xpm_merge",
            "mdp_gen", "show_style", "find_center", "dccm_ascii", "dssp",
            "ndx_add", "ndx_split", "ndx_show",
        ]
        assert dit.cmds == expected_cmds
    
    def test_dit_init_has_cmds_infos(self):
        """Test that DIT has cmds_infos string."""
        dit = DIT()
        assert hasattr(dit, 'cmds_infos')
        assert isinstance(dit.cmds_infos, str)
        assert "xvg_show" in dit.cmds_infos
        assert "xpm_show" in dit.cmds_infos
    
    def test_dit_init_has_welcome_info(self):
        """Test that DIT has welcome_info string."""
        dit = DIT()
        assert hasattr(dit, 'welcome_info')
        assert isinstance(dit.welcome_info, str)
        assert "DuIvyTools" in dit.welcome_info
    
    def test_dit_classes_contains_commands(self):
        """Test that classes dict contains the command classes."""
        dit = DIT()
        for cmd in dit.cmds:
            assert cmd in dit.classes, f"Command {cmd} not found in classes"
            assert callable(dit.classes[cmd]), f"Command {cmd} is not callable"


# ============================================================================
# Test DIT.run() method
# ============================================================================

class TestDITRun:
    """Test cases for DIT.run() method."""
    
    def test_run_no_args_shows_welcome(self, capsys):
        """Test that run() with no args shows welcome info and exits."""
        dit = DIT()
        
        with patch.object(sys, 'argv', ['dit']):
            with pytest.raises(SystemExit):
                dit.run()
        
        captured = capsys.readouterr()
        assert "DuIvyTools" in captured.out
    
    def test_run_help_for_valid_command(self, capsys):
        """Test that run() with -h for valid command shows help."""
        dit = DIT()
        
        with patch.object(sys, 'argv', ['dit', 'xvg_show', '-h']):
            with pytest.raises(SystemExit):
                dit.run()
        
        captured = capsys.readouterr()
        assert "command: xvg_show" in captured.out
    
    def test_run_help_for_invalid_command(self):
        """Test that run() with -h for invalid command shows error."""
        dit = DIT()
        
        with patch.object(sys, 'argv', ['dit', 'invalid_cmd', '-h']):
            with pytest.raises(SystemExit):
                dit.run()
    
    def test_run_invalid_command_shows_error(self):
        """Test that run() with invalid command shows error."""
        dit = DIT()
        
        # Need to mock Parameters to return invalid command
        with patch('DIT.Parameters') as MockParameters:
            mock_parm = MagicMock()
            mock_parm.cmd = 'invalid_command_xyz'
            MockParameters.return_value = mock_parm
            
            with pytest.raises(SystemExit):
                dit.run()
    
    def test_run_valid_command_executes(self, fixtures_path):
        """Test that run() with valid command executes successfully."""
        dit = DIT()
        xvg_file = os.path.join(fixtures_path, "xvg", "rmsd.xvg")
        
        # Mock the command execution to avoid actual plotting
        with patch('DIT.Parameters') as MockParameters:
            mock_parm = MagicMock()
            mock_parm.cmd = 'xvg_ave'
            mock_parm.input = [xvg_file]
            mock_parm.output = None
            mock_parm.begin = None
            mock_parm.end = None
            mock_parm.dt = 1
            MockParameters.return_value = mock_parm
            
            # The command should execute without error
            dit.run()


# ============================================================================
# Test main() function
# ============================================================================

class TestMainFunction:
    """Test cases for main() function."""
    
    def test_main_with_no_args(self, capsys):
        """Test main() with no arguments."""
        with patch.object(sys, 'argv', ['dit']):
            with pytest.raises(SystemExit):
                main()
        
        captured = capsys.readouterr()
        assert "DuIvyTools" in captured.out
    
    def test_main_calls_dit_run(self):
        """Test that main() creates DIT instance."""
        with patch.object(sys, 'argv', ['dit']):
            with pytest.raises(SystemExit):
                main()


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def fixtures_path():
    """Return fixtures base directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "fixtures"))
