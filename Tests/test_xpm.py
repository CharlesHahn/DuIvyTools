## author : charlie
## date : 20220826

import os
import sys
import pytest
import filecmp
from matplotlib.testing.compare import compare_images

# https://matplotlib.org/3.1.1/api/testing_api.html
# assert filecmp.cmp("ndx_test/hbond.ndx", "ndx_test/test.ndx", shallow=True)

sys.path.append("../DuIvyTools/")
import XPM


def test_xpm_init_continuous():
    xpm = XPM.XPM("xpm_test/gibbs.xpm")
    assert xpm.xpmfile == "xpm_test/gibbs.xpm"
    assert xpm.xpm_title == "Gibbs Energy Landscape"
    assert xpm.xpm_legend == "G (kJ/mol)"
    assert xpm.xpm_type == "Continuous"
    assert xpm.xpm_xlabel == "PC1"
    assert xpm.xpm_ylabel == "PC2"
    assert xpm.xpm_width == 32
    assert xpm.xpm_height == 32
    assert xpm.xpm_color_num == 100
    assert xpm.xpm_char_per_pixel == 2
    assert xpm.chars[:8] == ["AA", "BA", "CA", "DA", "EA", "FA", "GA", "HA"]
    assert xpm.chars[-8:] == ["EB", "FB", "GB", "HB", "IB", "JB", "KB", "LB"]
    assert xpm.colors[:4] == ["#000000", "#030303", "#050505", "#080808"]
    assert xpm.colors[-4:] == ["#F7F7F7", "#FAFAFA", "#FCFCFC", "#FFFFFF"]
    assert xpm.notes[:5] == ["0", "0.128", "0.256", "0.383", "0.511"]
    assert xpm.notes[-5:] == ["12.1", "12.3", "12.4", "12.5", "12.7"]
    assert xpm.colors_rgb[:4] == [[0, 0, 0], [3, 3, 3], [5, 5, 5], [8, 8, 8]]
    assert xpm.colors_rgb[-4:-1] == [[247, 247, 247], [250, 250, 250], [252, 252, 252]]
    assert xpm.xpm_xaxis[:5] == [
        -6.707990000000001,
        -6.32191,
        -5.93583,
        -5.5497499999999995,
        -5.16367,
    ]
    assert xpm.xpm_xaxis[-5:] == [3.71614, 4.10222, 4.4883, 4.87438, 5.26046]
    assert xpm.xpm_yaxis[:5] == [
        3.7110950000000003,
        3.46736,
        3.223625,
        2.97989,
        2.736155,
    ]
    assert xpm.xpm_yaxis[-5:] == [
        -2.8697749999999997,
        -3.1135099999999998,
        -3.357245,
        -3.60098,
        -3.844715,
    ]
    assert (
        xpm.xpm_datalines[0]
        == "LBLBLBLBLBLBLBLBLBLBLBDBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLB"
    )
    assert (
        xpm.xpm_datalines[12]
        == "LBLBLB}A*A@AiAeASAPAPAVAtA}ALBLBLBLBLBLBLBLBLB3AiAPALAJATAnADBDB"
    )
    assert (
        xpm.xpm_datalines[-1]
        == "LBLBLBLBLBLBLBDBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLBLB"
    )


def test_xpm_init_discrete():
    xpm = XPM.XPM("xpm_test/hbond.xpm")
    assert xpm.xpmfile == "xpm_test/hbond.xpm"
    assert xpm.xpm_title == "Hydrogen Bond Existence Map"
    assert xpm.xpm_legend == "Hydrogen Bonds"
    assert xpm.xpm_type == "Discrete"
    assert xpm.xpm_xlabel == "Time (ps)"
    assert xpm.xpm_ylabel == "Hydrogen Bond Index"
    assert xpm.xpm_width == 4001
    assert xpm.xpm_height == 8
    assert xpm.xpm_color_num == 2
    assert xpm.xpm_char_per_pixel == 1
    assert xpm.chars == [" ", "o"]
    assert xpm.colors == ["#FFFFFF", "#FF0000"]
    assert xpm.notes == ["None", "Present"]
    assert xpm.colors_rgb == [[255, 255, 255], [255, 0, 0]]
    assert xpm.xpm_xaxis == [i for i in range(60000, 100001, 10)]
    assert xpm.xpm_yaxis == [7, 6, 5, 4, 3, 2, 1, 0]
    assert (
        xpm.xpm_datalines[0]
        == "                                                                                             o                                                                                                                 o oooo o                                                                                                                                                                           o                                                                                                                                                                                                                                                                                                                                                                                                                                                                         o     o                                            o                             oo                                  o                                                                                                                                                        o                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            oo                                                                                                                                                                                                                          ooooooooo                                                                                                                                                                                                                                                                                                                                                                      o o                                                       o           o      o ooo  o ooo ooo   oo   o o oooo         o                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        "
    )


def test_xpm_xpm2csv():
    xpm = XPM.XPM(
        "xpm_test/gibbs.xpm",
        "prominent component 1",
        "prominent conponent 2",
        "gibbs energy",
    )
    xpm.xpm2csv("xpm_test/test.csv")
    assert filecmp.cmp("xpm_test/test.csv", "xpm_test/gibbs2csv.csv")
    os.remove("xpm_test/test.csv")


def test_xpm_xpm2gpl():
    xpm = XPM.XPM("xpm_test/gibbs.xpm")
    xpm.xpm2gpl("xpm_test/test.gpl")
    assert filecmp.cmp("xpm_test/test.gpl", "xpm_test/gibbs2gpl.gpl")
    os.remove("xpm_test/test.gpl")
    xpm = XPM.XPM("xpm_test/hbond.xpm", xlabel="Time (ns)", xshrink=0.001)
    xpm.xpm2gpl("xpm_test/test.gpl")
    assert filecmp.cmp("xpm_test/test.gpl", "xpm_test/hbond2gpl.gpl")
    os.remove("xpm_test/test.gpl")
    xpm = XPM.XPM("xpm_test/dssp.xpm", xlabel="Time (ns)", xshrink=0.001)
    xpm.xpm2gpl("xpm_test/test.gpl")
    assert filecmp.cmp("xpm_test/test.gpl", "xpm_test/dssp2gpl.gpl")
    os.remove("xpm_test/test.gpl")


def test_xpm_draw_origin():
    xpm = XPM.XPM("xpm_test/hbond.xpm", xlabel="Time (ns)", xshrink=0.001)
    xpm.draw_origin(False, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/hbond_draw_origin.png")
    assert (
        compare_images("xpm_test/test.png", "xpm_test/hbond_draw_origin.png", 0.001)
        is None
    )
    os.remove("xpm_test/test.png")

    xpm = XPM.XPM("xpm_test/dssp.xpm", xlabel="Time (ns)", xshrink=0.001)
    xpm.draw_origin(False, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/dssp_draw_origin.png")
    assert (
        compare_images("xpm_test/test.png", "xpm_test/dssp_draw_origin.png", 0.001)
        is None
    )
    os.remove("xpm_test/test.png")

    xpm = XPM.XPM("xpm_test/gibbs.xpm")
    xpm.draw_origin(False, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/gibbs_draw_origin.png")
    assert (
        compare_images("xpm_test/test.png", "xpm_test/gibbs_draw_origin.png", 0.001)
        is None
    )
    os.remove("xpm_test/test.png")

    xpm.draw_origin(True, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/gibbs_draw_origin_ip.png")
    assert (
        compare_images("xpm_test/test.png", "xpm_test/gibbs_draw_origin_ip.png", 0.001)
        is None
    )
    os.remove("xpm_test/test.png")


def test_xpm_draw_pcm():
    xpm = XPM.XPM("xpm_test/gibbs.xpm")
    xpm.draw_pcm(False, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/gibbs_pcm.png")
    assert compare_images("xpm_test/test.png", "xpm_test/gibbs_pcm.png", 0.001) is None
    os.remove("xpm_test/test.png")

    xpm.draw_pcm(True, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/gibbs_pcm_ip.png")
    assert (
        compare_images("xpm_test/test.png", "xpm_test/gibbs_pcm_ip.png", 0.001) is None
    )
    os.remove("xpm_test/test.png")


def test_xpm_draw_3D():
    xpm = XPM.XPM("xpm_test/gibbs.xpm")
    xpm.draw_3D(False, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/gibbs_3d.png")
    assert compare_images("xpm_test/test.png", "xpm_test/gibbs_3d.png", 0.001) is None
    os.remove("xpm_test/test.png")

    xpm.draw_3D(True, "xpm_test/test.png", True)
    assert filecmp.cmp("xpm_test/test.png", "xpm_test/gibbs_3d_ip.png")
    assert (
        compare_images("xpm_test/test.png", "xpm_test/gibbs_3d_ip.png", 0.001) is None
    )
    os.remove("xpm_test/test.png")
