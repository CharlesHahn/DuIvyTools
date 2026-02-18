"""
Test cases for Visualizer_gnuplot.py module.

Tests for:
- Gnuplot: utility class for command generation
- ParentGnuplot: base class with load_style, dump, final
- LineGnuplot: line plot
- Other plot classes

Note: Gnuplot tests focus on script generation and class initialization.
Actual gnuplot execution is not tested to avoid external dependency.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import tempfile

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import numpy as np

from Visualizer.Visualizer_gnuplot import (
    Gnuplot,
    ParentGnuplot,
    LineGnuplot,
    StackGnuplot,
    ScatterGnuplot,
    BarGnuplot,
    BoxGnuplot,
    ImshowGnuplot,
)


# ============================================================================
# Test Gnuplot (utility class)
# ============================================================================

class TestGnuplot:
    """Test cases for Gnuplot utility class."""

    def test_init(self):
        """Test initialization."""
        gpl = Gnuplot()
        assert gpl.style == ""
        assert gpl.xntics == 8
        assert gpl.yntics == 8

    def test_check_repeat_values_no_repeat(self):
        """Test check_repeat_values returns False for unique values."""
        gpl = Gnuplot()
        result = gpl.check_repeat_values([1, 2, 3, 4, 5])
        assert result is False

    def test_check_repeat_values_with_repeat(self):
        """Test check_repeat_values returns True for repeated values."""
        gpl = Gnuplot()
        result = gpl.check_repeat_values([1, 2, 2, 4, 5])
        assert result is True

    def test_use_style(self, tmp_path):
        """Test use_style loads style file."""
        # Create a temporary style file
        style_file = tmp_path / "test.gpstyle"
        style_file.write_text("set style line 1 lw 2\n")
        
        gpl = Gnuplot()
        gpl.use_style(str(style_file))
        assert "set style line 1 lw 2" in gpl.style

    def test_dump2str_line(self):
        """Test dump2str generates gnuplot script string for line plot."""
        gpl = Gnuplot()
        gpl.title = "Test Title"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.plot_type = "line"
        gpl.xdata = [[0, 1, 2]]
        gpl.data = [[1, 2, 3]]
        gpl.legends = ["Test"]
        gpl.highs = []
        gpl.lows = []
        gpl.origins = []
        
        result = gpl.dump2str()
        assert "Test Title" in result
        assert "X" in result
        assert "Y" in result


# ============================================================================
# Test ParentGnuplot
# ============================================================================

class TestParentGnuplot:
    """Test cases for ParentGnuplot base class."""

    def test_init(self):
        """Test initialization."""
        parent = ParentGnuplot()
        assert parent.gnuplot is not None
        assert parent.outfig is not None
        assert parent.gpl_file is not None


# ============================================================================
# Test LineGnuplot
# ============================================================================

class TestLineGnuplot:
    """Test cases for LineGnuplot class."""

    @pytest.fixture
    def basic_line_kwargs(self):
        """Basic kwargs for LineGnuplot."""
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
            "alpha": 0.4,
            "legend_location": "inside",
        }

    def test_init_basic(self, basic_line_kwargs):
        """Test basic initialization."""
        line = LineGnuplot(**basic_line_kwargs)
        assert line.gnuplot is not None
        assert line.gnuplot.title == "Test Title"

    def test_init_with_xlim_ylim(self, basic_line_kwargs):
        """Test initialization with axis limits."""
        basic_line_kwargs["xmin"] = 0
        basic_line_kwargs["xmax"] = 10
        basic_line_kwargs["ymin"] = 0
        basic_line_kwargs["ymax"] = 5
        line = LineGnuplot(**basic_line_kwargs)
        assert line.gnuplot.xmin == 0
        assert line.gnuplot.xmax == 10

    def test_init_with_precision(self, basic_line_kwargs):
        """Test initialization with precision settings."""
        basic_line_kwargs["x_precision"] = 2
        basic_line_kwargs["y_precision"] = 3
        line = LineGnuplot(**basic_line_kwargs)
        assert line.gnuplot.x_precision == 2
        assert line.gnuplot.y_precision == 3

    def test_init_with_confidence_interval(self, basic_line_kwargs):
        """Test initialization with confidence intervals."""
        basic_line_kwargs["highs"] = [[1.5, 2.5, 3.5, 4.5]]
        basic_line_kwargs["lows"] = [[0.5, 1.5, 2.5, 3.5]]
        line = LineGnuplot(**basic_line_kwargs)
        assert line.gnuplot.highs == [[1.5, 2.5, 3.5, 4.5]]

    def test_init_multiple_lines(self, basic_line_kwargs):
        """Test initialization with multiple lines."""
        basic_line_kwargs["data_list"] = [[1, 2, 3], [4, 5, 6]]
        basic_line_kwargs["xdata_list"] = [[0, 1, 2], [0, 1, 2]]
        basic_line_kwargs["legends"] = ["Line 1", "Line 2"]
        line = LineGnuplot(**basic_line_kwargs)
        assert line.gnuplot is not None

    def test_init_legend_outside(self, basic_line_kwargs):
        """Test legend placement outside."""
        basic_line_kwargs["legend_location"] = "outside"
        line = LineGnuplot(**basic_line_kwargs)
        assert line.gnuplot.legend_location == "outside"


# ============================================================================
# Test StackGnuplot
# ============================================================================

class TestStackGnuplot:
    """Test cases for StackGnuplot class."""

    @pytest.fixture
    def basic_stack_kwargs(self):
        """Basic kwargs for StackGnuplot."""
        return {
            "data_list": [[1, 2, 3], [2, 3, 4]],
            "xdata_list": [[0, 1, 2], [0, 1, 2]],
            "legends": ["Series 1", "Series 2"],
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "title": "Stack Test",
            "x_precision": None,
            "y_precision": None,
            "highs": [[1.5, 2.5, 3.5], [2.5, 3.5, 4.5]],
            "lows": [[0.5, 1.5, 2.5], [1.5, 2.5, 3.5]],
            "alpha": 0.6,
            "legend_location": "inside",
        }

    def test_init_basic(self, basic_stack_kwargs):
        """Test basic initialization."""
        stack = StackGnuplot(**basic_stack_kwargs)
        assert stack.gnuplot is not None


# ============================================================================
# Test ScatterGnuplot
# ============================================================================

class TestScatterGnuplot:
    """Test cases for ScatterGnuplot class."""

    @pytest.fixture
    def basic_scatter_kwargs(self):
        """Basic kwargs for ScatterGnuplot."""
        return {
            "data_list": [[1.0, 2.0, 3.0]],
            "xdata_list": [[0.0, 1.0, 2.0]],
            "color_list": [None],
            "legends": ["Test Scatter"],
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": "Z",
            "title": "Scatter Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "alpha": 1.0,
            "cmap": None,
            "legend_location": "inside",
            "colorbar_location": None,
        }

    def test_init_basic(self, basic_scatter_kwargs):
        """Test basic initialization without color mapping."""
        scatter = ScatterGnuplot(**basic_scatter_kwargs)
        assert scatter.gnuplot is not None

    def test_init_with_color_mapping(self, basic_scatter_kwargs):
        """Test initialization with color mapping."""
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        scatter = ScatterGnuplot(**basic_scatter_kwargs)
        assert scatter.gnuplot is not None


# ============================================================================
# Test BarGnuplot
# ============================================================================

class TestBarGnuplot:
    """Test cases for BarGnuplot class."""

    @pytest.fixture
    def basic_bar_kwargs(self):
        """Basic kwargs for BarGnuplot."""
        return {
            "data_list": [[1.0, 2.0, 3.0]],
            "stds_list": [[0.1, 0.2, 0.3]],
            "xtitles": ["A", "B", "C"],
            "legends": ["Test Bar"],
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
            "xlabel": "Category",
            "ylabel": "Value",
            "title": "Bar Test",
            "x_precision": None,
            "y_precision": None,
            "legend_location": "inside",
        }

    def test_init_basic(self, basic_bar_kwargs):
        """Test basic initialization."""
        bar = BarGnuplot(**basic_bar_kwargs)
        assert bar.gnuplot is not None
        assert bar.gnuplot.plot_type == "bar"


# ============================================================================
# Test BoxGnuplot
# ============================================================================

class TestBoxGnuplot:
    """Test cases for BoxGnuplot class."""

    @pytest.fixture
    def basic_box_kwargs(self):
        """Basic kwargs for BoxGnuplot."""
        return {
            "data_list": [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
            "color_list": [None, None],
            "legends": ["Box 1", "Box 2"],
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
            "zmin": None,
            "zmax": None,
            "xlabel": "Category",
            "ylabel": "Value",
            "zlabel": "Color",
            "title": "Box Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "alpha": 0.8,
            "cmap": None,
            "colorbar_location": None,
            "mode": "withoutScatter",
        }

    def test_init_basic(self, basic_box_kwargs):
        """Test basic initialization."""
        box = BoxGnuplot(**basic_box_kwargs)
        assert box.gnuplot is not None


# ============================================================================
# Test ImshowGnuplot
# ============================================================================

class TestImshowGnuplot:
    """Test cases for ImshowGnuplot class."""

    @pytest.fixture
    def basic_imshow_kwargs(self):
        """Basic kwargs for ImshowGnuplot."""
        return {
            "data_list": [[1, 2], [3, 4]],
            "xdata_list": [0, 1],
            "ydata_list": [0, 1],
            "legends": ["A", "B"],
            "color_list": ["#FF0000", "#00FF00"],
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": "Value",
            "title": "Imshow Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "x_numticks": None,
            "y_numticks": None,
            "alpha": None,
            "legend_location": "outside",
            "fig_type": "Continuous",
            "cmap": None,
            "colorbar_location": None,
        }

    def test_init_basic(self, basic_imshow_kwargs):
        """Test basic initialization."""
        imshow = ImshowGnuplot("imshow", **basic_imshow_kwargs)
        assert imshow.gnuplot is not None

    def test_init_3d_mode(self, basic_imshow_kwargs):
        """Test initialization in 3D mode."""
        imshow = ImshowGnuplot("3d", **basic_imshow_kwargs)
        assert imshow.gnuplot is not None

    def test_init_contour_mode(self, basic_imshow_kwargs):
        """Test initialization in contour mode."""
        imshow = ImshowGnuplot("contour", **basic_imshow_kwargs)
        assert imshow.gnuplot is not None