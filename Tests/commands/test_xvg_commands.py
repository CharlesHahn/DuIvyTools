"""
Test cases for xvgCommands.py module.

Tests for:
- xvg_show: visualize xvg data
- xvg_compare: compare xvg data columns
- xvg_ave: compute averages
- xvg_combine: combine xvg files
- xvg_energy_compute: compute binding energy
- xvg_show_distribution: show distribution
- xvg_show_scatter: scatter plot
- xvg_show_stack: stack plot
- xvg_box_compare: box plot comparison
- xvg_ave_bar: average bar chart
- xvg_rama: Ramachandran plot
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from utils import Parameters
from Commands.xvgCommands import (
    xvg_show,
    xvg_compare,
    xvg_ave,
    xvg_combine,
    xvg_energy_compute,
    xvg_show_distribution,
    xvg_show_scatter,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def xvg_test_dir():
    """Return xvg test directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "xvg_test"))


@pytest.fixture
def sample_xvg_file(xvg_test_dir):
    """Return a sample xvg file path."""
    return os.path.join(xvg_test_dir, "gyrate.xvg")


@pytest.fixture
def sample_xvg_files(xvg_test_dir):
    """Return multiple sample xvg file paths."""
    return [
        os.path.join(xvg_test_dir, "gyrate.xvg"),
        os.path.join(xvg_test_dir, "rmsd.xvg"),
    ]


@pytest.fixture
def energy_xvg_files(xvg_test_dir):
    """Return energy xvg file paths."""
    return [
        os.path.join(xvg_test_dir, "prolig_energy.xvg"),
        os.path.join(xvg_test_dir, "pro_energy.xvg"),
        os.path.join(xvg_test_dir, "lig_energy.xvg"),
    ]


class MockParameters:
    """Mock Parameters class for testing."""
    
    def __init__(self, **kwargs):
        # Default values from Parameters class
        self.input = kwargs.get('input', [])
        self.output = kwargs.get('output', None)
        self.noshow = kwargs.get('noshow', False)
        self.legends = kwargs.get('legends', None)
        self.xlabel = kwargs.get('xlabel', None)
        self.ylabel = kwargs.get('ylabel', None)
        self.title = kwargs.get('title', None)
        self.engine = kwargs.get('engine', 'matplotlib')
        self.begin = kwargs.get('begin', None)
        self.end = kwargs.get('end', None)
        self.dt = kwargs.get('dt', None)
        self.xshrink = kwargs.get('xshrink', 1.0)
        self.yshrink = kwargs.get('yshrink', 1.0)
        self.xplus = kwargs.get('xplus', 0.0)
        self.yplus = kwargs.get('yplus', 0.0)
        self.xmin = kwargs.get('xmin', None)
        self.xmax = kwargs.get('xmax', None)
        self.ymin = kwargs.get('ymin', None)
        self.ymax = kwargs.get('ymax', None)
        self.x_precision = kwargs.get('x_precision', None)
        self.y_precision = kwargs.get('y_precision', None)
        self.x_numticks = kwargs.get('x_numticks', None)
        self.y_numticks = kwargs.get('y_numticks', None)
        self.legend_location = kwargs.get('legend_location', None)
        self.legend_ncol = kwargs.get('legend_ncol', None)
        self.alpha = kwargs.get('alpha', None)
        
        # xvg_compare specific
        self.columns = kwargs.get('columns', None)
        self.showMV = kwargs.get('showMV', None)
        self.windowsize = kwargs.get('windowsize', 50)
        self.confidence = kwargs.get('confidence', 0.95)
        self.csv = kwargs.get('csv', None)
        
        # xvg_show_distribution specific
        self.mode = kwargs.get('mode', None)
        self.additional_list = kwargs.get('additional_list', None)
        
        # xvg_show_scatter specific
        self.zlabel = kwargs.get('zlabel', None)
        self.zshrink = kwargs.get('zshrink', 1.0)
        self.zplus = kwargs.get('zplus', 0.0)
        self.zmin = kwargs.get('zmin', None)
        self.zmax = kwargs.get('zmax', None)
        self.z_precision = kwargs.get('z_precision', None)
        self.z_numticks = kwargs.get('z_numticks', None)
        self.colormap = kwargs.get('colormap', None)
        self.colorbar_location = kwargs.get('colorbar_location', None)


# ============================================================================
# Test xvg_show
# ============================================================================

class TestXvgShow:
    """Test cases for xvg_show command."""
    
    def test_xvg_show_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[])
        cmd = xvg_show(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_basic(self, mock_line, sample_xvg_file):
        """Test basic xvg_show execution."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(input=[sample_xvg_file], noshow=True)
        cmd = xvg_show(parm)
        cmd()
        
        # Verify LineMatplotlib was called
        mock_line.assert_called_once()
        mock_instance.final.assert_called_once_with(None, True)
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_with_output(self, mock_line, sample_xvg_file, tmp_path):
        """Test xvg_show with output file."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        output_file = tmp_path / "test_output.png"
        parm = MockParameters(input=[sample_xvg_file], output=str(output_file), noshow=True)
        cmd = xvg_show(parm)
        cmd()
        
        mock_instance.final.assert_called_once()
    
    @patch('Commands.xvgCommands.LinePlotly')
    def test_xvg_show_plotly_engine(self, mock_line, sample_xvg_file):
        """Test xvg_show with plotly engine."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(input=[sample_xvg_file], engine='plotly', noshow=True)
        cmd = xvg_show(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineGnuplot')
    def test_xvg_show_gnuplot_engine(self, mock_line, sample_xvg_file):
        """Test xvg_show with gnuplot engine."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(input=[sample_xvg_file], engine='gnuplot', noshow=True)
        cmd = xvg_show(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LinePlotext')
    def test_xvg_show_plotext_engine(self, mock_line, sample_xvg_file):
        """Test xvg_show with plotext engine."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(input=[sample_xvg_file], engine='plotext', noshow=True)
        cmd = xvg_show(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    def test_xvg_show_wrong_engine(self, sample_xvg_file):
        """Test error with wrong engine."""
        parm = MockParameters(input=[sample_xvg_file], engine='wrong_engine')
        cmd = xvg_show(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_with_range(self, mock_line, sample_xvg_file):
        """Test xvg_show with begin/end/dt parameters."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            begin=100,
            end=500,
            dt=2,
            noshow=True
        )
        cmd = xvg_show(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_with_scale(self, mock_line, sample_xvg_file):
        """Test xvg_show with xshrink/yshrink/xplus/yplus parameters."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            xshrink=0.001,
            yshrink=1.0,
            xplus=0.0,
            yplus=0.0,
            noshow=True
        )
        cmd = xvg_show(parm)
        cmd()
        
        mock_line.assert_called_once()


# ============================================================================
# Test xvg_compare
# ============================================================================

class TestXvgCompare:
    """Test cases for xvg_compare command."""
    
    def test_xvg_compare_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[], columns=[[1]])
        cmd = xvg_compare(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xvg_compare_no_columns(self, sample_xvg_file):
        """Test error when no columns specified."""
        parm = MockParameters(input=[sample_xvg_file], columns=None)
        cmd = xvg_compare(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xvg_compare_mismatched_columns(self, sample_xvg_files):
        """Test error when columns don't match input files."""
        parm = MockParameters(input=sample_xvg_files, columns=[[1]])  # 2 files but 1 column list
        cmd = xvg_compare(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_compare_basic(self, mock_line, sample_xvg_files):
        """Test basic xvg_compare execution."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=sample_xvg_files,
            columns=[[1], [1]],
            noshow=True
        )
        cmd = xvg_compare(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_compare_with_csv(self, mock_line, sample_xvg_files, tmp_path):
        """Test xvg_compare with CSV output."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        csv_file = tmp_path / "compare.csv"
        parm = MockParameters(
            input=sample_xvg_files,
            columns=[[1], [1]],
            csv=str(csv_file),
            noshow=True
        )
        cmd = xvg_compare(parm)
        cmd()
        
        assert csv_file.exists()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_compare_with_mvave(self, mock_line, sample_xvg_file):
        """Test xvg_compare with moving average."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1, 2, 3]],
            showMV='origin',
            windowsize=50,
            noshow=True
        )
        cmd = xvg_compare(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_compare_with_ci(self, mock_line, sample_xvg_file):
        """Test xvg_compare with confidence interval."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1]],
            showMV='CI',
            windowsize=50,
            confidence=0.95,
            noshow=True
        )
        cmd = xvg_compare(parm)
        cmd()
        
        mock_line.assert_called_once()


# ============================================================================
# Test xvg_ave
# ============================================================================

class TestXvgAve:
    """Test cases for xvg_ave command."""
    
    def test_xvg_ave_basic(self, sample_xvg_file, capsys):
        """Test basic xvg_ave execution."""
        parm = MockParameters(input=[sample_xvg_file])
        cmd = xvg_ave(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert "Average" in captured.out
        assert "Std.Dev" in captured.out
    
    def test_xvg_ave_with_output(self, sample_xvg_file, tmp_path):
        """Test xvg_ave with output file."""
        output_file = tmp_path / "ave.dat"
        parm = MockParameters(input=[sample_xvg_file], output=str(output_file))
        cmd = xvg_ave(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_xvg_ave_with_range(self, sample_xvg_file, capsys):
        """Test xvg_ave with range parameters."""
        parm = MockParameters(
            input=[sample_xvg_file],
            begin=100,
            end=500,
            dt=2
        )
        cmd = xvg_ave(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert "Average" in captured.out
    
    def test_xvg_ave_multiple_files(self, sample_xvg_files, capsys):
        """Test xvg_ave with multiple files."""
        parm = MockParameters(input=sample_xvg_files)
        cmd = xvg_ave(parm)
        cmd()
        
        captured = capsys.readouterr()
        assert "Average" in captured.out


# ============================================================================
# Test xvg_combine
# ============================================================================

class TestXvgCombine:
    """Test cases for xvg_combine command."""
    
    def test_xvg_combine_basic(self, sample_xvg_files, tmp_path):
        """Test basic xvg_combine execution."""
        output_file = tmp_path / "combined.xvg"
        parm = MockParameters(
            input=sample_xvg_files,
            columns=[[0, 1], [1]],
            output=str(output_file)
        )
        cmd = xvg_combine(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_xvg_combine_mismatched_columns(self, sample_xvg_files):
        """Test error when columns don't match files."""
        parm = MockParameters(
            input=sample_xvg_files,
            columns=[[1]]  # 2 files but 1 column list
        )
        cmd = xvg_combine(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xvg_combine_with_legends(self, sample_xvg_files, tmp_path):
        """Test xvg_combine with custom legends."""
        output_file = tmp_path / "combined.xvg"
        # columns = [[0, 1], [1]] = 3 columns, legends should be 2 (total - 1)
        parm = MockParameters(
            input=sample_xvg_files,
            columns=[[0, 1], [1]],
            legends=['RMSD', 'Gyrate'],  # Time column doesn't need legend
            output=str(output_file)
        )
        cmd = xvg_combine(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_xvg_combine_with_labels(self, sample_xvg_files, tmp_path):
        """Test xvg_combine with custom labels."""
        output_file = tmp_path / "combined.xvg"
        parm = MockParameters(
            input=sample_xvg_files,
            columns=[[0, 1], [1]],
            xlabel='Time (ps)',
            ylabel='Value',
            title='Combined Data',
            output=str(output_file)
        )
        cmd = xvg_combine(parm)
        cmd()
        
        assert output_file.exists()


# ============================================================================
# Test xvg_energy_compute
# ============================================================================

class TestXvgEnergyCompute:
    """Test cases for xvg_energy_compute command."""
    
    def test_xvg_energy_compute_wrong_file_count(self, sample_xvg_file):
        """Test error with wrong number of files."""
        parm = MockParameters(input=[sample_xvg_file])
        cmd = xvg_energy_compute(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xvg_energy_compute_basic(self, energy_xvg_files, tmp_path):
        """Test basic xvg_energy_compute execution."""
        output_file = tmp_path / "energy.xvg"
        parm = MockParameters(
            input=energy_xvg_files,
            output=str(output_file)
        )
        cmd = xvg_energy_compute(parm)
        cmd()
        
        assert output_file.exists()


# ============================================================================
# Test xvg_show_distribution
# ============================================================================

class TestXvgShowDistribution:
    """Test cases for xvg_show_distribution command."""
    
    def test_xvg_show_distribution_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[], columns=[[1]])
        cmd = xvg_show_distribution(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_distribution_basic(self, mock_line, sample_xvg_file):
        """Test basic xvg_show_distribution execution."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1]],
            noshow=True
        )
        cmd = xvg_show_distribution(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_distribution_with_bin(self, mock_line, sample_xvg_file):
        """Test xvg_show_distribution with custom bin number."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1]],
            additional_list=['50'],
            noshow=True
        )
        cmd = xvg_show_distribution(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_distribution_pdf_mode(self, mock_line, sample_xvg_file):
        """Test xvg_show_distribution with PDF mode."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1]],
            mode='pdf',
            noshow=True
        )
        cmd = xvg_show_distribution(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_distribution_cdf_mode(self, mock_line, sample_xvg_file):
        """Test xvg_show_distribution with CDF mode."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1]],
            mode='cdf',
            noshow=True
        )
        cmd = xvg_show_distribution(parm)
        cmd()
        
        mock_line.assert_called_once()
    
    @patch('Commands.xvgCommands.LineMatplotlib')
    def test_xvg_show_distribution_with_csv(self, mock_line, sample_xvg_file, tmp_path):
        """Test xvg_show_distribution with CSV output."""
        mock_instance = MagicMock()
        mock_line.return_value = mock_instance
        
        csv_file = tmp_path / "distribution.csv"
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1]],
            csv=str(csv_file),
            noshow=True
        )
        cmd = xvg_show_distribution(parm)
        cmd()
        
        assert csv_file.exists()


# ============================================================================
# Test xvg_show_scatter
# ============================================================================

class TestXvgShowScatter:
    """Test cases for xvg_show_scatter command."""
    
    def test_xvg_show_scatter_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[], columns=[[1, 2]])
        cmd = xvg_show_scatter(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xvg_show_scatter_no_columns(self, sample_xvg_file):
        """Test error when no columns specified."""
        parm = MockParameters(input=[sample_xvg_file], columns=None)
        cmd = xvg_show_scatter(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xvg_show_scatter_wrong_column_count(self, sample_xvg_file):
        """Test error with wrong number of columns."""
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1]]  # Need 2 or 3 columns
        )
        cmd = xvg_show_scatter(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    @patch('Commands.xvgCommands.ScatterMatplotlib')
    def test_xvg_show_scatter_basic(self, mock_scatter, sample_xvg_file):
        """Test basic xvg_show_scatter execution."""
        mock_instance = MagicMock()
        mock_scatter.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1, 2]],
            noshow=True
        )
        cmd = xvg_show_scatter(parm)
        cmd()
        
        mock_scatter.assert_called_once()
    
    @patch('Commands.xvgCommands.ScatterMatplotlib')
    def test_xvg_show_scatter_with_color(self, mock_scatter, sample_xvg_file):
        """Test xvg_show_scatter with color column."""
        mock_instance = MagicMock()
        mock_scatter.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1, 2, 0]],  # X, Y, color
            noshow=True
        )
        cmd = xvg_show_scatter(parm)
        cmd()
        
        mock_scatter.assert_called_once()
    
    @patch('Commands.xvgCommands.ScatterPlotly')
    def test_xvg_show_scatter_plotly(self, mock_scatter, sample_xvg_file):
        """Test xvg_show_scatter with plotly engine."""
        mock_instance = MagicMock()
        mock_scatter.return_value = mock_instance
        
        parm = MockParameters(
            input=[sample_xvg_file],
            columns=[[1, 2]],
            engine='plotly',
            noshow=True
        )
        cmd = xvg_show_scatter(parm)
        cmd()
        
        mock_scatter.assert_called_once()
