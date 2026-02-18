"""
Test cases for xpmCommands.py module.

Tests for:
- xpm_show: visualize xpm data
- xpm2csv: convert xpm to csv
- xpm2dat: convert xpm to dat
- xpm_diff: calculate difference of two xpms
- xpm_merge: merge two xpms
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from Commands.xpmCommands import xpm_show, xpm2csv, xpm2dat, xpm_diff, xpm_merge


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def xpm_test_dir():
    """Return xpm test directory path."""
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "xpm_test"))


@pytest.fixture
def continuous_xpm_file(xpm_test_dir):
    """Return a continuous XPM file path (Gibbs free energy)."""
    return os.path.join(xpm_test_dir, "gibbs.xpm")


@pytest.fixture
def discrete_xpm_file(xpm_test_dir):
    """Return a discrete XPM file path (hydrogen bond)."""
    return os.path.join(xpm_test_dir, "hbond.xpm")


class MockParameters:
    """Mock Parameters class for testing."""
    
    def __init__(self, **kwargs):
        # Default values
        self.input = kwargs.get('input', [])
        self.output = kwargs.get('output', None)
        self.noshow = kwargs.get('noshow', False)
        self.xlabel = kwargs.get('xlabel', None)
        self.ylabel = kwargs.get('ylabel', None)
        self.zlabel = kwargs.get('zlabel', None)
        self.title = kwargs.get('title', None)
        self.engine = kwargs.get('engine', 'matplotlib')
        self.mode = kwargs.get('mode', None)
        self.xshrink = kwargs.get('xshrink', 1.0)
        self.yshrink = kwargs.get('yshrink', 1.0)
        self.zshrink = kwargs.get('zshrink', 1.0)
        self.xplus = kwargs.get('xplus', 0.0)
        self.yplus = kwargs.get('yplus', 0.0)
        self.zplus = kwargs.get('zplus', 0.0)
        self.xmin = kwargs.get('xmin', None)
        self.xmax = kwargs.get('xmax', None)
        self.ymin = kwargs.get('ymin', None)
        self.ymax = kwargs.get('ymax', None)
        self.zmin = kwargs.get('zmin', None)
        self.zmax = kwargs.get('zmax', None)
        self.x_precision = kwargs.get('x_precision', None)
        self.y_precision = kwargs.get('y_precision', None)
        self.z_precision = kwargs.get('z_precision', None)
        self.x_numticks = kwargs.get('x_numticks', None)
        self.y_numticks = kwargs.get('y_numticks', None)
        self.z_numticks = kwargs.get('z_numticks', None)
        self.legend_location = kwargs.get('legend_location', None)
        self.legend_ncol = kwargs.get('legend_ncol', None)
        self.colorbar_location = kwargs.get('colorbar_location', None)
        self.alpha = kwargs.get('alpha', None)
        self.colormap = kwargs.get('colormap', None)
        self.interpolation = kwargs.get('interpolation', None)
        self.interpolation_fold = kwargs.get('interpolation_fold', 10)
        self.legends = kwargs.get('legends', None)


# ============================================================================
# Test xpm_show
# ============================================================================

class TestXpmShow:
    """Test cases for xpm_show command."""
    
    def test_xpm_show_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[])
        cmd = xpm_show(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    @patch('Commands.xpmCommands.ImshowMatplotlib')
    def test_xpm_show_continuous_basic(self, mock_imshow, continuous_xpm_file):
        """Test basic xpm_show for continuous XPM."""
        mock_instance = MagicMock()
        mock_imshow.return_value = mock_instance
        
        parm = MockParameters(input=[continuous_xpm_file], noshow=True)
        cmd = xpm_show(parm)
        cmd()
        
        mock_imshow.assert_called_once()
    
    @patch('Commands.xpmCommands.ImshowMatplotlib')
    def test_xpm_show_discrete_basic(self, mock_imshow, discrete_xpm_file):
        """Test basic xpm_show for discrete XPM."""
        mock_instance = MagicMock()
        mock_imshow.return_value = mock_instance
        
        parm = MockParameters(input=[discrete_xpm_file], noshow=True)
        cmd = xpm_show(parm)
        cmd()
        
        mock_imshow.assert_called_once()
    
    @patch('Commands.xpmCommands.PcolormeshMatplotlib')
    def test_xpm_show_pcolormesh_mode(self, mock_pcolormesh, continuous_xpm_file):
        """Test xpm_show with pcolormesh mode."""
        mock_instance = MagicMock()
        mock_pcolormesh.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            mode='pcolormesh',
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_pcolormesh.assert_called_once()
    
    @patch('Commands.xpmCommands.ThreeDimensionMatplotlib')
    def test_xpm_show_3d_mode(self, mock_3d, continuous_xpm_file):
        """Test xpm_show with 3d mode."""
        mock_instance = MagicMock()
        mock_3d.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            mode='3d',
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_3d.assert_called_once()
    
    @patch('Commands.xpmCommands.ContourMatplotlib')
    def test_xpm_show_contour_mode(self, mock_contour, continuous_xpm_file):
        """Test xpm_show with contour mode."""
        mock_instance = MagicMock()
        mock_contour.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            mode='contour',
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_contour.assert_called_once()
    
    @patch('Commands.xpmCommands.PcolormeshPlotly')
    def test_xpm_show_plotly_engine(self, mock_pcolormesh, continuous_xpm_file):
        """Test xpm_show with plotly engine."""
        mock_instance = MagicMock()
        mock_pcolormesh.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            engine='plotly',
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_pcolormesh.assert_called_once()
    
    @patch('Commands.xpmCommands.ThreeDimensionPlotly')
    def test_xpm_show_plotly_3d(self, mock_3d, continuous_xpm_file):
        """Test xpm_show with plotly 3d mode."""
        mock_instance = MagicMock()
        mock_3d.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            engine='plotly',
            mode='3d',
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_3d.assert_called_once()
    
    @patch('Commands.xpmCommands.ImshowGnuplot')
    def test_xpm_show_gnuplot_engine(self, mock_gnuplot, continuous_xpm_file):
        """Test xpm_show with gnuplot engine."""
        mock_instance = MagicMock()
        mock_gnuplot.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            engine='gnuplot',
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_gnuplot.assert_called_once()
    
    @patch('Commands.xpmCommands.PcolormeshMatplotlib')
    def test_xpm_show_with_interpolation(self, mock_pcolormesh, continuous_xpm_file):
        """Test xpm_show with interpolation."""
        mock_instance = MagicMock()
        mock_pcolormesh.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            mode='pcolormesh',
            interpolation='linear',
            interpolation_fold=5,
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_pcolormesh.assert_called_once()
    
    @patch('Commands.xpmCommands.ImshowMatplotlib')
    def test_xpm_show_with_cutting(self, mock_imshow, continuous_xpm_file):
        """Test xpm_show with image cutting."""
        mock_instance = MagicMock()
        mock_imshow.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            xmin=0,
            xmax=50,
            ymin=0,
            ymax=50,
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_imshow.assert_called_once()
    
    @patch('Commands.xpmCommands.ImshowMatplotlib')
    def test_xpm_show_with_colormap(self, mock_imshow, continuous_xpm_file):
        """Test xpm_show with custom colormap."""
        mock_instance = MagicMock()
        mock_imshow.return_value = mock_instance
        
        parm = MockParameters(
            input=[continuous_xpm_file],
            colormap='jet',
            noshow=True
        )
        cmd = xpm_show(parm)
        cmd()
        
        mock_imshow.assert_called_once()
    
    def test_xpm_show_wrong_engine(self, continuous_xpm_file):
        """Test error with wrong engine."""
        parm = MockParameters(input=[continuous_xpm_file], engine='wrong_engine')
        cmd = xpm_show(parm)
        
        with pytest.raises(SystemExit):
            cmd()


# ============================================================================
# Test xpm2csv
# ============================================================================

class TestXpm2Csv:
    """Test cases for xpm2csv command."""
    
    def test_xpm2csv_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[])
        cmd = xpm2csv(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xpm2csv_continuous(self, continuous_xpm_file, tmp_path):
        """Test xpm2csv with continuous XPM."""
        output_file = tmp_path / "output.csv"
        parm = MockParameters(
            input=[continuous_xpm_file],
            output=str(output_file)
        )
        cmd = xpm2csv(parm)
        cmd()
        
        assert output_file.exists()
        # Check file content
        with open(output_file, 'r') as f:
            content = f.read()
            # Should have header line
            assert ',' in content
    
    def test_xpm2csv_discrete(self, discrete_xpm_file, tmp_path):
        """Test xpm2csv with discrete XPM."""
        output_file = tmp_path / "output.csv"
        parm = MockParameters(
            input=[discrete_xpm_file],
            output=str(output_file)
        )
        cmd = xpm2csv(parm)
        cmd()
        
        assert output_file.exists()
        # Check file content for discrete type comment
        with open(output_file, 'r') as f:
            content = f.read()
            assert "not a Continuous type" in content
    
    def test_xpm2csv_with_labels(self, continuous_xpm_file, tmp_path):
        """Test xpm2csv with custom labels."""
        output_file = tmp_path / "output.csv"
        parm = MockParameters(
            input=[continuous_xpm_file],
            output=str(output_file),
            xlabel='PC1',
            ylabel='PC2',
            zlabel='Energy'
        )
        cmd = xpm2csv(parm)
        cmd()
        
        assert output_file.exists()
        with open(output_file, 'r') as f:
            content = f.read()
            assert 'PC1' in content
    
    def test_xpm2csv_with_scale(self, continuous_xpm_file, tmp_path):
        """Test xpm2csv with scale parameters."""
        output_file = tmp_path / "output.csv"
        parm = MockParameters(
            input=[continuous_xpm_file],
            output=str(output_file),
            xshrink=0.001,
            yshrink=1.0,
            zshrink=1.0
        )
        cmd = xpm2csv(parm)
        cmd()
        
        assert output_file.exists()


# ============================================================================
# Test xpm2dat
# ============================================================================

class TestXpm2Dat:
    """Test cases for xpm2dat command."""
    
    def test_xpm2dat_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[])
        cmd = xpm2dat(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xpm2dat_continuous(self, continuous_xpm_file, tmp_path):
        """Test xpm2dat with continuous XPM."""
        output_file = tmp_path / "output.dat"
        parm = MockParameters(
            input=[continuous_xpm_file],
            output=str(output_file)
        )
        cmd = xpm2dat(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_xpm2dat_discrete(self, discrete_xpm_file, tmp_path):
        """Test xpm2dat with discrete XPM."""
        output_file = tmp_path / "output.dat"
        parm = MockParameters(
            input=[discrete_xpm_file],
            output=str(output_file)
        )
        cmd = xpm2dat(parm)
        cmd()
        
        assert output_file.exists()
        with open(output_file, 'r') as f:
            content = f.read()
            assert "not a Continuous type" in content
    
    def test_xpm2dat_with_labels(self, continuous_xpm_file, tmp_path):
        """Test xpm2dat with custom labels."""
        output_file = tmp_path / "output.dat"
        parm = MockParameters(
            input=[continuous_xpm_file],
            output=str(output_file),
            xlabel='X_Axis',
            ylabel='Y_Axis',
            zlabel='Z_Value'
        )
        cmd = xpm2dat(parm)
        cmd()
        
        assert output_file.exists()
        with open(output_file, 'r') as f:
            content = f.read()
            assert 'X_Axis' in content


# ============================================================================
# Test xpm_diff
# ============================================================================

class TestXpmDiff:
    """Test cases for xpm_diff command."""
    
    def test_xpm_diff_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[])
        cmd = xpm_diff(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xpm_diff_single_input(self, continuous_xpm_file):
        """Test error when only one input file specified - will raise IndexError."""
        parm = MockParameters(input=[continuous_xpm_file])
        cmd = xpm_diff(parm)
        
        # Will try to access second file which doesn't exist - IndexError
        with pytest.raises(IndexError):
            cmd()
    
    def test_xpm_diff_basic(self, continuous_xpm_file, tmp_path):
        """Test basic xpm_diff execution."""
        output_file = tmp_path / "diff.xpm"
        parm = MockParameters(
            input=[continuous_xpm_file, continuous_xpm_file],
            output=str(output_file)
        )
        cmd = xpm_diff(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_xpm_diff_with_labels(self, continuous_xpm_file, tmp_path):
        """Test xpm_diff with custom labels."""
        output_file = tmp_path / "diff.xpm"
        parm = MockParameters(
            input=[continuous_xpm_file, continuous_xpm_file],
            output=str(output_file),
            xlabel='X',
            ylabel='Y',
            zlabel='Diff'
        )
        cmd = xpm_diff(parm)
        cmd()
        
        assert output_file.exists()


# ============================================================================
# Test xpm_merge
# ============================================================================

class TestXpmMerge:
    """Test cases for xpm_merge command."""
    
    def test_xpm_merge_no_input(self):
        """Test error when no input file specified."""
        parm = MockParameters(input=[])
        cmd = xpm_merge(parm)
        
        with pytest.raises(SystemExit):
            cmd()
    
    def test_xpm_merge_basic(self, continuous_xpm_file, tmp_path):
        """Test basic xpm_merge execution."""
        output_file = tmp_path / "merge.xpm"
        parm = MockParameters(
            input=[continuous_xpm_file, continuous_xpm_file],
            output=str(output_file)
        )
        cmd = xpm_merge(parm)
        cmd()
        
        assert output_file.exists()
    
    def test_xpm_merge_with_labels(self, continuous_xpm_file, tmp_path):
        """Test xpm_merge with custom labels."""
        output_file = tmp_path / "merge.xpm"
        parm = MockParameters(
            input=[continuous_xpm_file, continuous_xpm_file],
            output=str(output_file),
            xlabel='X',
            ylabel='Y',
            zlabel='Value'
        )
        cmd = xpm_merge(parm)
        cmd()
        
        assert output_file.exists()
