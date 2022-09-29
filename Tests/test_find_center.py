
## author : charlie
## date : 20220823

import os
import sys
import pytest
import filecmp


sys.path.append("../DuIvyTools/")
from FindCenter import find_center


def test_ndx_show_ndx(capfd):
    gro_file = "find_center_test/test.gro"
    find_center(gro_file)
    out, err = capfd.readouterr()
    assert (
        out == """--------------------------------------------
ResID Name Atom  Num       X       Y       Z
--------------------------------------------
14509SOL    HW144693   4.042   4.159   4.131 -2.8704  2.1028 -0.3357
--------------------------------------------
""")
