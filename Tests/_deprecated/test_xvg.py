## author : charlie
## date : 20220824

import os
import sys
import pytest
import filecmp
from matplotlib.testing.compare import compare_images
from matplotlib import pyplot as plt

# https://matplotlib.org/3.1.1/api/testing_api.html

sys.path.append("../DuIvyTools/")
import XVG

data_file_path = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
mplstyle = os.path.join(data_file_path, os.path.join("..", "DuIvyTools","data", "DIT.mplstyle"))
plt.style.use(mplstyle)

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
    assert xvg.data_columns[0] == [i * 10 for i in range(4001)]
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
    assert (
        compare_images("xvg_test/rama_General.png", "xvg_test/test_General.png", 0.001)
        is None
    )
    assert (
        compare_images("xvg_test/rama_Gly.png", "xvg_test/test_Gly.png", 0.001) is None
    )
    os.remove("xvg_test/test_General.png")
    os.remove("xvg_test/test_Gly.png")
    if "test_Pre-PRO.png" in os.listdir("xvg_test"):
        os.remove("xvg_test/test_Pre-PRO.png")
    if "test_PRO.png" in os.listdir("xvg_test"):
        os.remove("xvg_test/test_PRO.png")
    out, err = capfd.readouterr()
    assert out == output


def test_xvg_compare():
    XVG.xvg_compare(
        ["xvg_test/gyrate.xvg", "xvg_test/rmsd.xvg"],
        [[1, 2], [1]],
        ["Rg(nm)", "RgX(nm)", "RMSD(nm)"],
        xlabel="Time(ps)",
        ylabel="",
        title="Comparison",
        noshow=True,
        outpng="xvg_test/test1.png",
    )
    assert filecmp.cmp("xvg_test/xvg_compare.png", "xvg_test/test1.png")
    assert (
        compare_images("xvg_test/xvg_compare.png", "xvg_test/test1.png", 0.001) is None
    )

    XVG.xvg_compare(
        ["xvg_test/gyrate.xvg", "xvg_test/rmsd.xvg"],
        [[1, 2], [1]],
        ["Rg(nm)", "RgX(nm)", "RMSD(nm)"],
        xlabel="Time(ps)",
        ylabel="",
        title="Comparison",
        noshow=True,
        outpng="xvg_test/test2.png",
        showMV=True,
        windowsize=50,
        confidence=0.95,
    )
    assert filecmp.cmp("xvg_test/xvg_compare_mv.png", "xvg_test/test2.png")
    assert (
        compare_images("xvg_test/xvg_compare_mv.png", "xvg_test/test2.png", 0.001)
        is None
    )

    XVG.xvg_compare(
        ["xvg_test/gyrate.xvg", "xvg_test/rmsd.xvg"],
        [[1, 2], [1]],
        ["Rg(nm)", "RgX(nm)", "RMSD(nm)"],
        xlabel="Time(ps)",
        ylabel="",
        title="Comparison",
        noshow=True,
        outpng="xvg_test/test3.png",
        start=1000,
        end=3001,
    )
    assert filecmp.cmp("xvg_test/xvg_compare_se.png", "xvg_test/test3.png")
    assert (
        compare_images("xvg_test/xvg_compare_se.png", "xvg_test/test3.png", 0.001)
        is None
    )

    os.remove("xvg_test/test1.png")
    os.remove("xvg_test/test2.png")
    os.remove("xvg_test/test3.png")


def test_xvg_bar_compare():
    XVG.xvg_bar_compare(
        [
            ["xvg_test/bar_0_0.xvg", "xvg_test/bar_0_1.xvg"],
            ["xvg_test/bar_1_0.xvg", "xvg_test/bar_1_1.xvg"],
        ],
        [1, 2],
        ["bar_0", "bar_1"],
        ["Hbond", "Pairs"],
        output="xvg_test/test1.png",
        ylabel="number",
        title="hbond number comparision",
        noshow=True,
        ave2csv="xvg_test/test1.csv",
    )
    assert filecmp.cmp("xvg_test/bar_ave.csv", "xvg_test/test1.csv")
    assert filecmp.cmp("xvg_test/ave_bar.png", "xvg_test/test1.png")
    assert compare_images("xvg_test/ave_bar.png", "xvg_test/test1.png", 0.001) is None

    XVG.xvg_bar_compare(
        [
            ["xvg_test/bar_0_0.xvg", "xvg_test/bar_0_1.xvg"],
            ["xvg_test/bar_1_0.xvg", "xvg_test/bar_1_1.xvg"],
        ],
        [1, 2],
        ["bar_0", "bar_1"],
        ["Hbond", "Pairs"],
        output="xvg_test/test2.png",
        ylabel="number",
        title="hbond number comparision",
        noshow=True,
        ave2csv="xvg_test/test2.csv",
        start=3000,
        end=4001,
    )
    assert filecmp.cmp("xvg_test/bar_ave_se.csv", "xvg_test/test2.csv")
    assert filecmp.cmp("xvg_test/ave_bar_se.png", "xvg_test/test2.png")
    assert (
        compare_images("xvg_test/ave_bar_se.png", "xvg_test/test2.png", 0.001) is None
    )

    os.remove("xvg_test/test1.png")
    os.remove("xvg_test/test1.csv")
    os.remove("xvg_test/test2.png")
    os.remove("xvg_test/test2.csv")


def test_xvg_box_compare():
    XVG.xvg_box_compare(
        ["xvg_test/bar_0_0.xvg", "xvg_test/bar_0_1.xvg", "xvg_test/bar_1_0.xvg"],
        [1, 2],
        ["Hbond", "Pairs"],
        ylabel="number",
        title="Box Comparison",
        noshow=True,
        outpng="xvg_test/test1.png",
    )
    assert filecmp.cmp("xvg_test/xvg_box.png", "xvg_test/test1.png")
    assert compare_images("xvg_test/xvg_box.png", "xvg_test/test1.png", 0.001) is None

    XVG.xvg_box_compare(
        ["xvg_test/bar_0_0.xvg", "xvg_test/bar_0_1.xvg", "xvg_test/bar_1_0.xvg"],
        [1, 2],
        ["Hbond", "Pairs"],
        start=3000,
        end=4001,
        ylabel="number",
        title="Box Comparison",
        noshow=True,
        outpng="xvg_test/test2.png",
    )
    assert filecmp.cmp("xvg_test/xvg_box_se.png", "xvg_test/test2.png")
    assert (
        compare_images("xvg_test/xvg_box_se.png", "xvg_test/test2.png", 0.001) is None
    )

    os.remove("xvg_test/test1.png")
    os.remove("xvg_test/test2.png")


def test_xvg_calc_ave(capfd):
    XVG.xvg_calc_ave("xvg_test/gyrate.xvg")
    output = """\n-------------------------------------------------------------------------------
                       Time (ps)              Rg         Rg\\sX\\N         Rg\\sY\\N         Rg\\sZ\\N
             ave      20000.0000          3.8014          2.7891          2.8660          3.5743
             std      11549.8918          0.0391          0.2391          0.2224          0.1702\n"""
    out, err = capfd.readouterr()
    assert out == output

    XVG.xvg_calc_ave("xvg_test/gyrate.xvg", start=2000)
    output = """\n-------------------------------------------------------------------------------
                       Time (ps)              Rg         Rg\\sX\\N         Rg\\sY\\N         Rg\\sZ\\N
             ave      30000.0000          3.7775          2.8920          2.8154          3.4834
             std       5776.3887          0.0286          0.1741          0.2253          0.1884\n"""
    out, err = capfd.readouterr()
    assert out == output

    XVG.xvg_calc_ave("xvg_test/gyrate.xvg", start=2000, end=3001)
    output = """\n-------------------------------------------------------------------------------
                       Time (ps)              Rg         Rg\\sX\\N         Rg\\sY\\N         Rg\\sZ\\N
             ave      30000.0000          3.7775          2.8920          2.8154          3.4834
             std       5776.3887          0.0286          0.1741          0.2253          0.1884\n"""
    output = """\n-------------------------------------------------------------------------------
                       Time (ps)              Rg         Rg\\sX\\N         Rg\\sY\\N         Rg\\sZ\\N
             ave      25000.0000          3.7809          2.8940          2.6588          3.6148
             std       2889.6367          0.0265          0.2011          0.1824          0.0836\n"""
    out, err = capfd.readouterr()
    assert out == output


def test_xvg_calc_mvave2csv():
    XVG.xvg_calc_mvave2csv("xvg_test/gyrate.xvg", "xvg_test/test1.csv")
    assert filecmp.cmp("xvg_test/xvg_mvave1.csv", "xvg_test/test1.csv")
    XVG.xvg_calc_mvave2csv(
        "xvg_test/gyrate.xvg", "xvg_test/test2.csv", windowsize=100, confidence=0.95
    )
    assert filecmp.cmp("xvg_test/xvg_mvave2.csv", "xvg_test/test2.csv")

    os.remove("xvg_test/test1.csv")
    os.remove("xvg_test/test2.csv")


def test_xvg2csv():
    XVG.xvg2csv("xvg_test/gyrate.xvg", "xvg_test/test.csv")
    assert filecmp.cmp("xvg_test/xvg2csv.csv", "xvg_test/test.csv")
    os.remove("xvg_test/test.csv")


def test_xvg_show():
    XVG.xvg_show("xvg_test/rmsd.xvg", "xvg_test/test.png", noshow=True)
    assert filecmp.cmp("xvg_test/xvg_show.png", "xvg_test/test.png")
    assert compare_images("xvg_test/xvg_show.png", "xvg_test/test.png", 0.001) is None
    os.remove("xvg_test/test.png")


def test_xvg_show_distribution():
    XVG.xvg_show_distribution("xvg_test/rmsd.xvg", 50, "xvg_test/test.png", True)
    assert filecmp.cmp("xvg_test/xvg_show_distribution.png", "xvg_test/test.png")
    assert (
        compare_images("xvg_test/xvg_show_distribution.png", "xvg_test/test.png", 0.001)
        is None
    )
    os.remove("xvg_test/test.png")


def test_xvg_show_stacking():
    XVG.xvg_show_stacking(
        "xvg_test/dssp_sc.xvg", [2, 3, 4, 5, 6], outpng="xvg_test/test.png", noshow=True
    )
    assert filecmp.cmp("xvg_test/xvg_stack.png", "xvg_test/test.png")
    assert compare_images("xvg_test/xvg_stack.png", "xvg_test/test.png", 0.001) is None
    os.remove("xvg_test/test.png")


def test_xvg_show_scatter():
    XVG.xvg_show_scatter(
        "xvg_test/xvg_combined.xvg",
        x_index=1,
        y_index=2,
        outpng="xvg_test/test.png",
        noshow=True,
    )
    assert filecmp.cmp("xvg_test/xvg_scatter.png", "xvg_test/test.png")
    assert (
        compare_images("xvg_test/xvg_scatter.png", "xvg_test/test.png", 0.001) is None
    )
    os.remove("xvg_test/test.png")
