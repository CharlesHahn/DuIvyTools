"""
ndxParser module is part of DuIvyTools for parsing the ndx file generated by GROMACS.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import math
from typing import Dict, List, Union

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class NDX(log):
    def __init__(self, ndxfile: str, new_file: bool = False) -> None:
        self.name_index: Dict[str, List[int]] = dict()
        self.names: list = []
        self.ndxfile: str = ndxfile

        if not new_file and ndxfile:
            if not os.path.exists(ndxfile):
                self.error(f"No {ndxfile} detected ! check it !")
            with open(ndxfile, "r") as fo:
                lines = [line.strip() for line in fo.readlines()]
            for id, line in enumerate(lines):
                if line.strip() == "":
                    continue
                elif line[0] == "[" and line[-1] == "]":
                    name = line[1:-1].strip()
                    if name in self.name_index.keys():
                        self.warn(
                            f"Repeat group name {name} detected, dropped the former one."
                        )
                        self.names.remove(name)
                    self.name_index[name] = []
                    self.names.append(name)
                else:
                    try:
                        self.name_index[name] += [int(i) for i in line.split()]
                    except:
                        self.error(f"Unable to parse line {id} of {ndxfile}, check it!")
        if len(self.names) != len(self.name_index.keys()):
            self.critical("wrong length in paring ndx file")

    def __len__(self) -> int:
        return len(self.names)

    def __getitem__(self, name: str) -> List[int]:
        return self.name_index[name]

    def __setitem__(self, name: str, indexs: List[int]) -> None:
        self.name_index[name] = indexs
        self.names.append(name)

    def __delitem__(self, name: str) -> None:
        if self.name_index.get(name, 0) == 0:
            self.warn(f"request group {name} not found")
        else:
            del self.name_index[name]
            self.names.remove(name)

    def __str__(self) -> str:
        output: str = ""
        for name, indexs in self.name_index.items():
            output += f"[ {name} ] \n"
            count = math.ceil(len(indexs) / 15)
            for c in range(count):
                items = [f"{v:>4d}" for v in indexs[c * 15 : c * 15 + 15]]
                output += " ".join(items) + "\n"
        output += "\n "
        return output

    def get_id_by_name(self, name: str) -> int:
        return self.names.index(name) + 1

    def formatter(self, name: str, column_num: int) -> str:
        if column_num <= 0:
            self.error("Unable to format indexs by 0 column")
            return ""
        output: str = f"[ {name} ] \n"
        indexs = self.name_index[name]
        count = math.ceil(len(indexs) / column_num)
        for c in range(count):
            items = [f"{v:>4d}" for v in indexs[c * column_num : (c + 1) * column_num]]
            output += " ".join(items) + "\n"
        return output


def main():
    ndx = NDX("../../test/index.ndx")
    for key, value in ndx.name_index.items():
        print(key)
        print(value)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(ndx["1ZIN"])
    print(len(ndx))
    ndx["hhhh"] = [0, 10, 20, -1]
    print(ndx["hhhh"])
    del ndx["System"]
    print(ndx.names)

    print(ndx.formatter("1ZIN", 4))
    print(ndx.formatter("2ZIN", 0))
    print(ndx.formatter("3ZIN", 1))
