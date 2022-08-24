## author : charlie
## date : 20220823

import os
import sys
import pytest 
import filecmp
# assert filecmp.cmp("ndx_test/hbond.ndx", "ndx_test/test.ndx", shallow=True)

sys.path.append("../DuIvyTools/")
from NDX import NDX


def test_ndx_init():
    ndx_file = "ndx_test/hbond.ndx"
    ndx = NDX(ndx_file)
    assert ndx.ndx_filename == ndx_file
    assert ndx.group_number == 4
    assert ndx.group_name_list == ["Protein", "1ZIN", "1ZIN", "hbonds_Protein-1ZIN"]
    assert ndx.group_index_list[0] == [i for i in range(1, 1126)]
    assert ndx.group_index_list[1] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[-1] == [617, 618, 1133, 833, 834, 1133, 992, 993, 1155, 996, 997, 1155]

def test_ndx_show_ndx(capfd):
    ndx_file = "ndx_test/hbond.ndx"
    ndx = NDX(ndx_file)
    ndx.show_ndx()
    out, err = capfd.readouterr()
    print(out)
    assert out == "   0 -> Protein\n   1 -> 1ZIN\n   2 -> 1ZIN\n   3 -> hbonds_Protein-1ZIN\n"

def test_ndx_write_ndx():
    ndx_file = "ndx_test/hbond.ndx"
    out_file = "ndx_test/test.ndx"
    ndx = NDX(ndx_file)
    ndx.write_ndx(out_file)
    out = NDX(out_file)
    assert ndx.group_number == out.group_number
    assert ndx.group_name_list == out.group_name_list
    assert ndx.group_index_list == out.group_index_list
    os.remove("ndx_test/test.ndx")

def test_ndx_remove_duplicate():
    ndx_file = "ndx_test/hbond.ndx"
    out_file = "ndx_test/test.ndx"
    ndx = NDX(ndx_file)
    ndx.remove_duplicate(out_file)
    os.remove("ndx_test/test.ndx")
    assert ndx.group_number == 3
    assert ndx.group_name_list == ["Protein", "1ZIN", "hbonds_Protein-1ZIN"]
    assert ndx.group_index_list[0] == [i for i in range(1, 1126)]
    assert ndx.group_index_list[1] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[-1] == [617, 618, 1133, 833, 834, 1133, 992, 993, 1155, 996, 997, 1155]

def test_ndx_remove_group():
    ndx_file = "ndx_test/hbond.ndx"
    out_file = "ndx_test/test.ndx"
    ndx = NDX(ndx_file)
    ndx.remove_group(out_file, ["1ZIN"])
    os.remove("ndx_test/test.ndx")
    assert ndx.group_number == 2
    assert ndx.group_name_list == ["Protein", "hbonds_Protein-1ZIN"]
    assert ndx.group_index_list[0] == [i for i in range(1, 1126)]
    assert ndx.group_index_list[-1] == [617, 618, 1133, 833, 834, 1133, 992, 993, 1155, 996, 997, 1155]

def test_ndx_preserve_group():
    ndx_file = "ndx_test/hbond.ndx"
    out_file = "ndx_test/test.ndx"
    ndx = NDX(ndx_file)
    ndx.preserve_group(out_file, ["1ZIN", "hbonds_Protein-1ZIN"])
    os.remove("ndx_test/test.ndx")
    assert ndx.group_number == 3
    assert ndx.group_name_list == ["1ZIN", "1ZIN", "hbonds_Protein-1ZIN"]
    assert ndx.group_index_list[0] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[1] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[-1] == [617, 618, 1133, 833, 834, 1133, 992, 993, 1155, 996, 997, 1155]

def test_ndx_combine_group():
    ndx_file = "ndx_test/hbond.ndx"
    out_file = "ndx_test/test.ndx"
    ndx = NDX(ndx_file)
    ndx.combine_group(out_file, "ProLig", ["Protein", "1ZIN"])
    os.remove("ndx_test/test.ndx")
    assert ndx.group_number == 5
    assert ndx.group_name_list == ["Protein", "1ZIN", "1ZIN", "hbonds_Protein-1ZIN", "ProLig"]
    assert ndx.group_index_list[0] == [i for i in range(1, 1126)]
    assert ndx.group_index_list[1] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[2] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[3] == [617, 618, 1133, 833, 834, 1133, 992, 993, 1155, 996, 997, 1155]
    assert ndx.group_index_list[4] == [i for i in range(1, 1157)]

def test_ndx_add_group():
    ndx_file = "ndx_test/hbond.ndx"
    out_file = "ndx_test/test.ndx"
    ndx = NDX(ndx_file)
    ndx.add_group(out_file, "test", 2000, 3000)
    os.remove("ndx_test/test.ndx")
    assert ndx.group_number == 5
    assert ndx.group_name_list == ["Protein", "1ZIN", "1ZIN", "hbonds_Protein-1ZIN", "test"]
    assert ndx.group_index_list[0] == [i for i in range(1, 1126)]
    assert ndx.group_index_list[1] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[2] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[3] == [617, 618, 1133, 833, 834, 1133, 992, 993, 1155, 996, 997, 1155]
    assert ndx.group_index_list[4] == [i for i in range(2000, 3000)]
    ndx.add_group(out_file, "test", 2000, 3001, 5)
    os.remove("ndx_test/test.ndx")
    assert ndx.group_index_list[5] == [i for i in range(2000, 3001, 5)]

def test_ndx_rename_group():
    ndx_file = "ndx_test/hbond.ndx"
    out_file = "ndx_test/test.ndx"
    ndx = NDX(ndx_file)
    ndx.rename_group(out_file, "1ZIN", "lig")
    os.remove("ndx_test/test.ndx")
    assert ndx.group_number == 4
    assert ndx.group_name_list == ["Protein", "lig", "lig", "hbonds_Protein-1ZIN"]
    assert ndx.group_index_list[0] == [i for i in range(1, 1126)]
    assert ndx.group_index_list[1] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[2] == [i for i in range(1126, 1157)]
    assert ndx.group_index_list[3] == [617, 618, 1133, 833, 834, 1133, 992, 993, 1155, 996, 997, 1155]
    ndx.rename_group(out_file, "Protein", "pro")
    os.remove("ndx_test/test.ndx")
    assert ndx.group_name_list == ["pro", "lig", "lig", "hbonds_Protein-1ZIN"]
