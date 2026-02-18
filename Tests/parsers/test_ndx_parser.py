"""
Test cases for ndxParser.py module.

Tests for:
- NDX class: initialization, group access, save, add, delete operations
"""

import os
import sys
import pytest
import tempfile

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from FileParser.ndxParser import NDX


class TestNDXInit:
    """Test cases for NDX class initialization."""

    def test_ndx_init_basic(self, sample_ndx_file):
        """Test basic NDX file parsing."""
        ndx = NDX(sample_ndx_file)
        
        assert ndx.ndxfile == sample_ndx_file
        assert len(ndx) > 0

    def test_ndx_groups_count(self, sample_ndx_file):
        """Test number of groups parsed."""
        ndx = NDX(sample_ndx_file)
        
        # hbond.ndx has 4 groups
        assert len(ndx) == 4

    def test_ndx_group_names(self, sample_ndx_file):
        """Test group names extraction."""
        ndx = NDX(sample_ndx_file)
        
        assert "Protein" in ndx.names
        assert "1ZIN" in ndx.names

    def test_ndx_first_group_indexs(self, sample_ndx_file):
        """Test first group indexs (Protein)."""
        ndx = NDX(sample_ndx_file)
        
        # Protein group should have 1125 atoms (1 to 1125)
        name, indexs = ndx["Protein"]
        assert name == "Protein"
        assert len(indexs) == 1125
        assert indexs[0] == 1
        assert indexs[-1] == 1125

    def test_ndx_second_group_indexs(self, sample_ndx_file):
        """Test second group indexs (1ZIN)."""
        ndx = NDX(sample_ndx_file)
        
        # 1ZIN group should have 31 atoms
        name, indexs = ndx["1ZIN"]
        assert name == "1ZIN"
        assert len(indexs) == 31

    def test_ndx_file_not_exists(self):
        """Test error when file does not exist."""
        with pytest.raises(SystemExit):
            NDX("nonexistent_file.ndx")

    def test_ndx_wrong_suffix(self, tmp_path):
        """Test error when file has wrong suffix."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("[ Test ]\n1 2 3\n")
        
        with pytest.raises(SystemExit):
            NDX(str(wrong_file))


class TestNDXNewFile:
    """Test cases for NDX class with new_file=True."""

    def test_ndx_new_file_init(self):
        """Test NDX initialization with new_file=True."""
        ndx = NDX("output.ndx", new_file=True)
        
        assert ndx.ndxfile == "output.ndx"
        assert len(ndx) == 0
        assert len(ndx.names) == 0

    def test_ndx_new_file_add_groups(self):
        """Test adding groups to new NDX."""
        ndx = NDX("output.ndx", new_file=True)
        
        ndx.add("Protein", list(range(1, 101)))
        ndx.add("Ligand", list(range(101, 151)))
        
        assert len(ndx) == 2
        assert "Protein" in ndx.names
        assert "Ligand" in ndx.names


class TestNDXGetItem:
    """Test cases for NDX __getitem__ method."""

    def test_ndx_getitem_by_int(self, sample_ndx_file):
        """Test getting group by integer index."""
        ndx = NDX(sample_ndx_file)
        
        name, indexs = ndx[0]
        assert name == "Protein"
        assert len(indexs) == 1125

    def test_ndx_getitem_by_name(self, sample_ndx_file):
        """Test getting group by name."""
        ndx = NDX(sample_ndx_file)
        
        name, indexs = ndx["Protein"]
        assert name == "Protein"
        assert len(indexs) == 1125

    def test_ndx_getitem_invalid_int(self, sample_ndx_file):
        """Test getting group by invalid integer index."""
        ndx = NDX(sample_ndx_file)
        
        name, indexs = ndx[100]  # Out of range
        assert name is None
        assert indexs is None

    def test_ndx_getitem_invalid_name(self, sample_ndx_file):
        """Test getting group by invalid name."""
        ndx = NDX(sample_ndx_file)
        
        name, indexs = ndx["NonExistent"]
        assert name is None
        assert indexs is None


class TestNDXSetItem:
    """Test cases for NDX __setitem__ method."""

    def test_ndx_setitem_by_name_new(self):
        """Test setting new group by name."""
        ndx = NDX("output.ndx", new_file=True)
        
        ndx["NewGroup"] = [1, 2, 3, 4, 5]
        
        assert len(ndx) == 1
        assert "NewGroup" in ndx.names
        assert ndx["NewGroup"][1] == [1, 2, 3, 4, 5]

    def test_ndx_setitem_by_name_existing(self):
        """Test setting existing group by name (updates indexs)."""
        ndx = NDX("output.ndx", new_file=True)
        
        ndx["TestGroup"] = [1, 2, 3]
        ndx["TestGroup"] = [4, 5, 6, 7]  # Update existing group
        
        # Should still have only 1 group
        assert len(ndx) == 1
        # Indexs should be updated
        assert ndx["TestGroup"][1] == [4, 5, 6, 7]

    def test_ndx_setitem_by_int(self):
        """Test setting group by integer index."""
        ndx = NDX("output.ndx", new_file=True)
        ndx.add("Group1", [1, 2, 3])
        ndx.add("Group2", [4, 5, 6])
        
        # Update first group by index
        ndx[0] = [10, 20, 30]
        
        assert ndx[0][1] == [10, 20, 30]
        # Name should not change
        assert ndx[0][0] == "Group1"

    def test_ndx_setitem_by_int_out_of_range(self):
        """Test error when setting by invalid integer index."""
        ndx = NDX("output.ndx", new_file=True)
        ndx.add("Group1", [1, 2, 3])
        
        with pytest.raises(SystemExit):
            ndx[10] = [1, 2, 3]


class TestNDXDelItem:
    """Test cases for NDX __delitem__ method."""

    def test_ndx_delitem_by_int(self, sample_ndx_file):
        """Test deleting group by integer index."""
        ndx = NDX(sample_ndx_file)
        initial_len = len(ndx)
        
        del ndx[0]
        
        assert len(ndx) == initial_len - 1
        assert "Protein" not in ndx.names

    def test_ndx_delitem_by_name(self, sample_ndx_file):
        """Test deleting group by name."""
        ndx = NDX(sample_ndx_file)
        initial_len = len(ndx)
        
        del ndx["Protein"]
        
        assert len(ndx) == initial_len - 1

    def test_ndx_delitem_invalid_int(self, sample_ndx_file):
        """Test error when deleting by invalid integer index."""
        ndx = NDX(sample_ndx_file)
        
        with pytest.raises(SystemExit):
            del ndx[100]


class TestNDXMethods:
    """Test cases for NDX methods."""

    def test_ndx_add(self, sample_ndx_file):
        """Test adding a new group."""
        ndx = NDX(sample_ndx_file)
        initial_len = len(ndx)
        
        ndx.add("NewGroup", [1, 2, 3, 4, 5])
        
        assert len(ndx) == initial_len + 1
        assert "NewGroup" in ndx.names

    def test_ndx_show_names(self, sample_ndx_file):
        """Test show_names property."""
        ndx = NDX(sample_ndx_file)
        
        output = ndx.show_names
        
        assert "Protein" in output
        assert "1ZIN" in output

    def test_ndx_get_id_by_name(self, sample_ndx_file):
        """Test get_id_by_name method."""
        ndx = NDX(sample_ndx_file)
        
        ids = ndx.get_id_by_name("Protein")
        assert len(ids) == 1
        assert ids[0] == 0

    def test_ndx_str(self, sample_ndx_file):
        """Test __str__ method."""
        ndx = NDX(sample_ndx_file)
        
        output = str(ndx)
        
        assert "[ Protein ]" in output


class TestNDXSave:
    """Test cases for NDX save method."""

    def test_ndx_save(self, sample_ndx_file, tmp_path):
        """Test saving NDX to file."""
        ndx = NDX(sample_ndx_file)
        
        output_file = tmp_path / "output.ndx"
        ndx.save(str(output_file))
        
        assert output_file.exists()
        
        # Load saved file and verify
        ndx2 = NDX(str(output_file))
        assert len(ndx2) == len(ndx)

    def test_ndx_save_new_file(self, tmp_path):
        """Test saving new NDX instance."""
        ndx = NDX("output.ndx", new_file=True)
        ndx.add("Protein", list(range(1, 101)))
        ndx.add("Ligand", list(range(101, 151)))
        
        output_file = tmp_path / "new_output.ndx"
        ndx.save(str(output_file))
        
        assert output_file.exists()
        
        # Load and verify
        ndx2 = NDX(str(output_file))
        assert len(ndx2) == 2


class TestNDXFormatter:
    """Test cases for NDX formatter method."""

    def test_ndx_formatter_basic(self, sample_ndx_file):
        """Test formatter method output."""
        ndx = NDX(sample_ndx_file)
        
        output = ndx.formatter(0)
        
        assert "[ Protein ]" in output

    def test_ndx_formatter_column_num(self):
        """Test formatter with custom column number."""
        ndx = NDX("output.ndx", new_file=True)
        ndx.add("Test", list(range(1, 31)), column_num=10)
        
        output = ndx.formatter(0)
        
        lines = output.strip().split("\n")
        # First line is group name, rest should be data
        assert len(lines) >= 1
