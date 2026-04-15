"""
Test cases for xvgParser.py module.

Tests for:
- XVG class: initialization, parsing, save, calc_mvave, calc_ave, check_column_index
- XVGS class: multi-frame xvg parsing
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

from FileParser.xvgParser import XVG, XVGS


class TestXVGInit:
    """Test cases for XVG class initialization."""

    def test_xvg_init_basic(self, sample_xvg_file):
        """Test basic XVG file parsing."""
        xvg = XVG(sample_xvg_file)
        
        assert xvg.xvgfile == sample_xvg_file
        assert xvg.title == "Radius of gyration (total and around axes)"
        assert xvg.xlabel == "Time (ps)"
        assert xvg.ylabel == "Rg (nm)"
        assert xvg.column_num == 5
        assert xvg.row_num == 4001

    def test_xvg_legends(self, sample_xvg_file):
        """Test legend extraction."""
        xvg = XVG(sample_xvg_file)
        
        assert len(xvg.legends) == 4
        assert xvg.legends[0] == "Rg"
        assert "Rg" in xvg.legends[1]  # Rg\sX\N

    def test_xvg_data_heads(self, sample_xvg_file):
        """Test data heads extraction."""
        xvg = XVG(sample_xvg_file)
        
        assert len(xvg.data_heads) == 5
        assert xvg.data_heads[0] == "Time (ps)"
        assert "Rg" in xvg.data_heads[1]

    def test_xvg_data_columns(self, sample_xvg_file):
        """Test data columns extraction."""
        xvg = XVG(sample_xvg_file)
        
        assert len(xvg.data_columns) == 5
        # Check first column (Time): 0, 10, 20, ... , 40000
        assert xvg.data_columns[0][0] == 0.0
        assert xvg.data_columns[0][1] == 10.0
        assert xvg.data_columns[0][-1] == 40000.0
        # Check row count
        assert len(xvg.data_columns[0]) == 4001

    def test_xvg_data_values(self, sample_xvg_file):
        """Test specific data values."""
        xvg = XVG(sample_xvg_file)
        
        # Last row values (from original test file)
        assert abs(xvg.data_columns[1][-1] - 3.77892) < 0.0001
        assert abs(xvg.data_columns[2][-1] - 3.01626) < 0.0001
        # First row values
        assert abs(xvg.data_columns[1][0] - 3.73837) < 0.0001
        assert abs(xvg.data_columns[2][0] - 2.20746) < 0.0001

    def test_xvg_init_rmsd(self, xvg_test_path):
        """Test RMSD xvg file parsing (2 columns)."""
        rmsd_file = os.path.join(xvg_test_path, "rmsd.xvg")
        xvg = XVG(rmsd_file)
        
        assert xvg.title == "RMSD"
        assert xvg.xlabel == "Time (ps)"
        assert xvg.ylabel == "RMSD (nm)"
        assert xvg.column_num == 2
        assert len(xvg.data_columns) == 2

    def test_xvg_file_not_exists(self):
        """Test error when file does not exist."""
        with pytest.raises(SystemExit):
            XVG("nonexistent_file.xvg")

    def test_xvg_wrong_suffix(self, tmp_path):
        """Test error when file has wrong suffix."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("some content")
        
        with pytest.raises(SystemExit):
            XVG(str(wrong_file))

    def test_xvg_init_from_lines(self):
        """Test XVG initialization from lines instead of file."""
        lines = [
            '@    title "Test Title"\n',
            '@    xaxis label "X"\n',
            '@    yaxis label "Y"\n',
            '1.0 2.0\n',
            '3.0 4.0\n',
        ]
        xvg = XVG(lines, is_file=False)
        
        assert xvg.title == "Test Title"
        assert xvg.xlabel == "X"
        assert xvg.ylabel == "Y"
        assert xvg.column_num == 2
        assert xvg.row_num == 2
        assert xvg.data_columns[0] == [1.0, 3.0]
        assert xvg.data_columns[1] == [2.0, 4.0]


class TestXVGNewFile:
    """Test cases for XVG class with new_file=True."""

    def test_xvg_new_file_init(self):
        """Test XVG initialization with new_file=True."""
        xvg = XVG("output.xvg", is_file=False, new_file=True)
        
        assert xvg.xvgfile == "output.xvg"
        assert xvg.column_num == 0
        assert xvg.row_num == 0
        assert len(xvg.data_columns) == 0

    def test_xvg_new_file_set_attributes(self):
        """Test setting attributes on new XVG instance."""
        xvg = XVG("output.xvg", is_file=False, new_file=True)
        
        xvg.title = "Test"
        xvg.xlabel = "Time"
        xvg.ylabel = "Value"
        xvg.legends = ["Data1", "Data2"]
        xvg.data_columns = [[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]]
        xvg.column_num = 2
        xvg.row_num = 3
        xvg.data_heads = ["Time", "Value"]
        
        assert xvg.title == "Test"
        assert xvg.column_num == 2
        assert xvg.row_num == 3


class TestXVGSave:
    """Test cases for XVG save method."""

    def test_xvg_save_basic(self, sample_xvg_file, tmp_path):
        """Test saving XVG to file."""
        xvg = XVG(sample_xvg_file)
        
        output_file = tmp_path / "output.xvg"
        xvg.save(str(output_file), check=False)
        
        assert output_file.exists()
        
        # Load saved file and verify
        xvg2 = XVG(str(output_file))
        assert xvg2.title == xvg.title
        assert xvg2.xlabel == xvg.xlabel
        assert xvg2.column_num == xvg.column_num
        assert xvg2.row_num == xvg.row_num

    def test_xvg_save_new_file(self, tmp_path):
        """Test saving a new XVG instance."""
        xvg = XVG("output.xvg", is_file=False, new_file=True)
        
        xvg.title = "Test Data"
        xvg.xlabel = "Time (ps)"
        xvg.ylabel = "Value"
        xvg.legends = ["Data1"]
        xvg.data_columns = [[0.0, 1.0, 2.0], [10.0, 20.0, 30.0]]
        xvg.column_num = 2
        xvg.row_num = 3
        xvg.data_heads = ["Time (ps)", "Value"]
        
        output_file = tmp_path / "new_output.xvg"
        xvg.save(str(output_file), check=False)
        
        assert output_file.exists()

    def test_xvg_save_empty_data_heads_error(self):
        """Test error when saving with empty data_heads."""
        xvg = XVG("output.xvg", is_file=False, new_file=True)
        xvg.data_columns = [[1.0, 2.0]]
        
        with pytest.raises(SystemExit):
            xvg.save("output.xvg", check=True)


class TestXVGCalcMvave:
    """Test cases for XVG.calc_mvave method."""

    def test_xvg_calc_mvave_basic(self, sample_xvg_file):
        """Test basic moving average calculation."""
        xvg = XVG(sample_xvg_file)
        
        mvaves, highs, lows = xvg.calc_mvave(50, 0.95, 1)
        
        assert len(mvaves) == xvg.row_num
        # First windowsize values should be NaN
        assert np.isnan(mvaves[0])
        assert np.isnan(mvaves[49])
        # Later values should be numbers
        assert not np.isnan(mvaves[50])

    def test_xvg_calc_mvave_ci(self, sample_xvg_file):
        """Test moving average with confidence interval."""
        xvg = XVG(sample_xvg_file)
        
        mvaves, highs, lows = xvg.calc_mvave(50, 0.95, 1, calc_CI=True)
        
        # Check that highs > lows for non-NaN values
        for i in range(50, len(mvaves)):
            assert highs[i] > lows[i]
            assert highs[i] > mvaves[i]
            assert lows[i] < mvaves[i]

    def test_xvg_calc_mvave_no_ci(self, sample_xvg_file):
        """Test moving average without confidence interval."""
        xvg = XVG(sample_xvg_file)
        
        mvaves, highs, lows = xvg.calc_mvave(50, 0.95, 1, calc_CI=False)
        
        # highs and lows should still be NaN lists
        assert np.isnan(highs[0])
        assert np.isnan(lows[0])

    def test_xvg_calc_mvave_invalid_windowsize(self, sample_xvg_file):
        """Test error with invalid windowsize."""
        xvg = XVG(sample_xvg_file)
        
        # windowsize = 0
        with pytest.raises(SystemExit):
            xvg.calc_mvave(0, 0.95, 1)
        
        # windowsize too large
        with pytest.raises(SystemExit):
            xvg.calc_mvave(10000, 0.95, 1)

    def test_xvg_calc_mvave_invalid_confidence(self, sample_xvg_file):
        """Test error with invalid confidence."""
        xvg = XVG(sample_xvg_file)
        
        with pytest.raises(SystemExit):
            xvg.calc_mvave(50, 0.0, 1)
        
        with pytest.raises(SystemExit):
            xvg.calc_mvave(50, 1.0, 1)

    def test_xvg_calc_mvave_invalid_column(self, sample_xvg_file):
        """Test error with invalid column index."""
        xvg = XVG(sample_xvg_file)
        
        with pytest.raises(SystemExit):
            xvg.calc_mvave(50, 0.95, 100)


class TestXVGCalcAve:
    """Test cases for XVG.calc_ave method."""

    def test_xvg_calc_ave_basic(self, sample_xvg_file):
        """Test basic average calculation."""
        xvg = XVG(sample_xvg_file)
        
        legend, ave, std, ste = xvg.calc_ave(None, None, 1, 1)
        
        assert legend is not None
        assert isinstance(ave, float)
        assert isinstance(std, float)
        assert isinstance(ste, float)
        assert std >= 0
        assert ste >= 0

    def test_xvg_calc_ave_with_range(self, sample_xvg_file):
        """Test average calculation with begin/end range."""
        xvg = XVG(sample_xvg_file)
        
        legend1, ave1, std1, ste1 = xvg.calc_ave(None, None, 1, 1)
        legend2, ave2, std2, ste2 = xvg.calc_ave(1000, 2000, 1, 1)
        
        # Different ranges should give different results
        assert ave1 != ave2

    def test_xvg_calc_ave_with_step(self, sample_xvg_file):
        """Test average calculation with step."""
        xvg = XVG(sample_xvg_file)
        
        legend, ave, std, ste = xvg.calc_ave(None, None, 10, 1)
        
        # Should work without error
        assert isinstance(ave, float)

    def test_xvg_calc_ave_invalid_range(self, sample_xvg_file):
        """Test error with invalid range (begin >= end)."""
        xvg = XVG(sample_xvg_file)
        
        with pytest.raises(SystemExit):
            xvg.calc_ave(2000, 1000, 1, 1)

    def test_xvg_calc_ave_out_of_range(self, sample_xvg_file):
        """Test error with index out of range."""
        xvg = XVG(sample_xvg_file)
        
        with pytest.raises(SystemExit):
            xvg.calc_ave(5000, 6000, 1, 1)

    def test_xvg_calc_ave_invalid_column(self, sample_xvg_file):
        """Test error with invalid column index."""
        xvg = XVG(sample_xvg_file)
        
        with pytest.raises(SystemExit):
            xvg.calc_ave(None, None, 1, 100)


class TestXVGCheckColumnIndex:
    """Test cases for XVG.check_column_index method."""

    def test_xvg_check_column_index_valid(self, sample_xvg_file):
        """Test valid column index check."""
        xvg = XVG(sample_xvg_file)
        
        # Should not raise error
        xvg.check_column_index(0)
        xvg.check_column_index(4)
        xvg.check_column_index([0, 1, 2])

    def test_xvg_check_column_index_invalid(self, sample_xvg_file):
        """Test invalid column index check."""
        xvg = XVG(sample_xvg_file)
        
        with pytest.raises(SystemExit):
            xvg.check_column_index(5)
        
        with pytest.raises(SystemExit):
            xvg.check_column_index(100)

    def test_xvg_check_column_index_list_invalid(self, sample_xvg_file):
        """Test list with invalid column index."""
        xvg = XVG(sample_xvg_file)
        
        with pytest.raises(SystemExit):
            xvg.check_column_index([0, 1, 5])


class TestXVGWorldMinMax:
    """Test cases for XVG world min/max parsing."""

    def test_xvg_world_minmax(self, xvg_test_path):
        """Test parsing of world xmin/xmax/ymin/ymax values."""
        # Create a test xvg file with world min/max
        xvg_content = """@    title "Test"
@    xaxis label "X"
@    yaxis label "Y"
@    world xmin 0.0
@    world xmax 100.0
@    world ymin 0.0
@    world ymax 10.0
0.0 1.0
1.0 2.0
"""
        xvg = XVG(xvg_content.strip().split('\n'), is_file=False)
        
        assert xvg.xmin == 0.0
        assert xvg.xmax == 100.0
        assert xvg.ymin == 0.0
        assert xvg.ymax == 10.0


class TestXVGComments:
    """Test cases for XVG comments handling."""

    def test_xvg_comments_parsing(self):
        """Test parsing of comments."""
        lines = [
            '# This is a comment\n',
            '# Another comment\n',
            '@    title "Test"\n',
            '@    xaxis label "X"\n',
            '@    yaxis label "Y"\n',
            '1.0 2.0\n',
        ]
        xvg = XVG(lines, is_file=False)
        
        assert '# This is a comment' in xvg.comments
        assert '# Another comment' in xvg.comments

    def test_xvg_comments_tail(self):
        """Test comments_tail attribute."""
        xvg = XVG("output.xvg", is_file=False, new_file=True)
        xvg.comments_tail = "# Tail comment\n"
        
        assert "# Tail comment" in xvg.comments_tail


class TestXVGS:
    """Test cases for XVGS class (multi-frame xvg)."""

    def test_xvgs_init(self, xvg_test_path):
        """Test XVGS initialization with multi-frame xvg."""
        # Check if multi-frame xvg exists, skip if not
        # For now, test with regular xvg (single frame)
        gyrate_file = os.path.join(xvg_test_path, "gyrate.xvg")
        
        # Regular xvg should still work with XVGS
        xvgs = XVGS(gyrate_file)
        
        assert len(xvgs) >= 1
        assert isinstance(xvgs[0], XVG)

    def test_xvgs_len(self, xvg_test_path):
        """Test XVGS __len__ method."""
        gyrate_file = os.path.join(xvg_test_path, "gyrate.xvg")
        xvgs = XVGS(gyrate_file)
        
        assert isinstance(len(xvgs), int)
        assert len(xvgs) >= 1

    def test_xvgs_getitem(self, xvg_test_path):
        """Test XVGS __getitem__ method."""
        gyrate_file = os.path.join(xvg_test_path, "gyrate.xvg")
        xvgs = XVGS(gyrate_file)
        
        frame = xvgs[0]
        assert isinstance(frame, XVG)


class TestXVGEdgeCases:
    """Test edge cases for XVG parsing."""

    def test_xvg_single_column(self):
        """Test XVG with single column (should fail or warn)."""
        lines = [
            '@    title "Single Column"\n',
            '@    xaxis label "X"\n',
            '1.0\n',
            '2.0\n',
        ]
        xvg = XVG(lines, is_file=False)
        
        assert xvg.column_num == 1
        assert xvg.row_num == 2

    def test_xvg_empty_legend(self):
        """Test XVG with no legends."""
        lines = [
            '@    title "No Legend"\n',
            '@    xaxis label "X"\n',
            '@    yaxis label "Y"\n',
            '1.0 2.0\n',
            '3.0 4.0\n',
        ]
        xvg = XVG(lines, is_file=False)
        
        assert len(xvg.legends) == 0
        assert xvg.column_num == 2

    def test_xvg_yaxis_comma_separated(self):
        """Test XVG with comma-separated ylabel."""
        lines = [
            '@    title "Test"\n',
            '@    xaxis label "Time"\n',
            '@    yaxis label "(nm), (nm), (nm)"\n',
            '@ s0 legend "R1"\n',
            '@ s1 legend "R2"\n',
            '@ s2 legend "R3"\n',
            '1.0 2.0 3.0 4.0\n',
        ]
        xvg = XVG(lines, is_file=False)
        
        assert xvg.ylabel == "(nm), (nm), (nm)"

    def test_xvg_no_legend_multi_column_all_float(self):
        """BUG-09: Multi-column XVG with no legends must have all data columns as float, not string."""
        lines = [
            '@    title "No Legend Multi-Col"\n',
            '@    xaxis label "X"\n',
            '@    yaxis label "Y"\n',
            '1.0 2.0 3.0 4.0\n',
            '5.0 6.0 7.0 8.0\n',
        ]
        xvg = XVG(lines, is_file=False)

        assert xvg.column_num == 4
        # ALL data columns must be float
        for c in range(xvg.column_num):
            assert isinstance(xvg.data_columns[c][0], float), (
                f"data_columns[{c}][0] is {type(xvg.data_columns[c][0]).__name__}, expected float"
            )
        # arithmetic must work without TypeError
        result = xvg.data_columns[3][0] + xvg.data_columns[3][1]
        assert result == 12.0
