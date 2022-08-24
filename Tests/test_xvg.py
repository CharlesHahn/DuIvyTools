## author : charlie
## date : 20220824

import os
import sys
import pytest 
import filecmp
from matplotlib.testing.compare import compare_images
# https://matplotlib.org/3.1.1/api/testing_api.html

sys.path.append("../DuIvyTools/")
import XVG 


def test_xvg_init():
    xvg_file = "xvg_test/gyrate.xvg" 
    xvg = XVG.XVG(xvg_file)
    assert xvg.xvg_filename == "xvg_test/gyrate.xvg"
    assert xvg.xvg_title == "Radius of gyration (total and around axes)"
    assert xvg.xvg_xlabel == "Time (ps)"
    assert xvg.xvg_ylabel == "Rg (nm)"
    assert xvg.xvg_legends == ["Rg", "Rg\\sX\\N", "Rg\\sY\\N", "Rg\\sZ\\N"]
    assert xvg.xvg_column_num == 5
    assert xvg.xvg_row_num == 4001
    assert xvg.data_heads == ["Time (ps)", "Rg", "Rg\\sX\\N", "Rg\\sY\\N", "Rg\\sZ\\N"]
    assert xvg.data_columns[0] == [i*10 for i in range(4001)]
    assert xvg.data_columns[1][-1] == 3.77892
    assert xvg.data_columns[2][-1] == 3.01626
    assert xvg.data_columns[3][-1] == 3.04144
    assert xvg.data_columns[4][-1] == 3.19567
    assert xvg.data_columns[1][:2] == [3.73837, 3.73357]
    assert xvg.data_columns[2][:2] == [2.20746, 2.21266]
    assert xvg.data_columns[3][:2] == [3.13682, 3.12841]
    assert xvg.data_columns[4][:2] == [3.63844, 3.63267]


def test_xvg_combine():
    gyrate_file = "xvg_test/gyrate.xvg" 
    rmsd_file = "xvg_test/rmsd.xvg" 
    XVG.xvg_combine([gyrate_file, rmsd_file], [[0, 1], [1]], "xvg_test/gyrate_rmsd.xvg")
    assert filecmp.cmp("xvg_test/gyrate_rmsd.xvg", "xvg_test/xvg_combined.xvg")
    os.remove("xvg_test/gyrate_rmsd.xvg")


def test_energy_compute():
    prolig = "xvg_test/prolig_energy.xvg" 
    pro = "xvg_test/pro_energy.xvg" 
    lig = "xvg_test/lig_energy.xvg" 
    XVG.energy_compute([prolig, pro, lig], "xvg_test/energy.xvg") 
    assert filecmp.cmp("xvg_test/energy.xvg", "xvg_test/energy_compute.xvg")
    os.remove("xvg_test/energy.xvg")


def test_xvg_ramachandarn(capfd):
    output = """\n-------------------------------------------------------------------------------
               Normal Dihedrals    Outlier Dihedrals
General                    7778                  565
GLY                        1799                  226
Pre-PRO                       0                    0
PRO                           0                    0
-------------------------------------------------------------------------------\n"""
    file = "xvg_test/rama.xvg"
    XVG.xvg_ramachandran(file, "xvg_test/test.png", True)
    assert filecmp.cmp("xvg_test/rama_General.png", "xvg_test/test_General.png")
    assert filecmp.cmp("xvg_test/rama_Gly.png", "xvg_test/test_Gly.png")
    assert compare_images("xvg_test/rama_General.png", "xvg_test/test_General.png", 0.001) is None
    assert compare_images("xvg_test/rama_Gly.png", "xvg_test/test_Gly.png", 0.001) is None
    os.remove("xvg_test/test_General.png")
    os.remove("xvg_test/test_Gly.png")
    out, err = capfd.readouterr()
    assert out == output


def test_xvg_compare():
    pass

def test_xvg_bar_compare():
    pass

def test_xvg_box_compare():
    pass

def test_xvg_calc_ave():
    pass

def test_xvg_calc_mvave2csv():
    pass

def test_xvg2csv():
    pass

def test_xvg_show():
    pass

def test_xvg_show_distribution():
    pass

def test_xvg_show_stacking():
    pass

def test_xvg_show_scatter():
    pass
