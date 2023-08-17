"""
otherCommander module is part of DuIvyTools providing basic commands.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Tuple, Union

import numpy as np
import pandas as pd

from Commands.Commands import Command
from utils import Parameters
from FileParser.xpmParser import XPM
from FileParser.groParser import GRO
from FileParser.ndxParser import NDX


class mdp_gen(Command):
    """a command class to generate mdp file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in mdp_gen")
        print(self.parm.__dict__)

        mdp_path = os.path.realpath(
            os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                os.path.join("..", "data", "mdps"),
            )
        )
        mdp_files = [f for f in os.listdir(mdp_path) if f.endswith(".mdp")]
        if self.parm.output != None and self.parm.output not in mdp_files:
            self.warn(
                f'the specified output file "{self.parm.output}" were unable to provide'
            )
            self.parm.output = None
        if self.parm.output == None:
            print("-" * 70)
            print(
                "You can get one of the following mdp file by specifing the output parameter: \n"
            )
            print("  ".join(mdp_files))
            print("-" * 70)
        if self.parm.output in mdp_files:
            with open(os.path.join(mdp_path, self.parm.output), "r") as fo:
                content = fo.read()
            self.parm.output = self.check_output_exist(self.parm.output)
            with open(self.parm.output, "w") as fo:
                fo.write(content)
            self.info(f"generated {self.parm.output} successfully")


class show_style(Command):
    """a command class to generate matplotlib style file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in show_style")
        print(self.parm.__dict__)

        mplstyle_path = os.path.realpath(
            os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                os.path.join("..", "data", "mplstyle"),
            )
        )
        mplstyle_files = [
            f for f in os.listdir(mplstyle_path) if f.endswith(".mplstyle")
        ]

        if self.parm.output != None and self.parm.output not in mplstyle_files:
            self.warn(
                f'the specified output file "{self.parm.output}" were unable to provide'
            )
            print("-" * 70)
            print(
                "You can get one of the following mplstyle file by specifing the output parameter: \n"
            )
            print("  ".join(mplstyle_files))
            print("-" * 70)
        elif self.parm.output == None:
            self.parm.output = "DIT.mplstyle"
        if self.parm.output != None and self.parm.output in mplstyle_files:
            with open(os.path.join(mplstyle_path, self.parm.output), "r") as fo:
                content = fo.read()
            self.parm.output = self.check_output_exist(self.parm.output)
            with open(self.parm.output, "w") as fo:
                fo.write(content)
            self.info(f"generated {self.parm.output} successfully")


class find_center(Command):
    """a command class to find out the center of one group of atoms"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in find_center")
        print(self.parm.__dict__)

        ## read user input
        if self.parm.input == None:
            self.error(
                "you must specify a gro file (or with an index file) for finding atom group center"
            )
        else:
            indexfile, grofile = "", ""
            if ".gro" in "".join(self.parm.input):
                for file in self.parm.input:
                    if file.endswith(".gro") and grofile == "":
                        grofile = file
                        self.info(f"{file} has been used as gro file")
            if ".ndx" in "".join(self.parm.input):
                for file in self.parm.input:
                    if file.endswith(".ndx") and indexfile == "":
                        indexfile = file
                        self.info(f"{file} has been used as index file")
        if grofile == "":
            self.error(
                "you must specify a gro file (or with an index file) for finding atom group center"
            )

        ## deal with logic
        gro = GRO(grofile)
        if indexfile == "":
            indexs = [i for i in range(1, gro.atom_number + 1)]
        else:
            ndx = NDX(indexfile)
            print(ndx.show_names)
            indexs: Union[List[int], None] = None
            while indexs == None:
                name = input("==> select a group to calculate center: ")
                indexs = ndx[name]
                if indexs == None:
                    print(">> wrong selection, no atom indexs fetched")
        ## calculate the center point
        center_x, center_y, center_z = 0, 0, 0
        for i in indexs:
            coor = gro.frames[0][i - 1].coor
            center_x += coor[0]
            center_y += coor[1]
            center_z += coor[2]
        center_x = center_x / len(indexs)
        center_y = center_y / len(indexs)
        center_z = center_z / len(indexs)
        self.info(
            "the center point is ({:.3f}, {:.3f}, {:.3f})".format(
                center_x, center_y, center_z
            )
        )
        ## find the closed atom
        AllAtoms: bool = False
        if self.parm.mode == "AllAtoms":
            AllAtoms = True
        atom_info = ""
        dist = 5  # nm, find closed atom in sphere of 5 nm
        for i, atom in enumerate(gro.frames[0]):
            if (not AllAtoms) and (i + 1 not in indexs):
                continue
            x = atom.coor[0]
            y = atom.coor[1]
            z = atom.coor[2]
            atom_center_dist = (
                (x - center_x) ** 2 + (y - center_y) ** 2 + (z - center_z) ** 2
            ) ** 0.5
            if atom_center_dist < dist:
                dist = atom_center_dist
                atom_info = str(atom)
        if atom_info == "":
            self.info("no atom detected in 5.0 nm sphere of center point. ")
        else:
            self.info(f"distance from nearest atom to center: {dist:.3f} nm")
            print("--------------------------------------------")
            print("ResID Name Atom  Num       X       Y       Z")
            print("--------------------------------------------")
            print(atom_info)
            print("--------------------------------------------")


class dccm_ascii(Command):
    """a command class to convert dccm in ascii data file into xpm file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in dccm_ascii")
        print(self.parm.__dict__)

        ## check parameters
        if not self.parm.input:
            self.error(
                "you must specify ascii data file generated by 'gmx dccm' for input"
            )
        if len(self.parm.input) > 1:
            self.warn(f"only the first file {self.parm.input[0]} will be used")
        if not self.parm.output:
            self.error("you must specify a XPM file for output")
        if not os.path.exists(self.parm.input[0]):
            self.error(f"no {self.parm.input[0]} in current directory")

        ## read ascii
        covar = pd.read_csv(self.parm.input[0], sep=" ", header=None)
        resnum = int(np.sqrt((covar.shape[0]) / 3))
        results = pd.DataFrame()
        for i in range(resnum):
            one_N = pd.DataFrame()
            for j in range(
                (i * resnum) * 3, int(len(covar) / resnum) * (i + 1), resnum
            ):
                df = covar[j : resnum + j].reset_index(drop=True)
                one_N = pd.concat([one_N, df], ignore_index=True, axis=1)
            results = pd.concat([results, one_N], ignore_index=True, axis=0)
        results["sum"] = results.sum(axis=1)
        covar = results["sum"].to_numpy()
        covar = covar.reshape(resnum, resnum)
        ## convert covar to corr
        if self.parm.z_precision == None:
            self.parm.z_precision = 3
        corr = np.zeros((resnum, resnum))
        for i in range(resnum):
            for j in range(resnum):
                corr_ij = covar[i, j] / np.sqrt(covar[i, i] * covar[j, j])
                corr[i, j] = float(f"{corr_ij:.{self.parm.z_precision}f}")

        ## save to xpm
        xpm = XPM(self.parm.output, is_file=False, new_file=True)
        xpm.title = "DCCM by DIT"
        xpm.type = "Continuous"
        xpm.xlabel = "Residue No."
        xpm.ylabel = "Residue No."
        xpm.width = resnum
        xpm.height = resnum
        xpm.value_matrix = corr.tolist()
        xpm.xaxis = [i + 1 for i in range(resnum)]
        xpm.yaxis = [i + 1 for i in range(resnum)]
        xpm.yaxis.reverse()
        xpm.value_matrix.reverse()
        xpm.refresh_by_value_matrix()
        self.parm.output = self.check_output_exist(self.parm.output)
        xpm.save(self.parm.output)


class dssp(Command):
    """a command class to convert dssp data (gmx2023) into dssp xpm file
    
    input :str gmx2023 dssp data file
    output :str the outname of several files
    xlabel :str
    ylabel :str
    title :str
    columns :List[int] for residue number
    begin :int time beginning
    end :int time ending
    dt :int time gap
    """

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in dssp")
        print(self.parm.__dict__)

        ## for 2023, read in dat file and output normal xpm and ss.xvg
        if not self.parm.input:
            self.error(
                "you must specify data file generated by 'gmx2023 dssp' for input"
            )
        if len(self.parm.input) > 1:
            self.warn(f"only the first file {self.parm.input[0]} will be used")
        if not os.path.exists(self.parm.input[0]):
            self.error(f"no {self.parm.input[0]} in current directory")
        datafile :str = self.parm.input[0]
        outname = "dit_dssp_gmx2023"
        if self.parm.output:
            outname = self.parm.output
        outxpm :str = f"{outname}.xpm"
        outxvg_sc :str = f"{outname}_sc.xvg"
        outxvg_res :str = f"{outname}_residue.xvg"
        for file in [outxpm, outxvg_sc, outxvg_res]:
            new_file = self.check_output_exist(file)
            if new_file != file:
                outname = new_file.split(".")[0]
                outxpm :str = f"{outname}.xpm"
                outxvg_sc :str = f"{outname}_sc.xvg"
                outxvg_res :str = f"{outname}_residue.xvg"
                break

        ## the infos were get from https://github.com/gromacs/gromacs/blob/main/src/gromacs/trajectoryanalysis/modules/dssp.cpp#L220
        dssp_symbols_dict = {
            "~": "Loops",       # Loop
            "=": "Breaks",      # Break
            "S": "Bends",       # Bend
            "T": "Turns",       # Turn
            "P": "PP_Helices",  # Helix_PP
            "I": "π-Helices",   # Helix_5
            "G": "3⏨-Helices",  # Helix_3
            "E": "β-Strands",   # Strands
            "B": "β-Bridges",   # Bridge
            "H": "α-Helices",   # Helix_4
        }
        infos = """
        One-symbol secondary structure designations that are used in the output file:
        H — alpha-helix;
        B — residue in isolated beta-bridge;
        E — extended strand that participates in beta-ladder;
        G — 3_10_-helix;
        I — pi-helix;
        P — kappa-helix (poly-proline II helix);
        S — bend;
        T — hydrogen-bonded turn;
        = — break;
        ~ — loop (no special secondary structure designation).
        """
        
        # deal with logic
        xpm = XPM(outxpm, new_file=True)
        xpm.title = self.sel_parm(self.parm.title, "Secondary Structure")
        xpm.xlabel = self.sel_parm(self.parm.xlabel, "Time (ps)")
        xpm.ylabel = self.sel_parm(self.parm.ylabel, "Residue")
        xpm.type = "Discrete"


        with open(datafile, 'r') as fo:
            lines = fo.readlines()
        
