"""
pdbParser module is part of DuIvyTools for parsing the pdb file generated by GROMACS.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class Atom(object):
    def __init__(self, line: str) -> None:
        self.atom_id = int(line[6:11].strip())
        self.atom_name = line[12:16].strip()
        self.res_name = line[17:20].strip()
        self.chain_id = self.__blank(line[21])
        self.res_id = int(line[22:26].strip())
        self.coor_x = float(line[30:38].strip())
        self.coor_y = float(line[38:46].strip())
        self.coor_z = float(line[46:54].strip())
        self.coor = (self.coor_x, self.coor_y, self.coor_z)
        self.occupancy = self.__blank(line[54:60], True)
        self.tempfactor = self.__blank(line[60:66], True)
        self.symbol = self.__blank(line[76:78])
        self.charge = self.__blank(line[78:80], True)

    def __blank(self, item: str, float_flag: bool = False):
        if item.strip() == "":
            return None
        else:
            if float_flag:
                return float(item.strip())
            else:
                return item.strip()


class PDB(log):
    """PDB class for parsing PDB file"""

    def __init__(self, pdbfile: str) -> None:
        self.model_num: int = 0
        self.atom_number: int = 0
        self.models: list[list[Atom]] = []

        if not os.path.exists(pdbfile):
            self.error(f"No {pdbfile} detected ! check it !")
        with open(pdbfile, "r") as fo:
            lines = [l.strip() for l in fo.readlines()]
        atom_list: list[Atom] = []
        for line in lines:
            if line.startswith("ENDMDL") and len(atom_list) != 0:
                self.model_num += 1
                self.models.append(atom_list)
                self.atom_number = len(atom_list)
                atom_list = []
            if line.startswith("ATOM") or line.startswith("HETATM"):
                atom_list.append(Atom(line))
        if len(atom_list) != 0:
            self.model_num += 1
            self.models.append(atom_list)
            self.atom_number = len(atom_list)


def main():
    pdb = PDB("../../test/prolig/prolig.pdb")
    print(pdb.atom_number)
    print(pdb.model_num)
    print(pdb.models[0][100].__dict__)
