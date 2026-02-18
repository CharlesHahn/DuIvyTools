"""
Test cases for utils.py module.

Tests for:
- log class: debug, info, warn, error, critical methods
- Parameters class: argument parsing, column parsing, parameter checking
- Command class: sel_parm, get_parm, deal_latex methods
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import logging

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from utils import log, Parameters
from Commands.Commands import Command


class TestLog:
    """Test cases for log class."""

    def test_log_inheritance(self):
        """Test that log class can be inherited."""
        class TestClass(log):
            pass
        
        tc = TestClass()
        assert hasattr(tc, 'debug')
        assert hasattr(tc, 'info')
        assert hasattr(tc, 'warn')
        assert hasattr(tc, 'error')
        assert hasattr(tc, 'critical')

    def test_debug_output(self, capsys):
        """Test debug method outputs correct message."""
        class TestLog(log):
            pass
        
        tc = TestLog()
        tc.debug("test debug message")
        captured = capsys.readouterr()
        # Debug messages may not show if logging level is INFO
        # Just verify the method doesn't crash

    def test_info_output(self, caplog):
        """Test info method outputs correct message."""
        class TestLog(log):
            pass
        
        tc = TestLog()
        with caplog.at_level(logging.INFO):
            tc.info("test info message")
        # Check that the message was logged (message field contains formatted output)
        assert any("test info message" in record.message for record in caplog.records)

    def test_warn_output(self, caplog):
        """Test warn method outputs correct message."""
        class TestLog(log):
            pass
        
        tc = TestLog()
        with caplog.at_level(logging.WARNING):
            tc.warn("test warning message")
        # Check that the message was logged (message field contains formatted output)
        assert any("test warning message" in record.message for record in caplog.records)

    def test_error_exits(self):
        """Test error method calls sys.exit."""
        class TestLog(log):
            pass
        
        tc = TestLog()
        with pytest.raises(SystemExit):
            tc.error("test error message")

    def test_critical_exits(self):
        """Test critical method calls sys.exit."""
        class TestLog(log):
            pass
        
        tc = TestLog()
        with pytest.raises(SystemExit):
            tc.critical("test critical message")


class TestParameters:
    """Test cases for Parameters class."""

    def test_parameters_basic_cmd(self):
        """Test basic command parsing."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.cmd == 'xvg_show'

    def test_parameters_input_file(self):
        """Test input file parameter."""
        with patch('sys.argv', ['dit', 'xvg_show', '-f', 'test.xvg']):
            parm = Parameters()
            assert parm.input == ['test.xvg']

    def test_parameters_multiple_input_files(self):
        """Test multiple input files."""
        with patch('sys.argv', ['dit', 'xvg_compare', '-f', 'file1.xvg', 'file2.xvg']):
            parm = Parameters()
            assert parm.input == ['file1.xvg', 'file2.xvg']

    def test_parameters_output_file(self):
        """Test output file parameter."""
        with patch('sys.argv', ['dit', 'xvg_show', '-o', 'output.png']):
            parm = Parameters()
            assert parm.output == 'output.png'

    def test_parameters_noshow_flag(self):
        """Test noshow flag."""
        with patch('sys.argv', ['dit', 'xvg_show', '-ns']):
            parm = Parameters()
            assert parm.noshow == True

    def test_parameters_noshow_default(self):
        """Test noshow default value."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.noshow == False

    def test_parameters_begin_end(self):
        """Test begin and end parameters."""
        with patch('sys.argv', ['dit', 'xvg_show', '-b', '100', '-e', '200']):
            parm = Parameters()
            assert parm.begin == 100
            assert parm.end == 200

    def test_parameters_dt_default(self):
        """Test dt default value."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.dt == 1

    def test_parameters_xlabel_ylabel(self):
        """Test xlabel and ylabel parameters."""
        with patch('sys.argv', ['dit', 'xvg_show', '-x', 'Time', '-y', 'RMSD']):
            parm = Parameters()
            assert parm.xlabel == 'Time'
            assert parm.ylabel == 'RMSD'

    def test_parameters_engine_default(self):
        """Test engine default value."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.engine == 'matplotlib'

    def test_parameters_engine_plotly(self):
        """Test engine selection."""
        with patch('sys.argv', ['dit', 'xvg_show', '-eg', 'plotly']):
            parm = Parameters()
            assert parm.engine == 'plotly'

    def test_parameters_shrink_default(self):
        """Test shrink default values."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.xshrink == 1.0
            assert parm.yshrink == 1.0
            assert parm.zshrink == 1.0

    def test_parameters_plus_default(self):
        """Test plus default values."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.xplus == 0.0
            assert parm.yplus == 0.0
            assert parm.zplus == 0.0

    def test_parameters_windowsize_default(self):
        """Test windowsize default value."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.windowsize == 50

    def test_parameters_confidence_default(self):
        """Test confidence default value."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.confidence == 0.95

    def test_parameters_showMV_default(self):
        """Test showMV default value."""
        with patch('sys.argv', ['dit', 'xvg_show']):
            parm = Parameters()
            assert parm.showMV == ''

    def test_parameters_showMV_origin(self):
        """Test showMV origin flag."""
        with patch('sys.argv', ['dit', 'xvg_show', '-smv']):
            parm = Parameters()
            assert parm.showMV == 'origin'

    def test_parameters_showMV_CI(self):
        """Test showMV CI flag."""
        with patch('sys.argv', ['dit', 'xvg_show', '-smv', 'CI']):
            parm = Parameters()
            assert parm.showMV == 'CI'

    def test_parameters_legend_location(self):
        """Test legend_location parameter."""
        with patch('sys.argv', ['dit', 'xvg_show', '--legend_location', 'outside']):
            parm = Parameters()
            assert parm.legend_location == 'outside'

    def test_parameters_columns_single(self):
        """Test single column selection."""
        with patch('sys.argv', ['dit', 'xvg_compare', '-c', '1']):
            parm = Parameters()
            assert parm.columns == [[1]]

    def test_parameters_columns_range(self):
        """Test column range selection."""
        with patch('sys.argv', ['dit', 'xvg_compare', '-c', '1-5']):
            parm = Parameters()
            assert parm.columns == [[1, 2, 3, 4]]

    def test_parameters_columns_range_with_step(self):
        """Test column range with step selection."""
        with patch('sys.argv', ['dit', 'xvg_compare', '-c', '1-10-2']):
            parm = Parameters()
            assert parm.columns == [[1, 3, 5, 7, 9]]

    def test_parameters_columns_multiple(self):
        """Test multiple column selections."""
        with patch('sys.argv', ['dit', 'xvg_compare', '-c', '1', '2-5']):
            parm = Parameters()
            assert parm.columns == [[1], [2, 3, 4]]

    def test_parameters_xmin_xmax(self):
        """Test xmin and xmax parameters."""
        with patch('sys.argv', ['dit', 'xvg_show', '-xmin', '0.0', '-xmax', '100.0']):
            parm = Parameters()
            assert parm.xmin == 0.0
            assert parm.xmax == 100.0

    def test_parameters_precision(self):
        """Test precision parameters."""
        with patch('sys.argv', ['dit', 'xvg_show', '--x_precision', '2', '--y_precision', '3']):
            parm = Parameters()
            assert parm.x_precision == 2
            assert parm.y_precision == 3

    def test_parameters_mode(self):
        """Test mode parameter."""
        with patch('sys.argv', ['dit', 'xpm_show', '-m', '3d']):
            parm = Parameters()
            assert parm.mode == '3d'

    def test_parameters_colormap(self):
        """Test colormap parameter."""
        with patch('sys.argv', ['dit', 'xpm_show', '-cmap', 'viridis']):
            parm = Parameters()
            assert parm.colormap == 'viridis'

    def test_parameters_interpolation(self):
        """Test interpolation parameter."""
        with patch('sys.argv', ['dit', 'xpm_show', '-ip', 'linear']):
            parm = Parameters()
            assert parm.interpolation == 'linear'

    def test_parameters_interpolation_fold_default(self):
        """Test interpolation_fold default value."""
        with patch('sys.argv', ['dit', 'xpm_show']):
            parm = Parameters()
            assert parm.interpolation_fold == 10

    def test_parameters_negative_precision_error(self):
        """Test that negative precision raises error."""
        with patch('sys.argv', ['dit', 'xvg_show', '--x_precision', '-1']):
            with pytest.raises(SystemExit):
                Parameters()


class TestCommand:
    """Test cases for Command class."""

    def test_command_sel_parm_first_not_none(self):
        """Test sel_parm returns first non-None value."""
        cmd = Command()
        result = cmd.sel_parm(None, "value", "other")
        assert result == "value"

    def test_command_sel_parm_all_none(self):
        """Test sel_parm returns first item when all None."""
        cmd = Command()
        result = cmd.sel_parm(None, None)
        assert result is None

    def test_command_sel_parm_single_arg(self):
        """Test sel_parm with single argument."""
        cmd = Command()
        result = cmd.sel_parm("value")
        assert result == "value"

    def test_command_sel_parm_empty_raises(self):
        """Test sel_parm raises with no arguments."""
        cmd = Command()
        with pytest.raises(SystemExit):
            cmd.sel_parm()

    def test_command_deal_latex_subscript(self):
        """Test deal_latex with subscript."""
        cmd = Command()
        result = cmd.deal_latex("Rg\\sX\\N")
        assert "_{" in result
        assert "}" in result
        assert "$" in result

    def test_command_deal_latex_superscript(self):
        """Test deal_latex with superscript."""
        cmd = Command()
        result = cmd.deal_latex("E\\S2\\N")
        assert "^{" in result
        assert "}" in result

    def test_command_deal_latex_with_dollar(self):
        """Test deal_latex with dollar sign."""
        cmd = Command()
        result = cmd.deal_latex("x^2", with_dollar=True)
        assert result == "$x^2$"

    def test_command_deal_latex_without_dollar(self):
        """Test deal_latex without dollar sign."""
        cmd = Command()
        result = cmd.deal_latex("x^2", with_dollar=False)
        assert result == "x^2"
        assert "$" not in result

    def test_command_deal_latex_ignore_slash(self):
        """Test deal_latex with ignore_slash."""
        cmd = Command()
        result = cmd.deal_latex("path\\file", ignore_slash=True)
        assert "\\" not in result
        assert "/" in result

    def test_command_deal_latex_no_latex(self):
        """Test deal_latex with no latex content."""
        cmd = Command()
        result = cmd.deal_latex("plain text")
        assert result == "plain text"

    def test_command_deal_latex_combined(self):
        """Test deal_latex with combined subscripts and superscripts."""
        cmd = Command()
        result = cmd.deal_latex("Rg\\sX\\N^2")
        assert "_{" in result
        assert "^{" in result or "^2" in result

    def test_command_check_output_exist_new_file(self, tmp_path):
        """Test check_output_exist for non-existing file."""
        cmd = Command()
        output = os.path.join(tmp_path, "new_file.xvg")
        result = cmd.check_output_exist(output)
        assert result == output

    def test_command_check_output_exist_existing_file(self, tmp_path):
        """Test check_output_exist for existing file adds timestamp."""
        cmd = Command()
        # Create existing file
        existing = os.path.join(tmp_path, "existing.xvg")
        with open(existing, 'w') as f:
            f.write("test")
        
        result = cmd.check_output_exist(existing)
        # Should have timestamp appended
        assert "existing_" in result
        assert result.endswith(".xvg")
        assert result != existing


class TestCommandGetParm:
    """Test cases for Command.get_parm method."""

    def test_get_parm_from_parm_dict(self):
        """Test get_parm retrieves from parm first."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.__dict__ = {'xlabel': 'Time'}
        cmd.file = MagicMock()
        cmd.file.__dict__ = {'xlabel': 'X-axis'}
        
        result = cmd.get_parm('xlabel')
        assert result == 'Time'

    def test_get_parm_from_file_dict(self):
        """Test get_parm retrieves from file when parm is None."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.__dict__ = {'xlabel': None}
        cmd.file = MagicMock()
        cmd.file.__dict__ = {'xlabel': 'X-axis'}
        
        result = cmd.get_parm('xlabel')
        assert result == 'X-axis'

    def test_get_parm_returns_none_when_not_found(self):
        """Test get_parm returns None when key not found."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.__dict__ = {}
        cmd.file = MagicMock()
        cmd.file.__dict__ = {}
        
        result = cmd.get_parm('nonexistent')
        assert result is None


class TestCommandRemoveLatex:
    """Test cases for Command.remove_latex method."""

    def test_remove_latex_xvg_matplotlib(self):
        """Test remove_latex for XVG with matplotlib engine."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.engine = 'matplotlib'
        cmd.file = MagicMock()
        cmd.file.data_heads = ['Time', 'Rg\\sX\\N']
        cmd.file.xlabel = 'X\\saxis\\N'
        cmd.file.ylabel = 'Y\\saxis\\N'
        
        cmd.remove_latex('XVG')
        
        assert "_{" in cmd.file.data_heads[1]
        assert "_{" in cmd.file.xlabel
        assert "_{" in cmd.file.ylabel

    def test_remove_latex_xvg_gnuplot(self):
        """Test remove_latex for XVG with gnuplot engine (no dollar signs)."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.engine = 'gnuplot'
        cmd.file = MagicMock()
        cmd.file.data_heads = ['Time', 'Rg\\sX\\N']
        cmd.file.xlabel = 'X\\saxis\\N'
        cmd.file.ylabel = 'Y\\saxis\\N'
        
        cmd.remove_latex('XVG')
        
        # gnuplot should not have dollar signs
        assert "$" not in cmd.file.xlabel
        assert "$" not in cmd.file.ylabel

    def test_remove_latex_xpm_matplotlib(self):
        """Test remove_latex for XPM with matplotlib engine."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.engine = 'matplotlib'
        cmd.file = MagicMock()
        cmd.file.legend = 'G\\senergy\\N'
        cmd.file.xlabel = 'PC1'
        cmd.file.ylabel = 'PC2'
        
        cmd.remove_latex('XPM')
        
        assert "_{" in cmd.file.legend


class TestCommandRemoveLatexMsgs:
    """Test cases for Command.remove_latex_msgs method."""

    def test_remove_latex_msgs_matplotlib(self):
        """Test remove_latex_msgs with matplotlib engine."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.engine = 'matplotlib'
        
        msgs = ['Rg\\sX\\N', 'Rg\\sY\\N']
        result = cmd.remove_latex_msgs(msgs)
        
        assert len(result) == 2
        assert "_{" in result[0]
        assert "_{" in result[1]

    def test_remove_latex_msgs_gnuplot(self):
        """Test remove_latex_msgs with gnuplot engine."""
        cmd = Command()
        cmd.parm = MagicMock()
        cmd.parm.engine = 'gnuplot'
        
        msgs = ['Rg\\sX\\N', 'Rg\\sY\\N']
        result = cmd.remove_latex_msgs(msgs)
        
        assert len(result) == 2
        # gnuplot should not have dollar signs
        for r in result:
            assert "$" not in r
