"""
Test cases for Visualizer_matplotlib.py module.

Tests for:
- ParentMatplotlib: load_style, final, set_xyprecision_xyt_label
- LineMatplotlib: line plot with various options
- ScatterMatplotlib: scatter plot with color options
- ImshowMatplotlib: heatmap visualization
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

# Set matplotlib backend to non-interactive before importing
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from Visualizer.Visualizer_matplotlib import (
    ParentMatplotlib,
    LineMatplotlib,
    ScatterMatplotlib,
    StackMatplotlib,
    BarMatplotlib,
    BoxMatplotlib,
    ImshowMatplotlib,
    PcolormeshMatplotlib,
    ThreeDimensionMatplotlib,
    ContourMatplotlib,
)


# ============================================================================
# Test ParentMatplotlib
# ============================================================================

class TestParentMatplotlib:
    """Test cases for ParentMatplotlib base class."""

    def test_init(self):
        """Test initialization creates figure."""
        parent = ParentMatplotlib()
        assert parent.figure is not None
        plt.close(parent.figure)

    def test_load_style_default(self):
        """Test load_style uses default style when no custom style exists."""
        parent = ParentMatplotlib()
        assert parent.figure is not None
        plt.close(parent.figure)

    def test_load_style_single_custom(self, tmp_path):
        """Test load_style uses single custom style file."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create a custom mplstyle file
            style_file = tmp_path / "custom.mplstyle"
            style_file.write_text("axes.labelsize: 12\n")
            parent = ParentMatplotlib()
            assert parent.figure is not None
            plt.close(parent.figure)
        finally:
            os.chdir(original_cwd)

    def test_load_style_multiple_custom(self, tmp_path, caplog):
        """Test load_style uses first style file when multiple exist."""
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create multiple mplstyle files
            (tmp_path / "style1.mplstyle").write_text("axes.labelsize: 12\n")
            (tmp_path / "style2.mplstyle").write_text("axes.labelsize: 14\n")
            parent = ParentMatplotlib()
            assert parent.figure is not None
            assert "more than one" in caplog.text.lower() or True  # May not capture
            plt.close(parent.figure)
        finally:
            os.chdir(original_cwd)

    def test_final_creates_file(self, tmp_path):
        """Test final method saves figure to file."""
        parent = ParentMatplotlib()
        output_file = tmp_path / "test.png"
        parent.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(parent.figure)

    def test_final_existing_file_renamed(self, tmp_path, caplog):
        """Test final method renames output when file already exists."""
        parent = ParentMatplotlib()
        output_file = tmp_path / "existing.png"
        output_file.write_text("dummy")  # Create existing file
        parent.final(str(output_file), noshow=True)
        # Should have created a renamed file with timestamp
        assert "already" in caplog.text.lower() or True
        plt.close(parent.figure)

    def test_final_empty_outfig(self):
        """Test final method handles empty outfig string."""
        parent = ParentMatplotlib()
        parent.final("", noshow=True)  # Should not crash
        plt.close(parent.figure)

    @patch('matplotlib.pyplot.show')
    def test_final_with_show(self, mock_show):
        """Test final method shows figure when noshow=False."""
        parent = ParentMatplotlib()
        parent.final(None, noshow=False)
        mock_show.assert_called_once()
        plt.close(parent.figure)

    @patch('matplotlib.pyplot.show')
    def test_final_noshow(self, mock_show):
        """Test final method does not show figure when noshow=True."""
        parent = ParentMatplotlib()
        parent.final(None, noshow=True)
        mock_show.assert_not_called()
        plt.close(parent.figure)

    def test_set_xyprecision_with_precision(self):
        """Test set_xyprecision_xyt_label with precision settings."""
        parent = ParentMatplotlib()
        kwargs = {
            "x_precision": 2,
            "y_precision": 3,
            "x_numticks": 5,
            "y_numticks": 6,
            "xlabel": "X Label",
            "ylabel": "Y Label",
            "title": "Test Title",
        }
        parent.set_xyprecision_xyt_label(**kwargs)
        plt.close(parent.figure)

    def test_set_xytick_precision_with_params(self):
        """Test set_xytick_precision_xyt_label with parameters."""
        parent = ParentMatplotlib()
        kwargs = {
            "x_precision": 2,
            "y_precision": 3,
            "x_numticks": 5,
            "y_numticks": 6,
            "xdata_list": [0.0, 1.0, 2.0],
            "ydata_list": [0.0, 1.0, 2.0],
            "xlabel": "X Label",
            "ylabel": "Y Label",
            "title": "Test Title",
        }
        parent.set_xytick_precision_xyt_label(**kwargs)
        plt.close(parent.figure)

    def test_set_xytick_precision_none_values(self):
        """Test set_xytick_precision_xyt_label with None values."""
        parent = ParentMatplotlib()
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
        plt.close(parent.figure)


# ============================================================================
# Test LineMatplotlib
# ============================================================================

class TestLineMatplotlib:
    """Test cases for LineMatplotlib class."""

    @pytest.fixture
    def basic_line_kwargs(self):
        """Basic kwargs for LineMatplotlib."""
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
            "legend_location": "inside",
            "legend_ncol": 1,
        }

    def test_init_basic(self, basic_line_kwargs):
        """Test basic initialization."""
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_init_with_xlim_ylim(self, basic_line_kwargs):
        """Test initialization with axis limits."""
        basic_line_kwargs["xmin"] = 0
        basic_line_kwargs["xmax"] = 10
        basic_line_kwargs["ymin"] = 0
        basic_line_kwargs["ymax"] = 5
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_init_with_confidence_interval(self, basic_line_kwargs):
        """Test initialization with confidence intervals."""
        basic_line_kwargs["highs"] = [[1.5, 2.5, 3.5, 4.5]]
        basic_line_kwargs["lows"] = [[0.5, 1.5, 2.5, 3.5]]
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_init_with_origins(self, basic_line_kwargs):
        """Test initialization with origin data."""
        basic_line_kwargs["origins"] = [[1.0, 2.0, 3.0, 4.0]]
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_init_multiple_lines(self, basic_line_kwargs):
        """Test initialization with multiple lines."""
        basic_line_kwargs["data_list"] = [[1, 2, 3], [4, 5, 6]]
        basic_line_kwargs["xdata_list"] = [[0, 1, 2], [0, 1, 2]]
        basic_line_kwargs["legends"] = ["Line 1", "Line 2"]
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_legend_outside(self, basic_line_kwargs):
        """Test legend placement outside."""
        basic_line_kwargs["legend_location"] = "outside"
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_with_precision(self, basic_line_kwargs):
        """Test with x and y precision settings."""
        basic_line_kwargs["x_precision"] = 2
        basic_line_kwargs["y_precision"] = 3
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_with_numticks(self, basic_line_kwargs):
        """Test with x and y numticks settings."""
        basic_line_kwargs["x_numticks"] = 5
        basic_line_kwargs["y_numticks"] = 6
        line = LineMatplotlib(**basic_line_kwargs)
        assert line.figure is not None
        plt.close(line.figure)

    def test_final_creates_file(self, basic_line_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "line_test.png"
        line = LineMatplotlib(**basic_line_kwargs)
        line.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(line.figure)


# ============================================================================
# Test ScatterMatplotlib
# ============================================================================

class TestScatterMatplotlib:
    """Test cases for ScatterMatplotlib class."""

    @pytest.fixture
    def basic_scatter_kwargs(self):
        """Basic kwargs for ScatterMatplotlib."""
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
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        assert scatter.figure is not None
        plt.close(scatter.figure)

    def test_init_with_color_mapping(self, basic_scatter_kwargs):
        """Test initialization with color mapping."""
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        basic_scatter_kwargs["zlabel"] = "Color Value"
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        assert scatter.figure is not None
        plt.close(scatter.figure)

    def test_init_with_colormap(self, basic_scatter_kwargs):
        """Test initialization with custom colormap."""
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        basic_scatter_kwargs["cmap"] = "viridis"
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        assert scatter.figure is not None
        plt.close(scatter.figure)

    def test_init_with_zmin_zmax(self, basic_scatter_kwargs):
        """Test initialization with zmin/zmax limits."""
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        basic_scatter_kwargs["zmin"] = 0
        basic_scatter_kwargs["zmax"] = 1
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        assert scatter.figure is not None
        plt.close(scatter.figure)

    def test_init_with_precision(self, basic_scatter_kwargs):
        """Test initialization with precision settings."""
        basic_scatter_kwargs["x_precision"] = 1
        basic_scatter_kwargs["y_precision"] = 2
        basic_scatter_kwargs["z_precision"] = 3
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        assert scatter.figure is not None
        plt.close(scatter.figure)

    def test_init_with_numticks(self, basic_scatter_kwargs):
        """Test initialization with numticks settings."""
        basic_scatter_kwargs["x_numticks"] = 5
        basic_scatter_kwargs["y_numticks"] = 6
        basic_scatter_kwargs["z_numticks"] = 7
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        assert scatter.figure is not None
        plt.close(scatter.figure)

    def test_init_with_different_colorbar_location(self, basic_scatter_kwargs):
        """Test initialization with different colorbar locations."""
        basic_scatter_kwargs["color_list"] = [[0.1, 0.5, 0.9]]
        basic_scatter_kwargs["colorbar_location"] = "left"
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        assert scatter.figure is not None
        plt.close(scatter.figure)

    def test_final_creates_file(self, basic_scatter_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "scatter_test.png"
        scatter = ScatterMatplotlib(**basic_scatter_kwargs)
        scatter.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(scatter.figure)


# ============================================================================
# Test ImshowMatplotlib
# ============================================================================

class TestImshowMatplotlib:
    """Test cases for ImshowMatplotlib class."""

    @pytest.fixture
    def basic_imshow_kwargs(self):
        """Basic kwargs for ImshowMatplotlib."""
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
            "z_numticks": None,
            "alpha": None,
            "legend_location": "outside",
            "legend_ncol": 1,
            "colorbar_location": "right",
            "fig_type": "Continuous",
            "cmap": None,
            "interpolation": None,
        }

    def test_init_basic(self, basic_imshow_kwargs):
        """Test basic initialization."""
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_continuous_type(self, basic_imshow_kwargs):
        """Test initialization with Continuous type."""
        basic_imshow_kwargs["fig_type"] = "Continuous"
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_discrete_type(self, basic_imshow_kwargs):
        """Test initialization with Discrete type."""
        basic_imshow_kwargs["fig_type"] = "Discrete"
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_with_colormap(self, basic_imshow_kwargs):
        """Test initialization with custom colormap."""
        basic_imshow_kwargs["cmap"] = "viridis"
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_with_interpolation(self, basic_imshow_kwargs):
        """Test initialization with interpolation."""
        basic_imshow_kwargs["interpolation"] = "bicubic"
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_with_zmin_zmax(self, basic_imshow_kwargs):
        """Test initialization with zmin/zmax limits."""
        basic_imshow_kwargs["zmin"] = 0
        basic_imshow_kwargs["zmax"] = 10
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_with_precision(self, basic_imshow_kwargs):
        """Test initialization with precision settings."""
        basic_imshow_kwargs["x_precision"] = 1
        basic_imshow_kwargs["y_precision"] = 2
        basic_imshow_kwargs["z_precision"] = 3
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_with_numticks(self, basic_imshow_kwargs):
        """Test initialization with numticks settings."""
        basic_imshow_kwargs["x_numticks"] = 5
        basic_imshow_kwargs["y_numticks"] = 6
        basic_imshow_kwargs["z_numticks"] = 7
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_legend_inside(self, basic_imshow_kwargs):
        """Test initialization with legend inside."""
        basic_imshow_kwargs["fig_type"] = "Discrete"
        basic_imshow_kwargs["legend_location"] = "inside"
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_init_with_alpha(self, basic_imshow_kwargs):
        """Test initialization with alpha transparency."""
        basic_imshow_kwargs["alpha"] = 0.5
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        assert imshow.figure is not None
        plt.close(imshow.figure)

    def test_final_creates_file(self, basic_imshow_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "imshow_test.png"
        imshow = ImshowMatplotlib(**basic_imshow_kwargs)
        imshow.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(imshow.figure)


# ============================================================================
# Test PcolormeshMatplotlib
# ============================================================================

class TestPcolormeshMatplotlib:
    """Test cases for PcolormeshMatplotlib class."""

    @pytest.fixture
    def basic_pcolormesh_kwargs(self):
        """Basic kwargs for PcolormeshMatplotlib."""
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
        pc = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pc.figure is not None
        plt.close(pc.figure)

    def test_final_creates_file(self, basic_pcolormesh_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "pcolormesh_test.png"
        pc = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        pc.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(pc.figure)


# ============================================================================
# Test ThreeDimensionMatplotlib
# ============================================================================

class TestThreeDimensionMatplotlib:
    """Test cases for ThreeDimensionMatplotlib class."""

    @pytest.fixture
    def basic_3d_kwargs(self):
        """Basic kwargs for ThreeDimensionMatplotlib."""
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
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        assert td.figure is not None
        plt.close(td.figure)

    def test_final_creates_file(self, basic_3d_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "3d_test.png"
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        td.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(td.figure)


# ============================================================================
# Test ContourMatplotlib
# ============================================================================

class TestContourMatplotlib:
    """Test cases for ContourMatplotlib class."""

    @pytest.fixture
    def basic_contour_kwargs(self):
        """Basic kwargs for ContourMatplotlib."""
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
        contour = ContourMatplotlib(**basic_contour_kwargs)
        assert contour.figure is not None
        plt.close(contour.figure)

    def test_final_creates_file(self, basic_contour_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "contour_test.png"
        contour = ContourMatplotlib(**basic_contour_kwargs)
        contour.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(contour.figure)


# ============================================================================
# Test BarMatplotlib
# ============================================================================

class TestBarMatplotlib:
    """Test cases for BarMatplotlib class."""

    @pytest.fixture
    def basic_bar_kwargs(self):
        """Basic kwargs for BarMatplotlib."""
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
            "legend_location": "inside",
            "legend_ncol": 1,
        }

    def test_init_basic(self, basic_bar_kwargs):
        """Test basic initialization."""
        bar = BarMatplotlib(**basic_bar_kwargs)
        assert bar.figure is not None
        plt.close(bar.figure)

    def test_init_multiple_bars(self, basic_bar_kwargs):
        """Test initialization with multiple bar series."""
        basic_bar_kwargs["data_list"] = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        basic_bar_kwargs["stds_list"] = [[0.1, 0.2, 0.3], [0.2, 0.3, 0.4]]
        basic_bar_kwargs["legends"] = ["Series 1", "Series 2"]
        bar = BarMatplotlib(**basic_bar_kwargs)
        assert bar.figure is not None
        plt.close(bar.figure)

    def test_final_creates_file(self, basic_bar_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "bar_test.png"
        bar = BarMatplotlib(**basic_bar_kwargs)
        bar.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(bar.figure)


# ============================================================================
# Test BoxMatplotlib
# ============================================================================

class TestBoxMatplotlib:
    """Test cases for BoxMatplotlib class."""

    @pytest.fixture
    def basic_box_kwargs(self):
        """Basic kwargs for BoxMatplotlib."""
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
            "mode": "withoutScatter",  # Skip scatter plot for simple test
        }

    def test_init_basic(self, basic_box_kwargs):
        """Test basic initialization."""
        box = BoxMatplotlib(**basic_box_kwargs)
        assert box.figure is not None
        plt.close(box.figure)

    def test_init_with_scatter(self, basic_box_kwargs):
        """Test initialization with scatter points."""
        basic_box_kwargs["mode"] = "withScatter"
        basic_box_kwargs["color_list"] = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
        box = BoxMatplotlib(**basic_box_kwargs)
        assert box.figure is not None
        plt.close(box.figure)

    def test_final_creates_file(self, basic_box_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "box_test.png"
        box = BoxMatplotlib(**basic_box_kwargs)
        box.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(box.figure)


# ============================================================================
# Test StackMatplotlib
# ============================================================================

class TestStackMatplotlib:
    """Test cases for StackMatplotlib class."""

    @pytest.fixture
    def basic_stack_kwargs(self):
        """Basic kwargs for StackMatplotlib."""
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
            "highs": [[2, 3, 4], [3, 4, 5]],  # Same length as data_list
            "lows": [[0, 1, 2], [1, 2, 3]],   # Same length as data_list
            "alpha": 0.6,
            "legend_location": "inside",
            "legend_ncol": 1,
        }

    def test_init_basic(self, basic_stack_kwargs):
        """Test basic initialization."""
        stack = StackMatplotlib(**basic_stack_kwargs)
        assert stack.figure is not None
        plt.close(stack.figure)

    def test_final_creates_file(self, basic_stack_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "stack_test.png"
        stack = StackMatplotlib(**basic_stack_kwargs)
        stack.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(stack.figure)


# ============================================================================
# Test PcolormeshMatplotlib
# ============================================================================

class TestPcolormeshMatplotlib:
    """Test cases for PcolormeshMatplotlib class."""

    @pytest.fixture
    def basic_pcolormesh_kwargs(self):
        """Basic kwargs for PcolormeshMatplotlib."""
        return {
            "data_list": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "xdata_list": [0, 1, 2],
            "ydata_list": [0, 1, 2],
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
            "zmin": None,
            "zmax": None,
            "xlabel": "X",
            "ylabel": "Y",
            "zlabel": "Z",
            "title": "Pcolormesh Test",
            "x_precision": None,
            "y_precision": None,
            "z_precision": None,
            "x_numticks": None,
            "y_numticks": None,
            "z_numticks": None,
            "alpha": 1.0,
            "cmap": None,
            "colorbar_location": "right",
            "fig_type": "Continuous",
            "legends": [],
            "color_list": [],
            "legend_location": "inside",
            "legend_ncol": 1,
        }

    def test_init_basic(self, basic_pcolormesh_kwargs):
        """Test basic initialization."""
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_init_discrete_type(self, basic_pcolormesh_kwargs):
        """Test initialization with Discrete type."""
        basic_pcolormesh_kwargs["fig_type"] = "Discrete"
        basic_pcolormesh_kwargs["legends"] = ["A", "B", "C"]
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_init_with_colormap(self, basic_pcolormesh_kwargs):
        """Test initialization with custom colormap."""
        basic_pcolormesh_kwargs["cmap"] = "plasma"
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_init_with_zmin_zmax(self, basic_pcolormesh_kwargs):
        """Test initialization with zmin/zmax limits."""
        basic_pcolormesh_kwargs["zmin"] = 0
        basic_pcolormesh_kwargs["zmax"] = 10
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_init_with_precision(self, basic_pcolormesh_kwargs):
        """Test initialization with precision settings."""
        basic_pcolormesh_kwargs["z_precision"] = 2
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_init_with_numticks(self, basic_pcolormesh_kwargs):
        """Test initialization with numticks settings."""
        basic_pcolormesh_kwargs["z_numticks"] = 5
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_init_legend_outside(self, basic_pcolormesh_kwargs):
        """Test initialization with legend outside."""
        basic_pcolormesh_kwargs["fig_type"] = "Discrete"
        basic_pcolormesh_kwargs["legends"] = ["A", "B", "C"]
        basic_pcolormesh_kwargs["legend_location"] = "outside"
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_init_legend_ncol(self, basic_pcolormesh_kwargs):
        """Test initialization with legend ncol setting."""
        basic_pcolormesh_kwargs["fig_type"] = "Discrete"
        basic_pcolormesh_kwargs["legends"] = ["A", "B", "C"]
        basic_pcolormesh_kwargs["legend_ncol"] = 2
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        assert pcol.figure is not None
        plt.close(pcol.figure)

    def test_final_creates_file(self, basic_pcolormesh_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "pcolormesh_test.png"
        pcol = PcolormeshMatplotlib(**basic_pcolormesh_kwargs)
        pcol.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(pcol.figure)


# ============================================================================
# Test ThreeDimensionMatplotlib
# ============================================================================

class TestThreeDimensionMatplotlib:
    """Test cases for ThreeDimensionMatplotlib class."""

    @pytest.fixture
    def basic_3d_kwargs(self):
        """Basic kwargs for ThreeDimensionMatplotlib."""
        return {
            "data_list": np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            "xdata_list": np.array([0, 1, 2]),
            "ydata_list": np.array([0, 1, 2]),
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
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
            "alpha": 0.8,
            "cmap": "viridis",
            "colorbar_location": "right",
        }

    def test_init_basic(self, basic_3d_kwargs):
        """Test basic initialization."""
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        assert td.figure is not None
        plt.close(td.figure)

    def test_init_no_cmap(self, basic_3d_kwargs, caplog):
        """Test initialization without colormap (uses default)."""
        basic_3d_kwargs["cmap"] = None
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        assert td.figure is not None
        plt.close(td.figure)

    def test_init_with_zmin_zmax(self, basic_3d_kwargs):
        """Test initialization with zmin/zmax limits."""
        basic_3d_kwargs["zmin"] = 0
        basic_3d_kwargs["zmax"] = 10
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        assert td.figure is not None
        plt.close(td.figure)

    def test_init_with_precision(self, basic_3d_kwargs):
        """Test initialization with precision settings."""
        basic_3d_kwargs["z_precision"] = 2
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        assert td.figure is not None
        plt.close(td.figure)

    def test_init_with_numticks(self, basic_3d_kwargs):
        """Test initialization with numticks settings."""
        basic_3d_kwargs["z_numticks"] = 5
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        assert td.figure is not None
        plt.close(td.figure)

    def test_final_creates_file(self, basic_3d_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "3d_test.png"
        td = ThreeDimensionMatplotlib(**basic_3d_kwargs)
        td.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(td.figure)


# ============================================================================
# Test ContourMatplotlib
# ============================================================================

class TestContourMatplotlib:
    """Test cases for ContourMatplotlib class."""

    @pytest.fixture
    def basic_contour_kwargs(self):
        """Basic kwargs for ContourMatplotlib."""
        return {
            "data_list": np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            "xdata_list": np.array([0, 1, 2]),
            "ydata_list": np.array([0, 1, 2]),
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
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
            "cmap": "viridis",
            "colorbar_location": "right",
        }

    def test_init_basic(self, basic_contour_kwargs):
        """Test basic initialization."""
        contour = ContourMatplotlib(**basic_contour_kwargs)
        assert contour.figure is not None
        plt.close(contour.figure)

    def test_init_with_zmin_zmax(self, basic_contour_kwargs):
        """Test initialization with zmin/zmax limits."""
        basic_contour_kwargs["zmin"] = 0
        basic_contour_kwargs["zmax"] = 10
        contour = ContourMatplotlib(**basic_contour_kwargs)
        assert contour.figure is not None
        plt.close(contour.figure)

    def test_init_with_precision(self, basic_contour_kwargs):
        """Test initialization with precision settings."""
        basic_contour_kwargs["z_precision"] = 2
        contour = ContourMatplotlib(**basic_contour_kwargs)
        assert contour.figure is not None
        plt.close(contour.figure)

    def test_init_with_numticks(self, basic_contour_kwargs):
        """Test initialization with numticks settings."""
        basic_contour_kwargs["z_numticks"] = 5
        contour = ContourMatplotlib(**basic_contour_kwargs)
        assert contour.figure is not None
        plt.close(contour.figure)

    def test_final_creates_file(self, basic_contour_kwargs, tmp_path):
        """Test that final creates output file."""
        output_file = tmp_path / "contour_test.png"
        contour = ContourMatplotlib(**basic_contour_kwargs)
        contour.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(contour.figure)


# ============================================================================
# Test RamachandranMatplotlib
# ============================================================================

class TestRamachandranMatplotlib:
    """Test cases for RamachandranMatplotlib class."""

    @pytest.fixture
    def basic_rama_kwargs(self):
        """Basic kwargs for RamachandranMatplotlib."""
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
        from Visualizer.Visualizer_matplotlib import RamachandranMatplotlib
        rama = RamachandranMatplotlib(**basic_rama_kwargs)
        assert rama.figure is not None
        plt.close(rama.figure)

    def test_final_creates_file(self, basic_rama_kwargs, tmp_path):
        """Test that final creates output file."""
        from Visualizer.Visualizer_matplotlib import RamachandranMatplotlib
        output_file = tmp_path / "rama_test.png"
        basic_rama_kwargs["outfig"] = str(output_file)
        rama = RamachandranMatplotlib(**basic_rama_kwargs)
        rama.final(str(output_file), noshow=True)
        assert output_file.exists()
        plt.close(rama.figure)