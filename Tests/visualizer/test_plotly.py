"""
Test cases for Visualizer_plotly.py module.

Tests for:
- ParentPlotly: load_style, final, hex2rgb, get_color
- LinePlotly: line plot with various options
- PcolormeshPlotly: heatmap visualization
- ScatterPlotly: scatter plot
- Other plot classes
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

from Visualizer.Visualizer_plotly import (
    ParentPlotly,
    LinePlotly,
    StackPlotly,
    ScatterPlotly,
    BarPlotly,
    BoxPlotly,
    PcolormeshPlotly,
    ThreeDimensionPlotly,
    ContourPlotly,
)


# ============================================================================
# Test ParentPlotly
# ============================================================================

class TestParentPlotly:
    """Test cases for ParentPlotly base class."""

    def test_init(self):
        """Test initialization creates figure."""
        parent = ParentPlotly()
        assert parent.figure is not None
        assert parent.templates_name is not None

    def test_hex2rgb(self):
        """Test hex to rgb conversion."""
        parent = ParentPlotly()
        result = parent.hex2rgb("#FF0000")
        assert result == "rgb(255,0,0)"
        
        result = parent.hex2rgb("#00FF00")
        assert result == "rgb(0,255,0)"

    def test_get_color(self):
        """Test get_color returns valid color."""
        parent = ParentPlotly()
        color = parent.get_color(0)
        assert color is not None
        assert color.startswith("rgb(") or color.startswith("#")

    def test_load_style_default(self):
        """Test load_style uses default style when no custom style exists."""
        parent = ParentPlotly()
        assert parent.templates_name is not None

    @patch('plotly.graph_objs.Figure.show')
    def test_final_with_show(self, mock_show):
        """Test final method shows figure when noshow=False."""
        parent = ParentPlotly()
        parent.final(None, noshow=False)
        mock_show.assert_called_once()

    def test_final_noshow(self):
        """Test final method does not show figure when noshow=True."""
        parent = ParentPlotly()
        # Should not raise any errors
        parent.final(None, noshow=True)

    def test_final_with_output_warning(self, caplog):
        """Test final method warns when output is specified."""
        import logging
        caplog.set_level(logging.WARNING)
        parent = ParentPlotly()
        parent.final("output.png", noshow=True)
        # Plotly warns that it cannot save figure directly
        assert any("unable to save" in record.message.lower() for record in caplog.records)


# ============================================================================
# Test LinePlotly
# ============================================================================

class TestLinePlotly:
    """Test cases for LinePlotly class."""

    @pytest.fixture
    def basic_line_kwargs(self):
        """Basic kwargs for LinePlotly."""
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
            "x_numticks": None,
            "y_numticks": None,
            "highs": [],
            "lows": [],
            "origins": [],
            "alpha": 0.4,
        }

    def test_init_basic(self, basic_line_kwargs):
        """Test basic initialization."""
        line = LinePlotly(**basic_line_kwargs)
        assert line.figure is not None

    def test_init_with_xlim_ylim(self, basic_line_kwargs):
        """Test initialization with axis limits."""
        basic_line_kwargs["xmin"] = 0
        basic_line_kwargs["xmax"] = 10
        basic_line_kwargs["ymin"] = 0
        basic_line_kwargs["ymax"] = 5
        line = LinePlotly(**basic_line_kwargs)
        assert line.figure is not None

    def test_init_with_confidence_interval(self, basic_line_kwargs):
        """Test initialization with confidence intervals."""
        basic_line_kwargs["highs"] = [[1.5, 2.5, 3.5, 4.5]]
        basic_line_kwargs["lows"] = [[0.5, 1.5, 2.5, 3.5]]
        line = LinePlotly(**basic_line_kwargs)
        assert line.figure is not None

    def test_init_multiple_lines(self, basic_line_kwargs):
        """Test initialization with multiple lines."""
        basic_line_kwargs["data_list"] = [[1, 2, 3], [4, 5, 6]]
        basic_line_kwargs["xdata_list"] = [[0, 1, 2], [0, 1, 2]]
        basic_line_kwargs["legends"] = ["Line 1", "Line 2"]
        line = LinePlotly(**basic_line_kwargs)
        assert line.figure is not None

    def test_init_empty_legend(self, basic_line_kwargs):
        """Test initialization with empty legend string."""
        basic_line_kwargs["legends"] = [""]
        line = LinePlotly(**basic_line_kwargs)
        assert line.figure is not None


# ============================================================================
# Test ScatterPlotly
# ============================================================================

class TestScatterPlotly:
    """Test cases for ScatterPlotly class."""

    @pytest.fixture
    def basic_scatter_kwargs(self):
        """Basic kwargs for ScatterPlotly."""
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
            "x_numticks": None,
            "y_numticks": None,
            "z_numticks": None,
            "alpha": 1.0,
            "cmap": None,
            "colorbar_location": "right",
            "legend_location": "inside",
            "legend_ncol": 1,
        }

    def test_init_basic(self, basic_scatter_kwargs):
        """Test basic initialization without color mapping."""
        scatter = ScatterPlotly(**basic_scatter_kwargs)
        assert scatter.figure is not None

    def test_init_with_color_mapping(self, basic_scatter_kwargs):
        """Test initialization with color mapping."""
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        basic_scatter_kwargs["zlabel"] = "Color Value"
        scatter = ScatterPlotly(**basic_scatter_kwargs)
        assert scatter.figure is not None


# ============================================================================
# Test PcolormeshPlotly
# ============================================================================

class TestPcolormeshPlotly:
    """Test cases for PcolormeshPlotly class."""

    @pytest.fixture
    def basic_pcolormesh_kwargs(self):
        """Basic kwargs for PcolormeshPlotly."""
        return {
            "data_list": np.array([[1.0, 2.0], [3.0, 4.0]]),
            "xdata_list": np.array([0.0, 1.0]),
            "ydata_list": np.array([0.0, 1.0]),
            "legends": [],
            "color_list": None,
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": "Value",
            "title": "Pcolormesh Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "x_numticks": None,
            "y_numticks": None,
            "z_numticks": None,
            "alpha": None,
            "legend_location": "outside",
            "legend_ncol": 1,
            "colorbar_location": "right",
            "fig_type": "Continuous",
            "cmap": None,
        }

    def test_init_basic(self, basic_pcolormesh_kwargs):
        """Test basic initialization."""
        pc = PcolormeshPlotly(**basic_pcolormesh_kwargs)
        assert pc.figure is not None

    def test_init_with_colormap(self, basic_pcolormesh_kwargs):
        """Test initialization with custom colormap."""
        basic_pcolormesh_kwargs["cmap"] = "Viridis"
        pc = PcolormeshPlotly(**basic_pcolormesh_kwargs)
        assert pc.figure is not None


# ============================================================================
# Test ThreeDimensionPlotly
# ============================================================================

class TestThreeDimensionPlotly:
    """Test cases for ThreeDimensionPlotly class."""

    @pytest.fixture
    def basic_3d_kwargs(self):
        """Basic kwargs for ThreeDimensionPlotly."""
        return {
            "data_list": np.array([[1.0, 2.0], [3.0, 4.0]]),
            "xdata_list": np.array([0.0, 1.0]),
            "ydata_list": np.array([0.0, 1.0]),
            "legends": [],
            "color_list": None,
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": "Z",
            "title": "3D Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "x_numticks": None,
            "y_numticks": None,
            "z_numticks": None,
            "alpha": None,
            "legend_location": "outside",
            "legend_ncol": 1,
            "colorbar_location": "right",
            "fig_type": "Continuous",
            "cmap": None,
        }

    def test_init_basic(self, basic_3d_kwargs):
        """Test basic initialization."""
        td = ThreeDimensionPlotly(**basic_3d_kwargs)
        assert td.figure is not None


# ============================================================================
# Test ContourPlotly
# ============================================================================

class TestContourPlotly:
    """Test cases for ContourPlotly class."""

    @pytest.fixture
    def basic_contour_kwargs(self):
        """Basic kwargs for ContourPlotly."""
        return {
            "data_list": np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]),
            "xdata_list": np.array([0.0, 1.0, 2.0]),
            "ydata_list": np.array([0.0, 1.0, 2.0]),
            "legends": [],
            "color_list": None,
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": "Z",
            "title": "Contour Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "x_numticks": None,
            "y_numticks": None,
            "z_numticks": None,
            "alpha": None,
            "legend_location": "outside",
            "legend_ncol": 1,
            "colorbar_location": "right",
            "fig_type": "Continuous",
            "cmap": None,
        }

    def test_init_basic(self, basic_contour_kwargs):
        """Test basic initialization."""
        contour = ContourPlotly(**basic_contour_kwargs)
        assert contour.figure is not None


# ============================================================================
# Test BarPlotly
# ============================================================================

class TestBarPlotly:
    """Test cases for BarPlotly class."""

    @pytest.fixture
    def basic_bar_kwargs(self):
        """Basic kwargs for BarPlotly."""
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
            "x_numticks": None,
            "y_numticks": None,
        }

    def test_init_basic(self, basic_bar_kwargs):
        """Test basic initialization."""
        bar = BarPlotly(**basic_bar_kwargs)
        assert bar.figure is not None

    def test_init_with_different_stds(self, basic_bar_kwargs):
        """Test initialization with different standard deviations."""
        basic_bar_kwargs["stds_list"] = [[0.5, 0.3, 0.1]]
        bar = BarPlotly(**basic_bar_kwargs)
        assert bar.figure is not None


# ============================================================================
# Test BoxPlotly
# ============================================================================

class TestBoxPlotly:
    """Test cases for BoxPlotly class."""

    @pytest.fixture
    def basic_box_kwargs(self):
        """Basic kwargs for BoxPlotly."""
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
            "x_numticks": None,
            "y_numticks": None,
            "z_numticks": None,
            "alpha": 0.8,
            "cmap": None,
            "colorbar_location": "right",
            "mode": "withoutScatter",
        }

    def test_init_basic(self, basic_box_kwargs):
        """Test basic initialization."""
        box = BoxPlotly(**basic_box_kwargs)
        assert box.figure is not None

    def test_init_with_scatter(self, basic_box_kwargs):
        """Test initialization with scatter points."""
        basic_box_kwargs["mode"] = "withScatter"
        basic_box_kwargs["color_list"] = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
        box = BoxPlotly(**basic_box_kwargs)
        assert box.figure is not None


# ============================================================================
# Test StackPlotly
# ============================================================================

class TestStackPlotly:
    """Test cases for StackPlotly class."""

    @pytest.fixture
    def basic_stack_kwargs(self):
        """Basic kwargs for StackPlotly."""
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
            "x_numticks": None,
            "y_numticks": None,
            "alpha": 0.6,
        }

    def test_init_basic(self, basic_stack_kwargs):
        """Test basic initialization."""
        stack = StackPlotly(**basic_stack_kwargs)
        assert stack.figure is not None
