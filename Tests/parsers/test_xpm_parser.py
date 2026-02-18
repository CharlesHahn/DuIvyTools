"""
Test cases for xpmParser.py module.

Tests for:
- XPM class: initialization, parsing, save, subtraction, refresh_by_value_matrix
- XPMS class: multi-frame xpm parsing
"""

import os
import sys
import pytest
import tempfile
import numpy as np

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from FileParser.xpmParser import XPM, XPMS


class TestXPMInitContinuous:
    """Test cases for XPM class initialization with Continuous type."""

    def test_xpm_init_continuous(self, sample_xpm_continuous):
        """Test Continuous type XPM parsing."""
        xpm = XPM(sample_xpm_continuous)
        
        assert xpm.xpmfile == sample_xpm_continuous
        assert xpm.title == "Gibbs Energy Landscape"
        assert xpm.legend == "G (kJ/mol)"
        assert xpm.type == "Continuous"
        assert xpm.xlabel == "PC1"
        assert xpm.ylabel == "PC2"

    def test_xpm_continuous_dimensions(self, sample_xpm_continuous):
        """Test Continuous XPM dimensions."""
        xpm = XPM(sample_xpm_continuous)
        
        assert xpm.width == 32
        assert xpm.height == 32
        assert xpm.color_num == 100
        assert xpm.char_per_pixel == 2

    def test_xpm_continuous_chars(self, sample_xpm_continuous):
        """Test Continuous XPM character extraction."""
        xpm = XPM(sample_xpm_continuous)
        
        assert len(xpm.chars) == 100
        assert xpm.chars[0] == "AA"
        assert xpm.chars[1] == "BA"

    def test_xpm_continuous_colors(self, sample_xpm_continuous):
        """Test Continuous XPM color extraction."""
        xpm = XPM(sample_xpm_continuous)
        
        assert len(xpm.colors) == 100
        assert xpm.colors[0] == "#000000"
        # Colors should be hex format

    def test_xpm_continuous_notes(self, sample_xpm_continuous):
        """Test Continuous XPM note (value) extraction."""
        xpm = XPM(sample_xpm_continuous)
        
        assert len(xpm.notes) == 100
        # Notes should be floats for Continuous type
        assert isinstance(xpm.notes[0], float)
        assert xpm.notes[0] == 0.0

    def test_xpm_continuous_axis(self, sample_xpm_continuous):
        """Test Continuous XPM axis extraction."""
        xpm = XPM(sample_xpm_continuous)
        
        assert len(xpm.xaxis) == 32
        assert len(xpm.yaxis) == 32
        # yaxis should be reversed (high to low)
        assert xpm.yaxis[0] > xpm.yaxis[-1]

    def test_xpm_continuous_value_matrix(self, sample_xpm_continuous):
        """Test Continuous XPM value matrix."""
        xpm = XPM(sample_xpm_continuous)
        
        assert len(xpm.value_matrix) == 32
        assert len(xpm.value_matrix[0]) == 32
        # All values should be floats
        assert isinstance(xpm.value_matrix[0][0], float)

    def test_xpm_continuous_dot_matrix(self, sample_xpm_continuous):
        """Test Continuous XPM dot matrix."""
        xpm = XPM(sample_xpm_continuous)
        
        assert len(xpm.dot_matrix) == 32
        assert len(xpm.dot_matrix[0]) == 32
        # Each dot should be 2 characters
        assert len(xpm.dot_matrix[0][0]) == 2


class TestXPMInitDiscrete:
    """Test cases for XPM class initialization with Discrete type."""

    def test_xpm_init_discrete(self, sample_xpm_discrete):
        """Test Discrete type XPM parsing."""
        xpm = XPM(sample_xpm_discrete)
        
        assert xpm.xpmfile == sample_xpm_discrete
        assert xpm.title == "Hydrogen Bond Existence Map"
        assert xpm.legend == "Hydrogen Bonds"
        assert xpm.type == "Discrete"
        assert xpm.xlabel == "Time (ps)"
        assert xpm.ylabel == "Hydrogen Bond Index"

    def test_xpm_discrete_dimensions(self, sample_xpm_discrete):
        """Test Discrete XPM dimensions."""
        xpm = XPM(sample_xpm_discrete)
        
        assert xpm.width == 4001
        assert xpm.height == 8
        assert xpm.color_num == 2
        assert xpm.char_per_pixel == 1

    def test_xpm_discrete_chars(self, sample_xpm_discrete):
        """Test Discrete XPM character extraction."""
        xpm = XPM(sample_xpm_discrete)
        
        assert len(xpm.chars) == 2
        assert " " in xpm.chars or "o" in xpm.chars

    def test_xpm_discrete_colors(self, sample_xpm_discrete):
        """Test Discrete XPM color extraction."""
        xpm = XPM(sample_xpm_discrete)
        
        assert len(xpm.colors) == 2
        # Should have white and red
        assert "#FFFFFF" in xpm.colors or "#FF0000" in xpm.colors

    def test_xpm_discrete_notes(self, sample_xpm_discrete):
        """Test Discrete XPM note extraction."""
        xpm = XPM(sample_xpm_discrete)
        
        assert len(xpm.notes) == 2
        # Notes should be strings for Discrete type
        assert "None" in xpm.notes or "Present" in xpm.notes

    def test_xpm_discrete_axis(self, sample_xpm_discrete):
        """Test Discrete XPM axis extraction."""
        xpm = XPM(sample_xpm_discrete)
        
        assert len(xpm.xaxis) == 4001
        assert len(xpm.yaxis) == 8
        # Check xaxis values (time in ps)
        assert xpm.xaxis[0] == 60000

    def test_xpm_discrete_value_matrix(self, sample_xpm_discrete):
        """Test Discrete XPM value matrix."""
        xpm = XPM(sample_xpm_discrete)
        
        assert len(xpm.value_matrix) == 8
        assert len(xpm.value_matrix[0]) == 4001
        # Values should be integers (indices) for Discrete type
        assert isinstance(xpm.value_matrix[0][0], (int, np.integer))


class TestXPMNewFile:
    """Test cases for XPM class with new_file=True."""

    def test_xpm_new_file_init(self):
        """Test XPM initialization with new_file=True."""
        xpm = XPM("output.xpm", is_file=False, new_file=True)
        
        assert xpm.xpmfile == "output.xpm"
        assert xpm.width == 0
        assert xpm.height == 0
        assert xpm.color_num == 0

    def test_xpm_new_file_set_attributes(self):
        """Test setting attributes on new XPM instance."""
        xpm = XPM("output.xpm", is_file=False, new_file=True)
        
        xpm.title = "Test"
        xpm.type = "Continuous"
        xpm.xlabel = "X"
        xpm.ylabel = "Y"
        xpm.legend = "Value"
        xpm.width = 10
        xpm.height = 10
        xpm.xaxis = list(range(10))
        xpm.yaxis = list(range(10))
        xpm.value_matrix = [[i * j for j in range(10)] for i in range(10)]
        
        assert xpm.title == "Test"
        assert xpm.width == 10


class TestXPMSave:
    """Test cases for XPM save method."""

    def test_xpm_save_continuous(self, sample_xpm_continuous, tmp_path):
        """Test saving Continuous XPM to file."""
        xpm = XPM(sample_xpm_continuous)
        
        output_file = tmp_path / "output.xpm"
        xpm.save(str(output_file))
        
        assert output_file.exists()
        
        # Load saved file and verify
        xpm2 = XPM(str(output_file))
        assert xpm2.title == xpm.title
        assert xpm2.type == xpm.type
        assert xpm2.width == xpm.width
        assert xpm2.height == xpm.height

    def test_xpm_save_discrete(self, sample_xpm_discrete, tmp_path):
        """Test saving Discrete XPM to file."""
        xpm = XPM(sample_xpm_discrete)
        
        output_file = tmp_path / "output.xpm"
        xpm.save(str(output_file))
        
        assert output_file.exists()
        
        # Load saved file and verify basic attributes
        xpm2 = XPM(str(output_file))
        assert xpm2.type == "Discrete"

    def test_xpm_save_new_file(self, tmp_path):
        """Test saving a new XPM instance."""
        xpm = XPM("output.xpm", is_file=False, new_file=True)
        
        xpm.title = "Test XPM"
        xpm.type = "Continuous"
        xpm.xlabel = "X"
        xpm.ylabel = "Y"
        xpm.legend = "Value"
        xpm.width = 5
        xpm.height = 5
        xpm.xaxis = [float(i) for i in range(5)]
        xpm.yaxis = [float(i) for i in range(5)]
        xpm.value_matrix = [[float(i * j) for j in range(5)] for i in range(5)]
        
        xpm.refresh_by_value_matrix()
        
        output_file = tmp_path / "new_output.xpm"
        xpm.save(str(output_file))
        
        assert output_file.exists()


class TestXPMSubtraction:
    """Test cases for XPM __sub__ method (xpm_diff)."""

    def test_xpm_subtraction_same_file(self, sample_xpm_continuous):
        """Test XPM subtraction with same file (should result in zeros)."""
        xpm1 = XPM(sample_xpm_continuous)
        xpm2 = XPM(sample_xpm_continuous)
        
        xpm_diff = xpm1 - xpm2
        
        assert xpm_diff.width == xpm1.width
        assert xpm_diff.height == xpm1.height
        # All values should be zero (same file)
        for row in xpm_diff.value_matrix:
            for val in row:
                assert abs(val) < 1e-6

    def test_xpm_subtraction_different_values(self, sample_xpm_continuous):
        """Test XPM subtraction with modified values."""
        xpm1 = XPM(sample_xpm_continuous)
        xpm2 = XPM(sample_xpm_continuous)
        
        # Modify xpm2 values
        for h in range(xpm2.height):
            for w in range(xpm2.width):
                xpm2.value_matrix[h][w] += 1.0
        
        xpm_diff = xpm1 - xpm2
        
        # All values should be -1.0
        for row in xpm_diff.value_matrix:
            for val in row:
                assert abs(val - (-1.0)) < 1e-6

    def test_xpm_subtraction_discrete_error(self, sample_xpm_discrete):
        """Test that subtraction of Discrete XPM raises error."""
        xpm1 = XPM(sample_xpm_discrete)
        xpm2 = XPM(sample_xpm_discrete)
        
        with pytest.raises(SystemExit):
            _ = xpm1 - xpm2


class TestXPMRefreshByValueMatrix:
    """Test cases for XPM refresh_by_value_matrix method."""

    def test_xpm_refresh_basic(self):
        """Test basic refresh_by_value_matrix."""
        xpm = XPM("test.xpm", is_file=False, new_file=True)
        
        xpm.width = 3
        xpm.height = 3
        xpm.value_matrix = [
            [1.0, 2.0, 3.0],
            [2.0, 3.0, 4.0],
            [3.0, 4.0, 5.0],
        ]
        
        xpm.refresh_by_value_matrix()
        
        assert xpm.color_num == 5  # 5 unique values
        assert xpm.char_per_pixel == 1  # <= 74 unique values
        assert len(xpm.chars) == 5
        assert len(xpm.colors) == 5

    def test_xpm_refresh_many_values(self):
        """Test refresh_by_value_matrix with many unique values."""
        xpm = XPM("test.xpm", is_file=False, new_file=True)
        
        # Create matrix with many unique values (>74, needs 2 chars per pixel)
        xpm.width = 10
        xpm.height = 10
        xpm.value_matrix = [[float(i * 10 + j) for j in range(10)] for i in range(10)]
        
        xpm.refresh_by_value_matrix()
        
        assert xpm.color_num == 100
        assert xpm.char_per_pixel == 2  # >74 unique values

    def test_xpm_refresh_empty_error(self):
        """Test that refresh with empty value_matrix raises error."""
        xpm = XPM("test.xpm", is_file=False, new_file=True)
        
        xpm.width = 0
        xpm.height = 0
        xpm.value_matrix = []
        
        with pytest.raises(SystemExit):
            xpm.refresh_by_value_matrix()


class TestXPMErrorHandling:
    """Test cases for XPM error handling."""

    def test_xpm_file_not_exists(self):
        """Test error when file does not exist."""
        with pytest.raises(SystemExit):
            XPM("nonexistent_file.xpm")

    def test_xpm_wrong_suffix(self, tmp_path):
        """Test error when file has wrong suffix."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("some content")
        
        with pytest.raises(SystemExit):
            XPM(str(wrong_file))


class TestXPMInitFromContent:
    """Test cases for XPM initialization from content string."""

    def test_xpm_init_from_string(self):
        """Test XPM initialization from content string."""
        content = """/* XPM */
/* title:   "Test" */
/* legend:  "Value" */
/* x-label: "X" */
/* y-label: "Y" */
/* type:    "Continuous" */
static char *gromacs_xpm[] = {
"2 2 2 1",
"A c #000000 " /* "0" */,
"B c #FFFFFF " /* "1" */,
/* x-axis:  0 1 */
/* y-axis:  0 1 */
"AB",
"BA",
};
"""
        xpm = XPM(content, is_file=False)
        
        assert xpm.title == "Test"
        assert xpm.type == "Continuous"
        assert xpm.width == 2
        assert xpm.height == 2
        assert xpm.color_num == 2


class TestXPMS:
    """Test cases for XPMS class (multi-frame xpm)."""

    def test_xpms_init_single_frame(self, sample_xpm_continuous):
        """Test XPMS initialization with single-frame xpm."""
        xvgs = XPMS(sample_xpm_continuous)
        
        assert len(xvgs) == 1
        assert isinstance(xvgs[0], XPM)

    def test_xpms_len(self, sample_xpm_continuous):
        """Test XPMS __len__ method."""
        xvgs = XPMS(sample_xpm_continuous)
        
        assert isinstance(len(xvgs), int)
        assert len(xvgs) >= 1

    def test_xpms_getitem(self, sample_xpm_continuous):
        """Test XPMS __getitem__ method."""
        xvgs = XPMS(sample_xpm_continuous)
        
        frame = xvgs[0]
        assert isinstance(frame, XPM)
        assert frame.title == "Gibbs Energy Landscape"


class TestXPMEdgeCases:
    """Test edge cases for XPM parsing."""

    def test_xpm_yaxis_reversed(self, sample_xpm_continuous):
        """Test that yaxis is reversed (high to low)."""
        xpm = XPM(sample_xpm_continuous)
        
        # yaxis should be reversed after parsing
        for i in range(len(xpm.yaxis) - 1):
            assert xpm.yaxis[i] > xpm.yaxis[i + 1]

    def test_xpm_datalines_count(self, sample_xpm_continuous):
        """Test that datalines count matches height."""
        xpm = XPM(sample_xpm_continuous)
        
        assert len(xpm.datalines) == xpm.height

    def test_xpm_dataline_length(self, sample_xpm_continuous):
        """Test that each dataline has correct length."""
        xpm = XPM(sample_xpm_continuous)
        
        expected_length = xpm.width * xpm.char_per_pixel
        for line in xpm.datalines:
            assert len(line) == expected_length

    def test_xpm_value_matrix_consistency(self, sample_xpm_continuous):
        """Test value matrix consistency with dot matrix."""
        xpm = XPM(sample_xpm_continuous)
        
        for h in range(xpm.height):
            for w in range(xpm.width):
                dot = xpm.dot_matrix[h][w]
                value = xpm.value_matrix[h][w]
                # Value should match the note for this character
                char_index = xpm.chars.index(dot)
                assert value == xpm.notes[char_index]
