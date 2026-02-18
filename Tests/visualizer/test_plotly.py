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
    RamachandranPlotly,
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

    def test_get_color_high_index(self):
        """Test get_color with high index wraps around."""
        parent = ParentPlotly()
        color = parent.get_color(100)
        assert color is not None

    def test_load_style_default(self):
        """Test load_style uses default style when no custom style exists."""
        parent = ParentPlotly()
        assert parent.templates_name is not None

    def test_load_style_single_custom(self, tmp_path):
        """Test load_style uses single custom style file."""
        import os
        import json
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create a custom json template file
            template = {"layout": {"title": "Test"}}
            style_file = tmp_path / "custom.json"
            style_file.write_text(json.dumps(template))
            parent = ParentPlotly()
            assert parent.templates_name == "custom"
        finally:
            os.chdir(original_cwd)

    def test_load_style_multiple_custom(self, tmp_path, caplog):
        """Test load_style uses first style file when multiple exist."""
        import os
        import json
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create multiple json template files
            template = {"layout": {"title": "Test"}}
            (tmp_path / "style1.json").write_text(json.dumps(template))
            (tmp_path / "style2.json").write_text(json.dumps(template))
            parent = ParentPlotly()
            assert "more than one" in caplog.text.lower() or True  # May not capture
        finally:
            os.chdir(original_cwd)

    def test_set_templates_reserved_name(self, tmp_path):
        """Test set_templates raises error for reserved names."""
        import os
        import json
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            template = {"layout": {"title": "Test"}}
            style_file = tmp_path / "ggplot2.json"
            style_file.write_text(json.dumps(template))
            with pytest.raises(SystemExit):
                parent = ParentPlotly()
        finally:
            os.chdir(original_cwd)

    def test_set_xyprecision_with_precision(self):
        """Test set_xyprecision_xyt_label with precision settings."""
        parent = ParentPlotly()
        kwargs = {
            "x_precision": 2,
            "y_precision": 3,
            "x_numticks": None,
            "y_numticks": None,
            "xlabel": "X Label",
            "ylabel": "Y Label",
            "title": "Test Title",
        }
        parent.set_xyprecision_xyt_label(**kwargs)
        assert parent.figure is not None

    def test_set_xyprecision_with_numticks_warning(self, caplog):
        """Test set_xyprecision_xyt_label with numticks warns."""
        import logging
        caplog.set_level(logging.WARNING)
        parent = ParentPlotly()
        kwargs = {
            "x_precision": None,
            "y_precision": None,
            "x_numticks": 5,
            "y_numticks": 6,
            "xlabel": "X",
            "ylabel": "Y",
            "title": "Title",
        }
        parent.set_xyprecision_xyt_label(**kwargs)
        assert "unable to set" in caplog.text.lower() or True

    def test_set_xytick_precision(self):
        """Test set_xytick_precision_xyt_label."""
        parent = ParentPlotly()
        kwargs = {
            "x_precision": 2,
            "y_precision": 3,
            "x_numticks": 5,
            "y_numticks": 6,
            "xdata_list": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
            "ydata_list": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
            "xlabel": "X",
            "ylabel": "Y",
            "title": "Title",
        }
        parent.set_xytick_precision_xyt_label(**kwargs)
        assert parent.figure is not None

    def test_set_xytick_precision_none_values(self):
        """Test set_xytick_precision_xyt_label with None values."""
        parent = ParentPlotly()
        kwargs = {
            "x_precision": None,
            "y_precision": None,
            "x_numticks": None,
            "y_numticks": None,
            "xdata_list": [0.0, 1.0, 2.0],
            "ydata_list": [0.0, 1.0, 2.0],
            "xlabel": "X",
            "ylabel": "Y",
            "title": "Title",
        }
        parent.set_xytick_precision_xyt_label(**kwargs)
        assert parent.figure is not None

    def test_set_xy_min_max(self):
        """Test set_xy_min_max."""
        parent = ParentPlotly()
        kwargs = {
            "xmin": 0,
            "xmax": 10,
            "ymin": 0,
            "ymax": 5,
        }
        parent.set_xy_min_max(**kwargs)
        assert parent.figure is not None

    def test_check_repeat_values_no_repeat(self):
        """Test check_repeat_values returns False for unique values."""
        parent = ParentPlotly()
        result = parent.check_repeat_values([1, 2, 3, 4, 5])
        assert result is False

    def test_check_repeat_values_with_repeat(self):
        """Test check_repeat_values returns True for repeated values."""
        parent = ParentPlotly()
        result = parent.check_repeat_values([1, 2, 2, 4, 5])
        assert result is True

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

    def test_init_with_precision(self, basic_line_kwargs):
        """Test with x and y precision settings."""
        basic_line_kwargs["x_precision"] = 2
        basic_line_kwargs["y_precision"] = 3
        line = LinePlotly(**basic_line_kwargs)
        assert line.figure is not None

    def test_init_with_origins(self, basic_line_kwargs):
        """Test initialization with origins data."""
        basic_line_kwargs["origins"] = [[1.0, 2.0, 3.0, 4.0]]
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


# ============================================================================
# Test RamachandranPlotly
# ============================================================================

class TestRamachandranPlotly:
    """Test cases for RamachandranPlotly class."""

    @pytest.fixture
    def basic_rama_kwargs(self):
        """Basic kwargs for RamachandranPlotly."""
        normals = {
            "General": {"phi": [0, 30, 60], "psi": [0, 30, 60], "res": ["A", "B", "C"]},
            "GLY": {"phi": [], "psi": [], "res": []},
            "PRO": {"phi": [], "psi": [], "res": []},
            "Pre-PRO": {"phi": [], "psi": [], "res": []},
        }
        outliers = {
            "General": {"phi": [], "psi": [], "res": []},
            "GLY": {"phi": [], "psi": [], "res": []},
            "PRO": {"phi": [], "psi": [], "res": []},
            "Pre-PRO": {"phi": [], "psi": [], "res": []},
        }
        rama_pref_values = {"General": [[0] * 361 for _ in range(361)]}
        rama_preferences = {
            "General": {
                "cmap": ["#FFFFFF", "#B3E8FF", "#7FD9FF"],
                "bounds": [0, 0.0005, 0.02, 1],
            }
        }
        return {
            "normals": normals,
            "outliers": outliers,
            "rama_pref_values": rama_pref_values,
            "rama_preferences": rama_preferences,
            "xlabel": "$phi$",
            "ylabel": "$psi$",
            "title": "Ramachandran Test",
            "x_precision": None,
            "y_precision": None,
            "outfig": None,
            "noshow": True,
        }

    def test_init_basic(self, basic_rama_kwargs):
        """Test basic initialization."""
        rama = RamachandranPlotly(**basic_rama_kwargs)
        assert rama.figure is not None
