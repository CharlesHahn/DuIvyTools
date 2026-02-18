"""
Test cases for groParser.py module.

Tests for:
- GRO class: initialization, atom parsing, frame handling
- Atom class: atom line parsing
"""

import os
import sys
import pytest

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from FileParser.groParser import GRO, Atom


class TestAtom:
    """Test cases for Atom class."""

    def test_atom_parse_basic(self):
        """Test basic atom line parsing."""
        # GRO format: res_id(5), res_name(5), atom_name(5), atom_id(5), x(8), y(8), z(8)
        line = "   17LEU      N    1   4.734   1.121   2.157 -0.0732 -0.5912 -0.4172"
        atom = Atom(line)
        
        assert atom.res_id == 17
        assert atom.res_name == "LEU"
        assert atom.atom_name == "N"
        assert atom.atom_id == 1
        assert atom.coor_x == 4.734
        assert atom.coor_y == 1.121
        assert atom.coor_z == 2.157

    def test_atom_coordinates(self):
        """Test atom coordinate tuple."""
        line = "   17LEU      N    1   4.734   1.121   2.157 -0.0732 -0.5912 -0.4172"
        atom = Atom(line)
        
        assert atom.coor == (4.734, 1.121, 2.157)

    def test_atom_velocity(self):
        """Test atom velocity parsing."""
        line = "   17LEU      N    1   4.734   1.121   2.157 -0.0732 -0.5912 -0.4172"
        atom = Atom(line)
        
        assert atom.velocity_x == -0.0732
        assert atom.velocity_y == -0.5912
        assert atom.velocity_z == -0.4172
        assert atom.velocity == (-0.0732, -0.5912, -0.4172)

    def test_atom_no_velocity(self):
        """Test atom without velocity."""
        line = "   17LEU      N    1   4.734   1.121   2.157"
        atom = Atom(line)
        
        assert atom.velocity_x is None
        assert atom.velocity_y is None
        assert atom.velocity_z is None

    def test_atom_str(self):
        """Test Atom __str__ method."""
        line = "   17LEU      N    1   4.734   1.121   2.157 -0.0732 -0.5912 -0.4172"
        atom = Atom(line)
        
        output = str(atom)
        
        assert "17" in output
        assert "LEU" in output
        assert "N" in output


class TestGROInit:
    """Test cases for GRO class initialization."""

    def test_gro_init_basic(self, sample_gro_file):
        """Test basic GRO file parsing."""
        gro = GRO(sample_gro_file)
        
        assert gro.grofile == sample_gro_file
        assert gro.atom_number > 0
        assert gro.frame_num >= 1

    def test_gro_atom_number(self, sample_gro_file):
        """Test atom number parsing."""
        gro = GRO(sample_gro_file)
        
        assert gro.atom_number == 50435

    def test_gro_frame_number(self, sample_gro_file):
        """Test frame number parsing."""
        gro = GRO(sample_gro_file)
        
        # Single frame GRO file
        assert gro.frame_num == 1

    def test_gro_frames_list(self, sample_gro_file):
        """Test frames list initialization."""
        gro = GRO(sample_gro_file)
        
        assert len(gro.frames) == gro.frame_num
        assert len(gro.frames[0]) == gro.atom_number

    def test_gro_notes(self, sample_gro_file):
        """Test notes parsing."""
        gro = GRO(sample_gro_file)
        
        assert len(gro.notes) == gro.frame_num
        assert "Protein" in gro.notes[0]

    def test_gro_box_coordinates(self, sample_gro_file):
        """Test box coordinates parsing."""
        gro = GRO(sample_gro_file)
        
        assert len(gro.box_coors) == gro.frame_num
        # Box coordinates should be a tuple of floats
        assert isinstance(gro.box_coors[0], tuple)

    def test_gro_file_not_exists(self):
        """Test error when file does not exist."""
        with pytest.raises(SystemExit):
            GRO("nonexistent_file.gro")

    def test_gro_wrong_suffix(self, tmp_path):
        """Test error when file has wrong suffix."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("title\n2\nline1\nline2\nbox\n")
        
        with pytest.raises(SystemExit):
            GRO(str(wrong_file))


class TestGROAtoms:
    """Test cases for GRO atom access."""

    def test_gro_first_atom(self, sample_gro_file):
        """Test first atom in first frame."""
        gro = GRO(sample_gro_file)
        
        atom = gro.frames[0][0]
        
        assert isinstance(atom, Atom)
        assert atom.res_id == 17
        assert atom.res_name == "LEU"
        assert atom.atom_name == "N"
        assert atom.atom_id == 1

    def test_gro_atom_coordinates(self, sample_gro_file):
        """Test atom coordinates in GRO."""
        gro = GRO(sample_gro_file)
        
        atom = gro.frames[0][0]
        
        # Check coordinates match expected values
        assert abs(atom.coor_x - 4.734) < 0.001
        assert abs(atom.coor_y - 1.121) < 0.001
        assert abs(atom.coor_z - 2.157) < 0.001

    def test_gro_last_atom(self, sample_gro_file):
        """Test last atom in first frame."""
        gro = GRO(sample_gro_file)
        
        atom = gro.frames[0][-1]
        
        assert isinstance(atom, Atom)
        assert atom.atom_id == gro.atom_number


class TestGRONewFile:
    """Test cases for GRO class with new_file=True."""

    def test_gro_new_file_init(self):
        """Test GRO initialization with new_file=True."""
        gro = GRO("output.gro", new_file=True)
        
        assert gro.grofile == "output.gro"
        assert gro.frame_num == 0
        assert gro.atom_number == 0
        assert len(gro.frames) == 0


class TestGROEdgeCases:
    """Test edge cases for GRO parsing."""

    def test_gro_multiple_frames(self, tmp_path):
        """Test GRO file with multiple frames."""
        # Create a GRO file with 2 frames, each with 2 atoms
        content = """Frame 1
2
   17LEU      N    1   4.734   1.121   2.157
   18VAL      N    2   4.412   1.192   2.253
   5.0   5.0   5.0
Frame 2
2
   17LEU      N    1   4.800   1.200   2.200
   18VAL      N    2   4.500   1.300   2.300
   5.0   5.0   5.0
"""
        gro_file = tmp_path / "multi.gro"
        gro_file.write_text(content)
        
        gro = GRO(str(gro_file))
        
        assert gro.frame_num == 2
        assert len(gro.frames) == 2
        assert gro.atom_number == 2

    def test_gro_atom_types(self, sample_gro_file):
        """Test that atom properties have correct types."""
        gro = GRO(sample_gro_file)
        
        atom = gro.frames[0][0]
        
        assert isinstance(atom.res_id, int)
        assert isinstance(atom.res_name, str)
        assert isinstance(atom.atom_name, str)
        assert isinstance(atom.atom_id, int)
        assert isinstance(atom.coor_x, float)
        assert isinstance(atom.coor_y, float)
        assert isinstance(atom.coor_z, float)
