"""
Test cases for pdbParser.py module.

Tests for:
- PDB class: initialization, model parsing, atom access
- Atom class: atom line parsing
"""

import os
import sys
import pytest

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from FileParser.pdbParser import PDB, Atom


class TestAtom:
    """Test cases for Atom class."""

    def test_atom_parse_basic(self):
        """Test basic atom line parsing."""
        # PDB ATOM format
        line = "ATOM      1  C1  9G6     0      -0.477  -1.546   0.252  1.00  0.00           C  "
        atom = Atom(line)
        
        assert atom.atom_id == 1
        assert atom.atom_name == "C1"
        assert atom.res_name == "9G6"
        assert atom.res_id == 0
        assert atom.coor_x == -0.477
        assert atom.coor_y == -1.546
        assert atom.coor_z == 0.252

    def test_atom_coordinates(self):
        """Test atom coordinate tuple."""
        line = "ATOM      1  C1  9G6     0      -0.477  -1.546   0.252  1.00  0.00           C  "
        atom = Atom(line)
        
        assert atom.coor == (-0.477, -1.546, 0.252)

    def test_atom_occupancy(self):
        """Test atom occupancy parsing."""
        line = "ATOM      1  C1  9G6     0      -0.477  -1.546   0.252  1.00  0.00           C  "
        atom = Atom(line)
        
        assert atom.occupancy == 1.00

    def test_atom_tempfactor(self):
        """Test atom temperature factor parsing."""
        line = "ATOM      1  C1  9G6     0      -0.477  -1.546   0.252  1.00  0.00           C  "
        atom = Atom(line)
        
        assert atom.tempfactor == 0.00

    def test_atom_symbol(self):
        """Test atom symbol parsing."""
        line = "ATOM      1  C1  9G6     0      -0.477  -1.546   0.252  1.00  0.00           C  "
        atom = Atom(line)
        
        assert atom.symbol == "C"

    def test_atom_charge(self):
        """Test atom charge parsing (usually empty)."""
        line = "ATOM      1  C1  9G6     0      -0.477  -1.546   0.252  1.00  0.00           C  "
        atom = Atom(line)
        
        # Charge is usually empty
        assert atom.charge is None

    def test_atom_chain_id(self):
        """Test atom chain ID parsing."""
        line = "ATOM      1  C1  9G6 A   0      -0.477  -1.546   0.252  1.00  0.00           C  "
        atom = Atom(line)
        
        # Chain ID at position 21
        assert atom.chain_id == "A"


class TestPDBInit:
    """Test cases for PDB class initialization."""

    def test_pdb_init_basic(self, sample_pdb_file):
        """Test basic PDB file parsing."""
        pdb = PDB(sample_pdb_file)
        
        assert pdb.atom_number > 0
        assert pdb.model_num >= 1

    def test_pdb_atom_number(self, sample_pdb_file):
        """Test atom number parsing."""
        pdb = PDB(sample_pdb_file)
        
        assert pdb.atom_number > 0

    def test_pdb_model_number(self, sample_pdb_file):
        """Test model number parsing."""
        pdb = PDB(sample_pdb_file)
        
        # Single model PDB file
        assert pdb.model_num == 1

    def test_pdb_models_list(self, sample_pdb_file):
        """Test models list initialization."""
        pdb = PDB(sample_pdb_file)
        
        assert len(pdb.models) == pdb.model_num
        assert len(pdb.models[0]) == pdb.atom_number

    def test_pdb_file_not_exists(self):
        """Test error when file does not exist."""
        with pytest.raises(SystemExit):
            PDB("nonexistent_file.pdb")


class TestPDBAtoms:
    """Test cases for PDB atom access."""

    def test_pdb_first_atom(self, sample_pdb_file):
        """Test first atom in first model."""
        pdb = PDB(sample_pdb_file)
        
        atom = pdb.models[0][0]
        
        assert isinstance(atom, Atom)
        assert atom.atom_id == 1
        assert atom.atom_name == "C1"
        assert atom.res_name == "9G6"

    def test_pdb_atom_coordinates(self, sample_pdb_file):
        """Test atom coordinates in PDB."""
        pdb = PDB(sample_pdb_file)
        
        atom = pdb.models[0][0]
        
        # Check coordinates match expected values
        assert abs(atom.coor_x - (-0.477)) < 0.001
        assert abs(atom.coor_y - (-1.546)) < 0.001
        assert abs(atom.coor_z - 0.252) < 0.001

    def test_pdb_last_atom(self, sample_pdb_file):
        """Test last atom in first model."""
        pdb = PDB(sample_pdb_file)
        
        atom = pdb.models[0][-1]
        
        assert isinstance(atom, Atom)
        assert atom.atom_id == pdb.atom_number

    def test_pdb_atom_types(self, sample_pdb_file):
        """Test that atom properties have correct types."""
        pdb = PDB(sample_pdb_file)
        
        atom = pdb.models[0][0]
        
        assert isinstance(atom.atom_id, int)
        assert isinstance(atom.atom_name, str)
        assert isinstance(atom.res_name, str)
        assert isinstance(atom.res_id, int)
        assert isinstance(atom.coor_x, float)
        assert isinstance(atom.coor_y, float)
        assert isinstance(atom.coor_z, float)


class TestPDBMultipleModels:
    """Test cases for PDB files with multiple models."""

    def test_pdb_multiple_models(self, tmp_path):
        """Test PDB file with multiple models."""
        content = """MODEL        1
ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00  0.00           C
ENDMDL
MODEL        2
ATOM      1  CA  ALA A   1       2.000   3.000   4.000  1.00  0.00           C
ENDMDL
"""
        pdb_file = tmp_path / "multi.pdb"
        pdb_file.write_text(content)
        
        pdb = PDB(str(pdb_file))
        
        assert pdb.model_num == 2
        assert len(pdb.models) == 2
        assert pdb.models[0][0].coor_x == 1.000
        assert pdb.models[1][0].coor_x == 2.000


class TestPDBHETATM:
    """Test cases for PDB HETATM records."""

    def test_pdb_hetatm(self, tmp_path):
        """Test PDB file with HETATM records."""
        content = """ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00  0.00           C
HETATM    2  O   HOH A   2       5.000   6.000   7.000  1.00  0.00           O
"""
        pdb_file = tmp_path / "hetatm.pdb"
        pdb_file.write_text(content)
        
        pdb = PDB(str(pdb_file))
        
        assert pdb.atom_number == 2
        assert len(pdb.models[0]) == 2


class TestPDBEdgeCases:
    """Test edge cases for PDB parsing."""

    def test_pdb_no_endmdl(self, tmp_path):
        """Test PDB file without ENDMDL."""
        content = """ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00  0.00           C
ATOM      2  CB  ALA A   1       2.000   3.000   4.000  1.00  0.00           C
"""
        pdb_file = tmp_path / "noendmdl.pdb"
        pdb_file.write_text(content)
        
        pdb = PDB(str(pdb_file))
        
        assert pdb.model_num == 1
        assert pdb.atom_number == 2

    def test_pdb_empty_occupancy_tempfactor(self):
        """Test atom with empty occupancy and tempfactor."""
        line = "ATOM      1  CA  ALA A   1       1.000   2.000   3.000                          C  "
        atom = Atom(line)
        
        assert atom.occupancy is None
        assert atom.tempfactor is None

    def test_pdb_empty_chain_id(self):
        """Test atom with empty chain ID."""
        line = "ATOM      1  CA  ALA     1       1.000   2.000   3.000  1.00  0.00           C  "
        atom = Atom(line)
        
        # Empty chain ID should be None
        assert atom.chain_id is None

    def test_pdb_atom_symbol_empty(self):
        """Test atom with empty symbol."""
        line = "ATOM      1  CA  ALA A   1       1.000   2.000   3.000  1.00  0.00              "
        atom = Atom(line)
        
        assert atom.symbol is None
