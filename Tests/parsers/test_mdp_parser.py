"""
Test cases for mdpParser.py module.

Tests for:
- MDP class: initialization, parameter access, save operations
"""

import os
import sys
import pytest

# Ensure source path is in sys.path
SRC_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "DuIvyTools", "DuIvyTools"))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from FileParser.mdpParser import MDP


class TestMDPInit:
    """Test cases for MDP class initialization."""

    def test_mdp_init_basic(self, sample_mdp_file):
        """Test basic MDP file parsing."""
        mdp = MDP(sample_mdp_file)
        
        assert mdp.mdpfile == sample_mdp_file
        assert len(mdp) > 0

    def test_mdp_parameters_count(self, sample_mdp_file):
        """Test number of parameters parsed."""
        mdp = MDP(sample_mdp_file)
        
        # MDP file should have many parameters
        assert len(mdp) > 50

    def test_mdp_file_not_exists(self):
        """Test error when file does not exist."""
        with pytest.raises(SystemExit):
            MDP("nonexistent_file.mdp")

    def test_mdp_wrong_suffix(self, tmp_path):
        """Test error when file has wrong suffix."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("integrator = md\n")
        
        with pytest.raises(SystemExit):
            MDP(str(wrong_file))


class TestMDPGetItem:
    """Test cases for MDP __getitem__ method."""

    def test_mdp_getitem_integrator(self, sample_mdp_file):
        """Test getting integrator parameter."""
        mdp = MDP(sample_mdp_file)
        
        assert mdp["integrator"] == "md"

    def test_mdp_getitem_dt(self, sample_mdp_file):
        """Test getting dt parameter."""
        mdp = MDP(sample_mdp_file)
        
        assert mdp["dt"] == "0.002"

    def test_mdp_getitem_nsteps(self, sample_mdp_file):
        """Test getting nsteps parameter."""
        mdp = MDP(sample_mdp_file)
        
        assert mdp["nsteps"] == "50000"

    def test_mdp_getitem_nonexistent(self, sample_mdp_file):
        """Test getting nonexistent parameter."""
        mdp = MDP(sample_mdp_file)
        
        assert mdp["nonexistent_parameter"] is None

    def test_mdp_getitem_tcoupl(self, sample_mdp_file):
        """Test getting temperature coupling parameter."""
        mdp = MDP(sample_mdp_file)
        
        assert mdp["tcoupl"] == "V-rescale"

    def test_mdp_getitem_pcoupl(self, sample_mdp_file):
        """Test getting pressure coupling parameter."""
        mdp = MDP(sample_mdp_file)
        
        assert mdp["pcoupl"] == "Berendsen"


class TestMDPSetItem:
    """Test cases for MDP __setitem__ method."""

    def test_mdp_setitem_new(self, sample_mdp_file):
        """Test setting new parameter."""
        mdp = MDP(sample_mdp_file)
        initial_len = len(mdp)
        
        mdp["new_param"] = "new_value"
        
        assert len(mdp) == initial_len + 1
        assert mdp["new_param"] == "new_value"

    def test_mdp_setitem_update(self, sample_mdp_file):
        """Test updating existing parameter."""
        mdp = MDP(sample_mdp_file)
        
        mdp["integrator"] = "sd"
        
        assert mdp["integrator"] == "sd"

    def test_mdp_setitem_invalid_key_type(self, sample_mdp_file):
        """Test error when setting with invalid key type."""
        mdp = MDP(sample_mdp_file)
        
        with pytest.raises(SystemExit):
            mdp[123] = "value"

    def test_mdp_setitem_invalid_value_type(self, sample_mdp_file):
        """Test error when setting with invalid value type."""
        mdp = MDP(sample_mdp_file)
        
        with pytest.raises(SystemExit):
            mdp["key"] = 123


class TestMDPDelItem:
    """Test cases for MDP __delitem__ method."""

    def test_mdp_delitem(self, sample_mdp_file):
        """Test deleting parameter."""
        mdp = MDP(sample_mdp_file)
        initial_len = len(mdp)
        
        del mdp["integrator"]
        
        assert len(mdp) == initial_len - 1
        assert mdp["integrator"] is None

    def test_mdp_delitem_nonexistent(self, sample_mdp_file):
        """Test deleting nonexistent parameter (should not raise error)."""
        mdp = MDP(sample_mdp_file)
        
        # Should not raise error
        del mdp["nonexistent_parameter"]


class TestMDPMethods:
    """Test cases for MDP methods."""

    def test_mdp_len(self, sample_mdp_file):
        """Test __len__ method."""
        mdp = MDP(sample_mdp_file)
        
        assert isinstance(len(mdp), int)
        assert len(mdp) > 0

    def test_mdp_str(self, sample_mdp_file):
        """Test __str__ method."""
        mdp = MDP(sample_mdp_file)
        
        output = str(mdp)
        
        assert "integrator" in output
        assert "md" in output

    def test_mdp_save(self, sample_mdp_file, tmp_path):
        """Test saving MDP to file."""
        mdp = MDP(sample_mdp_file)
        
        output_file = tmp_path / "output.mdp"
        mdp.save(str(output_file))
        
        assert output_file.exists()
        
        # Load saved file and verify
        mdp2 = MDP(str(output_file))
        assert mdp2["integrator"] == "md"


class TestMDPNewFile:
    """Test cases for MDP class with new_file=True."""

    def test_mdp_new_file_init(self):
        """Test MDP initialization with new_file=True."""
        mdp = MDP("output.mdp", new_file=True)
        
        assert mdp.mdpfile == "output.mdp"
        assert len(mdp) == 0

    def test_mdp_new_file_set_params(self):
        """Test setting parameters on new MDP instance."""
        mdp = MDP("output.mdp", new_file=True)
        
        mdp["integrator"] = "md"
        mdp["dt"] = "0.002"
        mdp["nsteps"] = "100000"
        
        assert len(mdp) == 3
        assert mdp["integrator"] == "md"


class TestMDPInitFromContent:
    """Test cases for MDP initialization from content string."""

    def test_mdp_init_from_string(self):
        """Test MDP initialization from content string."""
        content = """
integrator = md
dt = 0.002
nsteps = 10000
tcoupl = V-rescale
"""
        mdp = MDP(content, is_file=False)
        
        assert len(mdp) == 4
        assert mdp["integrator"] == "md"
        assert mdp["dt"] == "0.002"

    def test_mdp_init_from_string_with_comments(self):
        """Test MDP initialization from content with comments."""
        content = """
; This is a comment
integrator = md  ; inline comment
dt = 0.002
"""
        mdp = MDP(content, is_file=False)
        
        assert mdp["integrator"] == "md"
        assert mdp["dt"] == "0.002"


class TestMDPUnderscoreToDash:
    """Test underscore to dash conversion in keys."""

    def test_mdp_underscore_conversion(self):
        """Test that underscores in keys are converted to dashes."""
        content = """
nsteps = 10000
nst_list = 10
"""
        mdp = MDP(content, is_file=False)
        
        # nst_list should be stored as nst-list
        assert mdp["nst-list"] == "10"


class TestMDPEdgeCases:
    """Test edge cases for MDP parsing."""

    def test_mdp_empty_value(self):
        """Test parameter with empty value."""
        content = "include = \n"
        mdp = MDP(content, is_file=False)
        
        assert mdp["include"] == ""

    def test_mdp_key_without_equals(self):
        """Test parameter without equals sign."""
        content = "somekey\n"
        mdp = MDP(content, is_file=False)
        
        assert mdp["somekey"] == ""

    def test_mdp_multiple_equals(self, tmp_path):
        """Test error when line has multiple equals signs."""
        # MDP parser has a bug when is_file=False, use actual file
        content = "key = value = extra\n"
        mdp_file = tmp_path / "test.mdp"
        mdp_file.write_text(content)
        
        with pytest.raises(SystemExit):
            MDP(str(mdp_file))
