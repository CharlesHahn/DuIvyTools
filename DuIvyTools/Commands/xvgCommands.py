"""
xvgCommander module is part of DuIvyTools providing basic commands.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Commands.Commands import Command
from FileParser.xvgParser import XVG
from Visualizor.Visualizer_matplotlib import LineMatplotlib
from utils import Parameters


class xvgShow(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  ## write process code

        self.info("in xvgSHOW")
        print(self.parm.__dict__)

        for xvgfile in self.parm.input:
            xvg = XVG(xvgfile)
            self.file = xvg

            kwargs = {
                "data_list": xvg.data_columns[1:],
                "xdata": xvg.data_columns[0],
                "legends": self.sel_parm(self.parm.legends, xvg.data_heads[1:]),
                "xmin": self.get_parm("xmin"),
                "xmax": self.get_parm("xmax"),
                "ymin": self.get_parm("ymin"),
                "ymax": self.get_parm("ymax"),
                "xlabel": self.get_parm("xlabel"),
                "ylabel": self.get_parm("ylabel"),
                "title": self.get_parm("title"),
                "begin": self.parm.begin,
                "end": self.parm.end,
                "dt": self.parm.dt,
                "x_precision": self.parm.x_precision,
                "y_precision": self.parm.y_precision,
            }
            line = LineMatplotlib(**kwargs)
            line.final(self.parm.output, self.parm.noshow)



"""
- xvg_compare
- xvg_ave
- xvg_mvave
- xvg2csv
- xvg_rama
- xvg_show_distribution
- xvg_show_stack
- xvg_show_scatter
- xvg_energy_compute
- xvg_combine
- xvg_ave_bar
- xvg_box
- xvg_violin
"""


