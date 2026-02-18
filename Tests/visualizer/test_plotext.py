"""
Test cases for Visualizer_plotext.py module.

Tests for:
- ParentPlotext: base class with hex2rgb, final
- LinePlotext: line plot
- ScatterPlotext: scatter plot
- BarPlotext: bar plot
- ImshowPlotext: heatmap

Note: Plotext is a terminal-based plotting library.
Tests mock plt.show() to avoid interactive display.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import plotext as plt

from Visualizer.Visualizer_plotext import (
    ParentPlotext,
    LinePlotext,
    ScatterPlotext,
    BarPlotext,
    ImshowPlotext,
)


# ============================================================================
# Test ParentPlotext
# ============================================================================

class TestParentPlotext:
    """Test cases for ParentPlotext base class."""

    def test_init(self):
        """Test initialization."""
        parent = ParentPlotext()
        assert parent.style is not None
        assert "color_cycle" in parent.style
        assert len(parent.style["color_cycle"]) > 0

    def test_hex2rgb(self):
        """Test hex to RGB conversion."""
        parent = ParentPlotext()
        # Test standard hex color
        result = parent.hex2rgb("#FF0000")
        assert result == (255, 0, 0)
        
        # Test another color
        result = parent.hex2rgb("#00FF00")
        assert result == (0, 255, 0)
        
        # Test blue
        result = parent.hex2rgb("#0000FF")
        assert result == (0, 0, 255)

    def test_hex2rgb_with_first_color(self):
        """Test hex2rgb with first color from style."""
        parent = ParentPlotext()
        result = parent.hex2rgb(parent.style["color_cycle"][0])
        assert isinstance(result, tuple)
        assert len(result) == 3

    @patch.object(plt, 'show')
    @patch.object(ParentPlotext, 'info')
    def test_final_with_outfig(self, mock_info, mock_show):
        """Test final method with output file (should warn)."""
        parent = ParentPlotext()
        parent.final(outfig="test.txt", noshow=True)
        mock_info.assert_called_once()
        mock_show.assert_called_once()

    @patch.object(plt, 'show')
    def test_final_without_outfig(self, mock_show):
        """Test final method without output file."""
        parent = ParentPlotext()
        parent.final(outfig=None, noshow=False)
        mock_show.assert_called_once()


# ============================================================================
# Test LinePlotext
# ============================================================================

class TestLinePlotext:
    """Test cases for LinePlotext class."""

    @pytest.fixture
    def basic_line_kwargs(self):
        """Basic kwargs for LinePlotext."""
        return {
            "data_list": [[1.0, 2.0, 3.0, 4.0]],
            "xdata_list": [[0.0, 1.0, 2.0, 3.0]],
            "legends": ["Test Line"],
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
            "xlabel": "X Axis",
            "ylabel": "Y Axis",
            "title": "Test Title",
            "x_precision": None,
            "y_precision": None,
            "highs": [],
            "lows": [],
            "origins": [],
        }

    @patch.object(plt, 'show')
    def test_init_basic(self, mock_show, basic_line_kwargs):
        """Test basic initialization."""
        line = LinePlotext(**basic_line_kwargs)
        assert line.style is not None

    @patch.object(plt, 'show')
    def test_init_with_xlim_ylim(self, mock_show, basic_line_kwargs):
        """Test initialization with axis limits."""
        basic_line_kwargs["xmin"] = 0
        basic_line_kwargs["xmax"] = 10
        basic_line_kwargs["ymin"] = 0
        basic_line_kwargs["ymax"] = 5
        line = LinePlotext(**basic_line_kwargs)
        assert line.style is not None

    @patch.object(plt, 'show')
    @patch.object(LinePlotext, 'warn')
    def test_init_with_highs_lows(self, mock_warn, mock_show, basic_line_kwargs):
        """Test initialization with confidence intervals (should warn)."""
        basic_line_kwargs["highs"] = [[1.5, 2.5, 3.5, 4.5]]
        basic_line_kwargs["lows"] = [[0.5, 1.5, 2.5, 3.5]]
        line = LinePlotext(**basic_line_kwargs)
        # Should warn about inability to plot intervals
        assert mock_warn.called

    @patch.object(plt, 'show')
    @patch.object(LinePlotext, 'warn')
    def test_init_with_origins(self, mock_warn, mock_show, basic_line_kwargs):
        """Test initialization with origins data (should warn)."""
        basic_line_kwargs["origins"] = [[0.5, 1.5, 2.5, 3.5]]
        line = LinePlotext(**basic_line_kwargs)
        assert mock_warn.called

    @patch.object(plt, 'show')
    @patch.object(LinePlotext, 'warn')
    def test_init_with_precision(self, mock_warn, mock_show, basic_line_kwargs):
        """Test initialization with precision settings (should warn)."""
        basic_line_kwargs["x_precision"] = 2
        basic_line_kwargs["y_precision"] = 3
        line = LinePlotext(**basic_line_kwargs)
        # Should warn about inability to apply precision
        assert mock_warn.called

    @patch.object(plt, 'show')
    def test_init_multiple_lines(self, mock_show, basic_line_kwargs):
        """Test initialization with multiple lines."""
        basic_line_kwargs["data_list"] = [[1, 2, 3], [4, 5, 6]]
        basic_line_kwargs["xdata_list"] = [[0, 1, 2], [0, 1, 2]]
        basic_line_kwargs["legends"] = ["Line 1", "Line 2"]
        line = LinePlotext(**basic_line_kwargs)
        assert line.style is not None


# ============================================================================
# Test ScatterPlotext
# ============================================================================

class TestScatterPlotext:
    """Test cases for ScatterPlotext class."""

    @pytest.fixture
    def basic_scatter_kwargs(self):
        """Basic kwargs for ScatterPlotext."""
        return {
            "data_list": [[1.0, 2.0, 3.0]],
            "xdata_list": [[0.0, 1.0, 2.0]],
            "color_list": None,
            "legends": ["Test Scatter"],
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": None,
            "title": "Scatter Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "cmap": None,
            "colorbar_location": None,
        }

    @patch.object(plt, 'show')
    def test_init_basic(self, mock_show, basic_scatter_kwargs):
        """Test basic initialization."""
        scatter = ScatterPlotext(**basic_scatter_kwargs)
        assert scatter.style is not None

    @patch.object(plt, 'show')
    def test_init_with_xlim_ylim(self, mock_show, basic_scatter_kwargs):
        """Test initialization with axis limits."""
        basic_scatter_kwargs["xmin"] = 0
        basic_scatter_kwargs["xmax"] = 10
        basic_scatter_kwargs["ymin"] = 0
        basic_scatter_kwargs["ymax"] = 5
        scatter = ScatterPlotext(**basic_scatter_kwargs)
        assert scatter.style is not None

    @patch.object(plt, 'show')
    @patch.object(ScatterPlotext, 'warn')
    def test_init_with_color_list(self, mock_warn, mock_show, basic_scatter_kwargs):
        """Test initialization with color list (should warn)."""
        basic_scatter_kwargs["color_list"] = ["red"]
        scatter = ScatterPlotext(**basic_scatter_kwargs)
        assert mock_warn.called

    @patch.object(plt, 'show')
    @patch.object(ScatterPlotext, 'warn')
    def test_init_with_unsupported_options(self, mock_warn, mock_show, basic_scatter_kwargs):
        """Test initialization with unsupported options."""
        basic_scatter_kwargs["cmap"] = "viridis"
        basic_scatter_kwargs["zlabel"] = "Z"
        scatter = ScatterPlotext(**basic_scatter_kwargs)
        assert mock_warn.called


# ============================================================================
# Test BarPlotext
# ============================================================================

class TestBarPlotext:
    """Test cases for BarPlotext class."""

    @pytest.fixture
    def basic_bar_kwargs(self):
        """Basic kwargs for BarPlotext."""
        return {
            "data_list": [[1.0, 2.0, 3.0]],
            "stds_list": [],
            "xtitles": ["A", "B", "C"],
            "legends": ["Test Bar"],
            "title": "Bar Test",
        }

    @patch.object(plt, 'show')
    def test_init_basic(self, mock_show, basic_bar_kwargs):
        """Test basic initialization."""
        bar = BarPlotext(**basic_bar_kwargs)
        assert bar.style is not None

    @patch.object(plt, 'show')
    @patch.object(BarPlotext, 'warn')
    def test_init_with_stds(self, mock_warn, mock_show, basic_bar_kwargs):
        """Test initialization with standard deviations (should warn)."""
        basic_bar_kwargs["stds_list"] = [[0.1, 0.2, 0.3]]
        bar = BarPlotext(**basic_bar_kwargs)
        assert mock_warn.called

    @patch.object(plt, 'show')
    def test_init_multiple_bars(self, mock_show, basic_bar_kwargs):
        """Test initialization with multiple bar series."""
        basic_bar_kwargs["data_list"] = [[1, 2, 3], [2, 3, 4]]
        basic_bar_kwargs["legends"] = ["Series 1", "Series 2"]
        bar = BarPlotext(**basic_bar_kwargs)
        assert bar.style is not None


# ============================================================================
# Test ImshowPlotext
# ============================================================================

class TestImshowPlotext:
    """Test cases for ImshowPlotext class."""

    @pytest.fixture
    def basic_imshow_kwargs(self):
        """Basic kwargs for ImshowPlotext."""
        return {
            "data_list": [[1, 2], [3, 4]],
            "xdata_list": [0, 1],
            "ydata_list": [0, 1],
        }

    @patch.object(plt, 'show')
    @patch.object(ImshowPlotext, 'warn')
    def test_init_basic(self, mock_warn, mock_show, basic_imshow_kwargs):
        """Test basic initialization."""
        imshow = ImshowPlotext(**basic_imshow_kwargs)
        assert imshow.style is not None
        # Should warn about terminal size
        assert mock_warn.called

    @patch.object(plt, 'show')
    @patch.object(ImshowPlotext, 'warn')
    def test_init_larger_matrix(self, mock_warn, mock_show, basic_imshow_kwargs):
        """Test initialization with larger matrix."""
        basic_imshow_kwargs["data_list"] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        basic_imshow_kwargs["xdata_list"] = [0, 1, 2]
        basic_imshow_kwargs["ydata_list"] = [0, 1, 2]
        imshow = ImshowPlotext(**basic_imshow_kwargs)
        assert imshow.style is not None
