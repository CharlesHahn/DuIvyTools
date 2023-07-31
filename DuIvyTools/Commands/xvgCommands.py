"""
xvgCommander module is part of DuIvyTools providing basic commands.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

from Commands.Commands import Command
from FileParser.xvgParser import XVG
from Visualizor.Visualizer_matplotlib import LineMatplotlib
from Visualizor.Visualizer_plotext import LinePlotext
from Visualizor.Visualizer_plotly import LinePlotly
from Visualizor.Visualizer_gnuplot import LineGnuplot
from utils import Parameters


class xvg_show(Command):
    """a command class to show xvg data file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  ## write process code
        self.info("in xvgSHOW")
        print(self.parm.__dict__)

        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        for xvgfile in self.parm.input:
            xvg = XVG(xvgfile)
            self.file = xvg
            xdata = [x * self.parm.xshrink for x in xvg.data_columns[0][begin:end:dt]]
            data_list = []
            for c in range(len(xvg.data_heads[1:])): # to avoid str list
                data_list.append([y * self.parm.yshrink for y in xvg.data_columns[c+1][begin:end:dt]])
            self.remove_latex()

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
                "highs": list(),
                "lows": list(),
                "alpha": self.parm.alpha,
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
                line = LineGnuplot(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            else:
                self.error("wrong selection of plot engine")


class xvg_compare(Command):
    """a command class for compare xvg file data"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvgCompare")
        print(self.parm.__dict__)

        ## check and convert parm
        for xvg in self.parm.input:
            if not isinstance(xvg, str):
                self.error("files should be seperated by space not ,")
        for indexs in self.parm.columns:
            if isinstance(indexs, list):
                break
        else:
            self.parm.columns = [[cs] for cs in self.parm.columns]
        if len(self.parm.input) != len(self.parm.columns):
            self.error(f"columns must contain {len(self.parm.input)} list")
        if self.parm.legends != None and len(self.parm.legends) != sum(
            [len(c) for c in self.parm.columns]
        ):
            self.error("number of legends you input can not pair to columns you select")
        if self.parm.title == None:
            self.parm.title = "XVG Comparison"

        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        xvgs = [XVG(xvg) for xvg in self.parm.input]
        self.file = xvgs[0]
        xdata = [x * self.parm.xshrink for x in self.file.data_columns[0][begin:end:dt]]
        legends, data_list, highs_list, lows_list = [], [], [], []
        for id, column_indexs in enumerate(self.parm.columns):
            xvg = xvgs[id]
            for column_index in column_indexs:
                if column_index >= xvg.column_num:
                    self.error(
                        f"invalid column index {column_index} which >= column number {xvg.column_num}"
                    )
                if self.parm.showMV:
                    aves, highs, lows = xvg.calc_mvave(
                        self.parm.windowsize, self.parm.confidence, column_index
                    )
                    highs_list.append(
                        [y * self.parm.yshrink for y in highs[begin:end:dt]]
                    )
                    lows_list.append(
                        [y * self.parm.yshrink for y in lows[begin:end:dt]]
                    )
                else:
                    aves = xvg.data_columns[column_index]
                data_list.append([y * self.parm.yshrink for y in aves[begin:end:dt]])
                legend = xvg.data_heads[column_index]
                legends.append(f"{legend} - {xvg.xvgfile}")
        self.remove_latex()
        legends = self.remove_latex_msgs(legends)

        kwargs = {
            "data_list": data_list,
            "xdata": xdata,
            "legends": self.sel_parm(self.parm.legends, legends),
            "xmin": self.get_parm("xmin"),
            "xmax": self.get_parm("xmax"),
            "ymin": self.get_parm("ymin"),
            "ymax": self.get_parm("ymax"),
            "xlabel": self.get_parm("xlabel"),
            "ylabel": self.get_parm("ylabel"),
            "title": self.get_parm("title"),
            "x_precision": self.parm.x_precision,
            "y_precision": self.parm.y_precision,
            "highs": highs_list,
            "lows": lows_list,
            "alpha": self.parm.alpha,
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
            line = LineGnuplot(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        else:
            self.error("wrong selection of plot engine")
        
        if self.parm.csv:
            self.parm.csv = self.check_output_exist(self.parm.csv)
            self.dump2csv(kwargs)

    def dump2csv(self, kwargs):
        ## merge xvg2csv and xvg_mvave functions here 
        if self.parm.showMV:
            with open(self.parm.csv, 'w') as fo:
                fo.write(f"""{kwargs["xlabel"].strip("$")}""")
                for leg in kwargs["legends"]:
                    leg = leg.strip("$")
                    fo.write(f""",mvave_{leg},high_{leg},low_{leg}""")
                fo.write("\n")
                for r in range(len(kwargs["xdata"])):
                    fo.write(f"""{kwargs["xdata"][r]:.8f}""")
                    for c in range(len(kwargs["data_list"])):
                        fo.write(f""",{kwargs["data_list"][c][r]:.8f},{kwargs["highs"][c][r]:.8f},{kwargs["lows"][c][r]:.8f}""")
                    fo.write("\n")
        else:
            with open(self.parm.csv, "w") as fo:
                fo.write(f"""{kwargs["xlabel"].strip("$")}""")
                for leg in kwargs["legends"]:
                    fo.write(f""",{leg.strip("$")}""")
                fo.write("\n")
                for r in range(len(kwargs["xdata"])):
                    fo.write(f"""{kwargs["xdata"][r]:.8f}""")
                    for c in range(len(kwargs["data_list"])):
                        fo.write(f""",{kwargs["data_list"][c][r]:.8f}""")
                    fo.write("\n")
        self.info(f"data has been dumped to {self.parm.csv} successfully")


class xvg_ave(Command):
    """compute averages of all data columns of specified xvg files
    """
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_ave")
        print(self.parm.__dict__)

        outstr:str = ""
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        for xvgfile in self.parm.input:
            xvg = XVG(xvgfile)
            self.file = xvg
            legends, aves, stderrs = [], [], []
            for c in range(len(xvg.data_heads)):
                legend, ave, stderr = xvg.calc_ave(begin, end, dt, c)
                legends.append(legend)
                aves.append(ave)
                stderrs.append(stderr)
            outstr += f"\n>>>>>>>>>>>>>> {xvg.xvgfile:^30} <<<<<<<<<<<<<<\n"
            outstr += "-"*60 + "\n"
            outstr += "|"+" "*18+"|      Average      |      Std.Err      |\n"
            outstr += "-"*60 + "\n"
            for l, a, s in zip(legends, aves, stderrs):
                outstr += f"|{l:^18}|{a:^19.6f}|{s:^19.6f}|\n"
                outstr += "-"*60 + "\n"
        print(outstr)
        if self.parm.output:
            outfile = self.check_output_exist(self.parm.output)
            with open(outfile, 'w') as fo:
                fo.write(outstr)
            self.info(f"all average data have been saved to {outfile}")


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
