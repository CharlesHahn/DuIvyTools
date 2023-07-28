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
from Visualizor.Visualizer_plotext import LinePlotext 
from Visualizor.Visualizer_plotly import LinePlotly 
from Visualizor.Visualizer_gnuplot import LineGnuplot 
from utils import Parameters


class xvg_show(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  ## write process code

        self.info("in xvgSHOW")
        print(self.parm.__dict__)

        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        for xvgfile in self.parm.input:
            xvg = XVG(xvgfile)
            self.file = xvg
            xdata = [x*self.parm.xshrink for x in xvg.data_columns[0][begin:end:dt]]
            data_list = []
            for data in xvg.data_columns[1:]:
                data_list.append([y*self.parm.yshrink for y in data[begin:end:dt]])

            kwargs = {
                "data_list": data_list,
                "xdata": xdata,
                "legends": self.sel_parm(self.parm.legends, xvg.data_heads[1:]),
                "xmin": self.get_parm("xmin"),
                "xmax": self.get_parm("xmax"),
                "ymin": self.get_parm("ymin"),
                "ymax": self.get_parm("ymax"),
                "xlabel": self.get_parm("xlabel"),
                "ylabel": self.get_parm("ylabel"),
                "title": self.get_parm("title"),
                "x_precision": self.parm.x_precision,
                "y_precision": self.parm.y_precision,
            }
            if self.parm.engine == "matplotlib":
                line = LineMatplotlib(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            elif self.parm.engine == "plotly":
                line = LinePlotly(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            elif self.parm.engine == "plotext":
                line = LinePlotext(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            elif self.parm.engine == "gnuplot":
                kwargs["output"] = self.parm.output
                line = LineGnuplot(**kwargs)
                line.final()
            else:
                pass


class xvg_compare(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvgCompare")
        print(self.parm.__dict__)


class xvg_ave(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_ave")
        print(self.parm.__dict__)

class xvg_mvave(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_mvave")
        print(self.parm.__dict__)


class xvg2csv(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg2csv")
        print(self.parm.__dict__)


class xvg_rama(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_rama")
        print(self.parm.__dict__)


class xvg_show_distribution(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_show_distribution")
        print(self.parm.__dict__)


class xvg_show_stack(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_show_stack")
        print(self.parm.__dict__)


class xvg_show_scatter(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_show_scatter")
        print(self.parm.__dict__)


class xvg_energy_compute(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_energy_compute")
        print(self.parm.__dict__)


class xvg_combine(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_combine")
        print(self.parm.__dict__)


class xvg_ave_bar(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_ave_bar")
        print(self.parm.__dict__)


class xvg_box(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_box")
        print(self.parm.__dict__)


class xvg_violin(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self): 
        self.info("in xvg_biolin")
        print(self.parm.__dict__)


