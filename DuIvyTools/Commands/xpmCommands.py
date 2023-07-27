"""
xpmCommander module is part of DuIvyTools providing xpm related commands.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

from Commands.Commands import Command
from FileParser.xpmParser import XPM, XPMS
from Visualizor.Visualizer_matplotlib import LineMatplotlib
from utils import Parameters


class xpm_show(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  ## write process code

        self.info("in xpm_show")
        print(self.parm.__dict__)


class xpm2csv(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xpm2csv")
        print(self.parm.__dict__)


class xpm2dat(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xpm2dat")
        print(self.parm.__dict__)


class xpm2gpl(Command):  ## need ???
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xpm2gpl")
        print(self.parm.__dict__)