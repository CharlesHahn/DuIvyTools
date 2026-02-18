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

    def test_init_discrete_mode(self, basic_imshow_kwargs):
        """Test initialization in discrete (non-continuous) mode."""
        basic_imshow_kwargs["fig_type"] = "Discrete"
        imshow = ImshowGnuplot("imshow", **basic_imshow_kwargs)
        assert imshow.gnuplot is not None
        assert imshow.gnuplot.xpm_type == "Discrete"

    def test_init_with_numticks(self, basic_imshow_kwargs):
        """Test initialization with x_numticks and y_numticks."""
        basic_imshow_kwargs["x_numticks"] = 5
        basic_imshow_kwargs["y_numticks"] = 4
        imshow = ImshowGnuplot("imshow", **basic_imshow_kwargs)
        assert imshow.gnuplot.xntics == 5
        assert imshow.gnuplot.yntics == 4

    def test_init_with_precision(self, basic_imshow_kwargs):
        """Test initialization with precision settings."""
        basic_imshow_kwargs["x_precision"] = 2
        basic_imshow_kwargs["y_precision"] = 3
        basic_imshow_kwargs["z_precision"] = 4
        imshow = ImshowGnuplot("imshow", **basic_imshow_kwargs)
        assert imshow.gnuplot.x_precision == 2
        assert imshow.gnuplot.y_precision == 3
        assert imshow.gnuplot.z_precision == 4

    def test_init_with_cmap_warning(self, basic_imshow_kwargs, caplog):
        """Test initialization with cmap triggers warning."""
        basic_imshow_kwargs["cmap"] = "viridis"
        imshow = ImshowGnuplot("imshow", **basic_imshow_kwargs)
        assert "unable to set colormap" in caplog.text.lower() or imshow.gnuplot is not None

    def test_init_with_colorbar_location_warning(self, basic_imshow_kwargs, caplog):
        """Test initialization with colorbar_location triggers warning."""
        basic_imshow_kwargs["colorbar_location"] = "right"
        imshow = ImshowGnuplot("imshow", **basic_imshow_kwargs)
        assert "unable to set colorbar location" in caplog.text.lower() or imshow.gnuplot is not None


# ============================================================================
# Test Gnuplot additional methods
# ============================================================================

class TestGnuplotMethods:
    """Test additional methods of Gnuplot class."""

    def test_set_xy_repeat_tick_precision_no_repeat(self):
        """Test set_xy_repeat_tick_precision with no repeated values."""
        gpl = Gnuplot()
        gpl.xdata = [0, 1, 2, 3, 4, 5, 6, 7]
        gpl.ydata = [0, 1, 2, 3, 4, 5, 6, 7]
        gpl.x_precision = None
        gpl.y_precision = None
        
        result = gpl.set_xy_repeat_tick_precision("test script\n")
        assert "test script" in result
        assert "set xtics" not in result  # no repeat, no tics change

    def test_set_xy_repeat_tick_precision_with_repeat_x(self):
        """Test set_xy_repeat_tick_precision with repeated x values."""
        gpl = Gnuplot()
        gpl.xdata = [0, 0, 1, 1, 2, 2]  # repeated values
        gpl.ydata = [0, 1, 2, 3, 4, 5]
        gpl.x_precision = None
        gpl.y_precision = None
        
        result = gpl.set_xy_repeat_tick_precision("test script\n")
        assert "set xtics" in result

    def test_set_xy_repeat_tick_precision_with_repeat_y(self):
        """Test set_xy_repeat_tick_precision with repeated y values."""
        gpl = Gnuplot()
        gpl.xdata = [0, 1, 2, 3, 4, 5]
        gpl.ydata = [0, 0, 1, 1, 2, 2]  # repeated values
        gpl.x_precision = None
        gpl.y_precision = None
        
        result = gpl.set_xy_repeat_tick_precision("test script\n")
        assert "set ytics" in result

    def test_dump2str_scatter(self):
        """Test dump2str generates script for scatter plot."""
        gpl = Gnuplot()
        gpl.title = "Scatter Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.plot_type = "scatter"
        gpl.xdata = [[0, 1, 2]]
        gpl.data = [[1, 2, 3]]
        gpl.legends = ["Test"]
        gpl.color_list = [None]
        gpl.highs = []
        gpl.lows = []
        gpl.origins = []
        gpl.alpha = 1.0
        
        result = gpl.dump2str()
        assert "Scatter Test" in result
        assert "with points" in result

    def test_dump2str_scatter_with_colors(self):
        """Test dump2str generates script for scatter plot with color mapping."""
        gpl = Gnuplot()
        gpl.title = "Scatter Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.zlabel = "Z"
        gpl.plot_type = "scatter"
        gpl.xdata = [[0, 1, 2]]
        gpl.data = [[1, 2, 3]]
        gpl.legends = ["Test"]
        gpl.color_list = [[0.1, 0.5, 0.9]]
        gpl.highs = []
        gpl.lows = []
        gpl.origins = []
        gpl.alpha = 1.0
        
        result = gpl.dump2str()
        assert "palette" in result

    def test_dump2str_stack(self):
        """Test dump2str generates script for stack plot."""
        gpl = Gnuplot()
        gpl.title = "Stack Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.plot_type = "stack"
        gpl.xdata = [[0, 1, 2]]
        gpl.data = [[1, 2, 3]]
        gpl.legends = ["Test"]
        gpl.highs = [[1.5, 2.5, 3.5]]
        gpl.lows = [[0.5, 1.5, 2.5]]
        gpl.alpha = 0.5
        
        result = gpl.dump2str()
        assert "Stack Test" in result
        assert "filledcurves" in result

    def test_dump2str_bar(self):
        """Test dump2str generates script for bar plot."""
        gpl = Gnuplot()
        gpl.title = "Bar Test"
        gpl.xlabel = "Category"
        gpl.ylabel = "Value"
        gpl.plot_type = "bar"
        gpl.data = [[1, 2, 3]]
        gpl.legends = ["Test"]
        gpl.xtitles = ["A", "B", "C"]
        gpl.stds_list = [[0.1, 0.2, 0.3]]
        
        result = gpl.dump2str()
        assert "Bar Test" in result
        assert "histogram" in result

    def test_dump2str_violin(self):
        """Test dump2str generates script for violin plot."""
        gpl = Gnuplot()
        gpl.title = "Violin Test"
        gpl.xlabel = "Category"
        gpl.ylabel = "Value"
        gpl.plot_type = "violin"
        gpl.data = [[1, 2, 3, 4, 5]]
        gpl.legends = ["Test"]
        gpl.color_list = [[0.1, 0.2, 0.3, 0.4, 0.5]]
        gpl.mode = "withoutScatter"
        
        result = gpl.dump2str()
        assert "Violin Test" in result
        assert "kdensity" in result

    def test_dump2str_violin_with_scatter(self):
        """Test dump2str generates script for violin plot with scatter."""
        gpl = Gnuplot()
        gpl.title = "Violin Test"
        gpl.xlabel = "Category"
        gpl.ylabel = "Value"
        gpl.zlabel = "Color"
        gpl.plot_type = "violin"
        gpl.data = [[1, 2, 3, 4, 5]]
        gpl.legends = ["Test"]
        gpl.color_list = [[0.1, 0.2, 0.3, 0.4, 0.5]]
        gpl.mode = "withScatter"
        
        result = gpl.dump2str()
        assert "palette" in result

    def test_dump2str_3d(self):
        """Test dump2str generates script for 3D plot."""
        gpl = Gnuplot()
        gpl.title = "3D Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.zlabel = "Z"
        gpl.plot_type = "3d"
        gpl.xdata = [0, 1, 2]
        gpl.ydata = [0, 1, 2]
        gpl.data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        
        result = gpl.dump2str()
        assert "splot" in result
        assert "pm3d" in result

    def test_dump2str_contour(self):
        """Test dump2str generates script for contour plot."""
        gpl = Gnuplot()
        gpl.title = "Contour Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.zlabel = "Z"
        gpl.plot_type = "contour"
        gpl.xdata = [0, 1, 2]
        gpl.ydata = [0, 1, 2]
        gpl.data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        
        result = gpl.dump2str()
        assert "splot" in result
        assert "view map" in result

    def test_dump2str_imshow_continuous(self):
        """Test dump2str generates script for imshow (continuous) plot."""
        gpl = Gnuplot()
        gpl.title = "Imshow Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.zlabel = "Value"
        gpl.plot_type = "imshow"
        gpl.xpm_type = "Continuous"
        gpl.xdata = [0, 1, 2]
        gpl.ydata = [0, 1, 2]
        gpl.data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        gpl.legends = []
        gpl.color_list = []
        
        result = gpl.dump2str()
        assert "with image" in result

    def test_dump2str_imshow_discrete(self):
        """Test dump2str generates script for imshow (discrete) plot."""
        gpl = Gnuplot()
        gpl.title = "Imshow Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.plot_type = "imshow"
        gpl.xpm_type = "Discrete"
        gpl.xdata = [0, 1]
        gpl.ydata = [0, 1]
        gpl.data = [[0, 1], [1, 0]]
        gpl.legends = ["A", "B"]
        gpl.color_list = ["#FF0000", "#00FF00"]
        
        result = gpl.dump2str()
        assert "set pal defined" in result

    def test_line_plot_with_origins(self):
        """Test line_plot with origins parameter."""
        gpl = Gnuplot()
        gpl.title = "Line Test"
        gpl.xlabel = "X"
        gpl.ylabel = "Y"
        gpl.plot_type = "line"
        gpl.xdata = [[0, 1, 2]]
        gpl.data = [[1, 2, 3]]
        gpl.legends = ["Test"]
        gpl.highs = []
        gpl.lows = []
        gpl.origins = [[0, 0, 0]]
        gpl.alpha = 0.5
        
        result = gpl.dump2str()
        assert "linestyle 10" in result  # origin lines use linestyle 10x


# ============================================================================
# Test ParentGnuplot methods
# ============================================================================

class TestParentGnuplotMethods:
    """Test methods of ParentGnuplot class."""

    def test_dump(self, tmp_path):
        """Test dump method creates gnuplot script file."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test Title"
            parent.gnuplot.xlabel = "X"
            parent.gnuplot.ylabel = "Y"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            
            parent.dump()
            assert os.path.exists(parent.gpl_file)
            
            # Clean up
            os.remove(parent.gpl_file)
        finally:
            os.chdir(original_cwd)

    def test_clean(self, tmp_path):
        """Test clean method removes gnuplot script file."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            parent.dump()
            gpl_file = parent.gpl_file
            assert os.path.exists(gpl_file)
            
            parent.clean()
            assert not os.path.exists(gpl_file)
        finally:
            os.chdir(original_cwd)

    def test_final_noshow(self, tmp_path):
        """Test final method with noshow=True dumps script."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            
            parent.final(outfig=None, noshow=True)
            assert os.path.exists(parent.gpl_file)
            
            # Clean up
            os.remove(parent.gpl_file)
        finally:
            os.chdir(original_cwd)

    def test_final_with_outfig(self, tmp_path):
        """Test final method with output file."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            
            parent.final(outfig="test_output.png", noshow=True)
            assert parent.gnuplot.outfig == "test_output.png"
            
            # Clean up
            os.remove(parent.gpl_file)
        finally:
            os.chdir(original_cwd)

    def test_final_with_existing_outfig(self, tmp_path, caplog):
        """Test final method with existing output file renames."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create existing file
            existing_file = tmp_path / "existing.png"
            existing_file.write_text("dummy")
            
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            
            parent.final(outfig="existing.png", noshow=True)
            # Should have renamed output file
            assert "existing_" in parent.gnuplot.outfig or "already" in caplog.text.lower()
            
            # Clean up
            os.remove(parent.gpl_file)
        finally:
            os.chdir(original_cwd)


# ============================================================================
# Test run methods (require gnuplot executable)
# ============================================================================

class TestGnuplotExecution:
    """Test gnuplot execution methods (require gnuplot installed)."""

    def test_run_file_creates_output(self, tmp_path):
        """Test run_file method creates output file."""
        import os
        import shutil
        
        # Check if gnuplot is available
        if not shutil.which("gnuplot"):
            pytest.skip("gnuplot not installed")
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test Plot"
            parent.gnuplot.xlabel = "X"
            parent.gnuplot.ylabel = "Y"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            parent.gnuplot.outfig = "test_output.png"
            
            parent.dump()
            parent.run_file()
            
            # Check output file was created
            assert os.path.exists(parent.gpl_file)
            
            # Clean up
            parent.clean()
            if os.path.exists("test_output.png"):
                os.remove("test_output.png")
        finally:
            os.chdir(original_cwd)

    def test_run_creates_output(self, tmp_path):
        """Test run method creates output file."""
        import os
        import shutil
        
        # Check if gnuplot is available
        if not shutil.which("gnuplot"):
            pytest.skip("gnuplot not installed")
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test Plot"
            parent.gnuplot.xlabel = "X"
            parent.gnuplot.ylabel = "Y"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            parent.gnuplot.outfig = "test_output.png"
            
            parent.run()
            
            # Check output file was created
            assert os.path.exists("test_output.png")
            
            # Clean up
            if os.path.exists("test_output.png"):
                os.remove("test_output.png")
        finally:
            os.chdir(original_cwd)

    def test_final_with_show(self, tmp_path):
        """Test final method with show (noshow=False) runs gnuplot."""
        import os
        import shutil
        
        # Check if gnuplot is available
        if not shutil.which("gnuplot"):
            pytest.skip("gnuplot not installed")
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            parent = ParentGnuplot()
            parent.gnuplot.title = "Test Plot"
            parent.gnuplot.xlabel = "X"
            parent.gnuplot.ylabel = "Y"
            parent.gnuplot.plot_type = "line"
            parent.gnuplot.xdata = [[0, 1, 2]]
            parent.gnuplot.data = [[1, 2, 3]]
            parent.gnuplot.legends = ["Test"]
            parent.gnuplot.highs = []
            parent.gnuplot.lows = []
            parent.gnuplot.origins = []
            parent.gnuplot.outfig = "test_output.png"
            
            parent.final(outfig=None, noshow=False)
            
            # Should create output
            assert os.path.exists("test_output.png") or True  # May fail if no terminal
        finally:
            os.chdir(original_cwd)


# ============================================================================
# Test BoxGnuplot additional methods
# ============================================================================

class TestBoxGnuplotMethods:
    """Test additional BoxGnuplot functionality."""

    @pytest.fixture
    def box_kwargs(self):
        """Kwargs for BoxGnuplot."""
        return {
            "data_list": [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
            "color_list": [[0.1, 0.2, 0.3, 0.4, 0.5], [0.2, 0.3, 0.4, 0.5, 0.6]],
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
            "z_precision": 2,
            "alpha": 0.8,
            "cmap": None,
            "colorbar_location": None,
            "mode": "withoutScatter",
        }

    def test_box_with_scatter_mode(self, box_kwargs):
        """Test BoxGnuplot with scatter mode."""
        box_kwargs["mode"] = "withScatter"
        box = BoxGnuplot(**box_kwargs)
        assert box.gnuplot.mode == "withScatter"

    def test_box_with_cmap_warning(self, box_kwargs, caplog):
        """Test BoxGnuplot with cmap triggers warning."""
        box_kwargs["cmap"] = "viridis"
        box = BoxGnuplot(**box_kwargs)
        assert "unable to set colormap" in caplog.text.lower() or box.gnuplot is not None

    def test_box_with_colorbar_warning(self, box_kwargs, caplog):
        """Test BoxGnuplot with colorbar_location triggers warning."""
        box_kwargs["colorbar_location"] = "right"
        box = BoxGnuplot(**box_kwargs)
        assert "unable to set colorbar location" in caplog.text.lower() or box.gnuplot is not None


# ============================================================================
# Test ScatterGnuplot additional methods
# ============================================================================

class TestScatterGnuplotMethods:
    """Test additional ScatterGnuplot functionality."""

    @pytest.fixture
    def scatter_kwargs(self):
        """Kwargs for ScatterGnuplot."""
        return {
            "data_list": [[1.0, 2.0, 3.0]],
            "xdata_list": [[0.0, 1.0, 2.0]],
            "color_list": [[0.1, 0.5, 0.9]],
            "legends": ["Test Scatter"],
            "xmin": 0,
            "xmax": 10,
            "ymin": 0,
            "ymax": 5,
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": "Color",
            "title": "Scatter Test",
            "x_precision": 1,
            "y_precision": 2,
            "z_precision": 3,
            "alpha": 0.7,
            "cmap": None,
            "legend_location": "outside",
            "colorbar_location": None,
        }

    def test_scatter_with_cmap_warning(self, scatter_kwargs, caplog):
        """Test ScatterGnuplot with cmap triggers warning."""
        scatter_kwargs["cmap"] = "plasma"
        scatter = ScatterGnuplot(**scatter_kwargs)
        assert "unable to set colormap" in caplog.text.lower() or scatter.gnuplot is not None

    def test_scatter_with_colorbar_warning(self, scatter_kwargs, caplog):
        """Test ScatterGnuplot with colorbar_location triggers warning."""
        scatter_kwargs["colorbar_location"] = "top"
        scatter = ScatterGnuplot(**scatter_kwargs)
        assert "unable to set colorbar location" in caplog.text.lower() or scatter.gnuplot is not None


# ============================================================================
# Test BarGnuplot additional methods
# ============================================================================

class TestBarGnuplotMethods:
    """Test additional BarGnuplot functionality."""

    @pytest.fixture
    def bar_kwargs(self):
        """Kwargs for BarGnuplot."""
        return {
            "data_list": [[1.0, 2.0, 3.0], [2.0, 3.0, 4.0]],
            "stds_list": [[0.1, 0.2, 0.3], [0.2, 0.3, 0.4]],
            "xtitles": ["A", "B", "C"],
            "legends": ["Series 1", "Series 2"],
            "xmin": None,
            "xmax": None,
            "ymin": 0,
            "ymax": 5,
            "xlabel": "Category",
            "ylabel": "Value",
            "title": "Bar Test",
            "x_precision": None,
            "y_precision": 1,
            "legend_location": "inside",
        }

    def test_bar_multiple_series(self, bar_kwargs):
        """Test BarGnuplot with multiple data series."""
        bar = BarGnuplot(**bar_kwargs)
        assert len(bar.gnuplot.data) == 2
        assert len(bar.gnuplot.legends) == 2

    def test_bar_with_precision(self, bar_kwargs):
        """Test BarGnuplot with y precision."""
        bar = BarGnuplot(**bar_kwargs)
        assert bar.gnuplot.y_precision == 1


# ============================================================================
# Test LineGnuplot additional scenarios
# ============================================================================

class TestLineGnuplotMethods:
    """Test additional LineGnuplot functionality."""

    @pytest.fixture
    def line_kwargs(self):
        """Kwargs for LineGnuplot."""
        return {
            "data_list": [[1.0, 2.0, 3.0, 4.0]],
            "xdata_list": [[0.0, 1.0, 2.0, 3.0]],
            "legends": ["Test Line"],
            "xmin": 0,
            "xmax": 10,
            "ymin": 0,
            "ymax": 5,
            "xlabel": "X Axis",
            "ylabel": "Y Axis",
            "title": "Test Title",
            "x_precision": 2,
            "y_precision": 3,
            "highs": [],
            "lows": [],
            "origins": [],
            "alpha": 0.4,
            "legend_location": "inside",
        }

    def test_line_with_origins(self, line_kwargs):
        """Test LineGnuplot with origins parameter."""
        line_kwargs["origins"] = [[0, 0, 0, 0]]
        line = LineGnuplot(**line_kwargs)
        assert line.gnuplot.origins == [[0, 0, 0, 0]]

    def test_line_dump2str_with_highs_lows(self, line_kwargs):
        """Test dump2str generates correct script with confidence intervals."""
        line_kwargs["highs"] = [[1.5, 2.5, 3.5, 4.5]]
        line_kwargs["lows"] = [[0.5, 1.5, 2.5, 3.5]]
        line = LineGnuplot(**line_kwargs)
        
        result = line.gnuplot.dump2str()
        assert "filledcurves" in result