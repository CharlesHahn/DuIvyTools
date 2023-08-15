"""
otherCommander module is part of DuIvyTools providing basic commands.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Tuple, Union

import numpy as np

from Commands.Commands import Command
from utils import Parameters


class mdp_gen(Command):
    """a command class to generate mdp file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  
        self.info("in mdp_gen")
        print(self.parm.__dict__)

        mdp_path = os.path.realpath(os.getcwd(), os.path.join(os.path.dirname(__file__), os.path.join("..", "data", "mdps")))
        mdp_files = [f for f in os.listdir(mdp_path) if f.endswith(".mdp")]

        if self.parm.output not in mdp_files:
            self.warn(f"the specified {self.parm.output} were unable to provide")

        if self.parm.output == None:
            print("-"*70)
            print("You can get one of the following mdp file by specifing the output parameter: ")
            print("  ".join(mdp_files))
            print("-"*70)




class show_style(Command):
    """a command class to generate matplotlib style file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  
        self.info("in show_style")
        print(self.parm.__dict__)




class find_center(Command):
    """a command class to find out the center of one group of atoms"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  
        self.info("in find_center")
        print(self.parm.__dict__)




class dccm_ascii(Command):
    """a command class to convert dccm in ascii data file into xpm file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  
        self.info("in dccm_ascii")
        print(self.parm.__dict__)



class dssp(Command):
    """a command class to convert dssp data (gmx2023) into dssp xpm file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  
        self.info("in dssp")
        print(self.parm.__dict__)

