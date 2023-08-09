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

        if not self.parm.input:
            self.error("you must specify a xpm file for converting to csv file")
        if len(self.parm.input) > 1:
            self.warn("only the first xpm file you specified will be used !")
        if not self.parm.output:
            self.error("you must specify a csv file to store results")
        self.parm.output = self.check_output_exist(self.parm.output)

        xpm = XPM(self.parm.input[0])
        with open(self.parm.output, "w") as fo:
            if xpm.type != "Continuous":
                fo.write("#### DIT: it's not a Continuous type xpm file\n")
                fo.write("#### labels of values were recorded below: \n")
                for index, label in enumerate(xpm.notes):
                    fo.write(f"#### {index} : {label}\n")
            x_title = (xpm.xlabel, "x-axis")[len(xpm.xlabel) == 0]
            y_title = (xpm.ylabel, "y-axis")[len(xpm.ylabel) == 0]
            z_title = (xpm.legend, "value")[len(xpm.legend) == 0]
            x_title = self.sel_parm(self.parm.xlabel, x_title)
            y_title = self.sel_parm(self.parm.ylabel, y_title)
            z_title = self.sel_parm(self.parm.zlabel, z_title)
            fo.write(f"{x_title},{y_title},{z_title}\n")
            for y, y_value in enumerate(xpm.yaxis):
                for x, x_value in enumerate(xpm.xaxis):
                    z_value = xpm.value_matrix[y][x]
                    x_value *= self.parm.xshrink
                    y_value *= self.parm.yshrink
                    z_value *= self.parm.zshrink
                    fo.write(f"{x_value:.6f},{y_value:.6f},{z_value:.6f}\n")
        self.info(f"extract data from {xpm.xpmfile} successfully")
        self.info(f"data are saved into {self.parm.output}")


class xpm2dat(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xpm2dat")
        print(self.parm.__dict__)


class xpm_diff(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xpm_diff")
        print(self.parm.__dict__)
