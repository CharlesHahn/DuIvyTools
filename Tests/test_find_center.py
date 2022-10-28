
## author : charlie
## date : 20220823

import os
import sys
import pytest
import filecmp
from io import StringIO

sys.path.append("../DuIvyTools/")
from FindCenter import find_center


def test_find_center_nondx(capfd):
    gro_file = "find_center_test/test.gro"
    ndx_file = "find_center_test/index.ndx"
    
    # center of system 
    find_center(gro_file)
    out, err = capfd.readouterr()
    assert (
        out == """--------------------------------------------
ResID Name Atom  Num       X       Y       Z
--------------------------------------------
14509SOL    HW144693   4.042   4.159   4.131
--------------------------------------------
""")

def test_find_center_ndx(capfd, monkeypatch):
    gro_file = "find_center_test/test.gro"
    ndx_file = "find_center_test/index.ndx"
    # center of one group
    inputs = StringIO('2\n')
    monkeypatch.setattr('sys.stdin', inputs)
    find_center(gro_file, ndx_file)
    out, err = capfd.readouterr()
    assert (
        out == """  0 => System (50435)
  1 => Protein (1125)
  2 => Protein-H (905)
  3 => C-alpha (130)
  4 => Backbone (390)
  5 => MainChain (525)
  6 => MainChain+Cb (630)
  7 => MainChain+H (665)
  8 => SideChain (460)
  9 => SideChain-H (380)
 10 => Prot-Masses (1125)
 11 => non-Protein (49310)
 12 => Other (186)
 13 => 1ZIN (31)
 14 => 2ZIN (31)
 15 => 3ZIN (31)
 16 => 4ZIN (31)
 17 => 5ZIN (31)
 18 => 6ZIN (31)
 19 => Water (49119)
 20 => SOL (49119)
 21 => non-Water (1316)
 22 => Ion (5)
 23 => NA (5)
 24 => Water_and_ions (49124)
 25 => Protein_Ligands (1311)
Select one group: --------------------------------------------
ResID Name Atom  Num       X       Y       Z
--------------------------------------------
   30ALA     CB  132   3.953   3.439   3.413
--------------------------------------------
"""
)

def test_find_center_ndx_aa(capfd, monkeypatch):
    gro_file = "find_center_test/test.gro"
    ndx_file = "find_center_test/index.ndx"
    # center of one group
    inputs = StringIO('22\n')
    monkeypatch.setattr('sys.stdin', inputs)
    find_center(gro_file, ndx_file, True)
    out, err = capfd.readouterr()
    assert (
        out == """  0 => System (50435)
  1 => Protein (1125)
  2 => Protein-H (905)
  3 => C-alpha (130)
  4 => Backbone (390)
  5 => MainChain (525)
  6 => MainChain+Cb (630)
  7 => MainChain+H (665)
  8 => SideChain (460)
  9 => SideChain-H (380)
 10 => Prot-Masses (1125)
 11 => non-Protein (49310)
 12 => Other (186)
 13 => 1ZIN (31)
 14 => 2ZIN (31)
 15 => 3ZIN (31)
 16 => 4ZIN (31)
 17 => 5ZIN (31)
 18 => 6ZIN (31)
 19 => Water (49119)
 20 => SOL (49119)
 21 => non-Water (1316)
 22 => Ion (5)
 23 => NA (5)
 24 => Water_and_ions (49124)
 25 => Protein_Ligands (1311)
Select one group: --------------------------------------------
ResID Name Atom  Num       X       Y       Z
--------------------------------------------
 6403SOL     OW20374   4.193   3.323   5.941
--------------------------------------------
"""
)
