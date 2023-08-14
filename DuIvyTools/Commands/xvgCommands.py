"""
xvgCommander module is part of DuIvyTools providing basic commands.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Tuple, Union

import numpy as np

from Commands.Commands import Command
from FileParser.xvgParser import XVG
from Visualizor.Visualizer_matplotlib import *
from Visualizor.Visualizer_plotext import *
from Visualizor.Visualizer_plotly import *
from Visualizor.Visualizer_gnuplot import *
from utils import Parameters


class xvg_show(Command):
    """a command class to show xvg data file"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):  ## write process code
        self.info("in xvgSHOW")
        print(self.parm.__dict__)

        if not self.parm.input:
            self.error("you must specify the xvg files to show")
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        for xvgfile in self.parm.input:
            xvg = XVG(xvgfile)
            self.file = xvg
            xdata, data_list = [], []
            for c in range(len(xvg.data_heads[1:])):  # to avoid str list
                data_list.append(
                    [
                        y * self.parm.yshrink
                        for y in xvg.data_columns[c + 1][begin:end:dt]
                    ]
                )
                xdata.append(
                    [x * self.parm.xshrink for x in xvg.data_columns[0][begin:end:dt]]
                )
            self.remove_latex()

            kwargs = {
                "data_list": data_list,
                "xdata_list": xdata,
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
                "alpha": self.sel_parm(self.parm.alpha, 0.4),
                "legend_location": self.sel_parm(self.parm.legend_location, "inside"),
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

    def check_parm(self) -> None:
        ## check and convert parm
        if not self.parm.input:
            self.error("you must specify the xvg files to compare")
        if not self.parm.columns:
            self.error("you must specify the columns to select")
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

    def __call__(self):
        self.info("in xvgCompare")
        print(self.parm.__dict__)

        self.check_parm()
        if self.parm.title == None:
            self.parm.title = "XVG Comparison"

        ## draw data relative to its original xdata
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        xvgs = [XVG(xvg) for xvg in self.parm.input]
        self.file = xvgs[0]
        legends, xdata, data_list, highs_list, lows_list = [], [], [], [], []
        for id, column_indexs in enumerate(self.parm.columns):
            xvg = xvgs[id]
            for column_index in column_indexs:
                xvg.check_column_index(column_index)
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
                xdata.append(
                    [x * self.parm.xshrink for x in xvg.data_columns[0][begin:end:dt]]
                )
                legend = xvg.data_heads[column_index]
                legends.append(f"{legend} - {xvg.xvgfile}")
        self.remove_latex()
        legends = self.remove_latex_msgs(legends)

        kwargs = {
            "data_list": data_list,
            "xdata_list": xdata,
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
            "alpha": self.sel_parm(self.parm.alpha, 0.4),
            "legend_location": self.sel_parm(self.parm.legend_location, "inside"),
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
            if len(self.parm.input) == 1:
                self.dump2csv_1_input(kwargs)
            else:
                self.dump2csv(kwargs)

    def dump2csv_1_input(self, kwargs):
        ## merge xvg2csv and xvg_mvave functions here
        if self.parm.showMV:
            with open(self.parm.csv, "w") as fo:
                fo.write(f"""{kwargs["xlabel"].strip("$")}""")
                for leg in kwargs["legends"]:
                    leg = leg.strip("$")
                    fo.write(f""",mvave_{leg},high_{leg},low_{leg}""")
                fo.write("\n")
                for r in range(len(kwargs["xdata_list"][0])):
                    fo.write(f"""{kwargs["xdata_list"][0][r]:.8f}""")
                    for c in range(len(kwargs["data_list"])):
                        fo.write(
                            f""",{kwargs["data_list"][c][r]:.8f},{kwargs["highs"][c][r]:.8f},{kwargs["lows"][c][r]:.8f}"""
                        )
                    fo.write("\n")
        else:
            with open(self.parm.csv, "w") as fo:
                fo.write(f"""{kwargs["xlabel"].strip("$")}""")
                for leg in kwargs["legends"]:
                    fo.write(f""",{leg.strip("$")}""")
                fo.write("\n")
                for r in range(len(kwargs["xdata_list"][0])):
                    fo.write(f"""{kwargs["xdata_list"][0][r]:.8f}""")
                    for c in range(len(kwargs["data_list"])):
                        fo.write(f""",{kwargs["data_list"][c][r]:.8f}""")
                    fo.write("\n")
        self.info(f"data has been dumped to {self.parm.csv} successfully")

    def dump2csv(self, kwargs):
        ## merge xvg2csv and xvg_mvave functions here
        if self.parm.showMV:
            with open(self.parm.csv, "w") as fo:
                for leg in kwargs["legends"]:
                    fo.write(f"""{kwargs["xlabel"].strip("$")},""")
                    leg = leg.strip("$")
                    fo.write(f"""mvave_{leg},high_{leg},low_{leg},""")
                fo.write("\n")
                for r in range(len(kwargs["data_list"][0])):
                    for c in range(len(kwargs["data_list"])):
                        fo.write(f"""{kwargs["xdata_list"][c][r]:.8f},""")
                        fo.write(
                            f"""{kwargs["data_list"][c][r]:.8f},{kwargs["highs"][c][r]:.8f},{kwargs["lows"][c][r]:.8f},"""
                        )
                    fo.write("\n")
        else:
            with open(self.parm.csv, "w") as fo:
                for leg in kwargs["legends"]:
                    fo.write(f"""{kwargs["xlabel"].strip("$")},""")
                    fo.write(f"""{leg.strip("$")},""")
                fo.write("\n")
                for r in range(len(kwargs["data_list"][0])):
                    for c in range(len(kwargs["data_list"])):
                        fo.write(f"""{kwargs["xdata_list"][0][r]:.8f},""")
                        fo.write(f"""{kwargs["data_list"][c][r]:.8f},""")
                    fo.write("\n")
        self.info(f"data has been dumped to {self.parm.csv} successfully")


class xvg_ave(Command):
    """compute averages of all data columns of specified xvg files"""

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_ave")
        print(self.parm.__dict__)

        outstr: str = ""
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
            outstr += f"\n>>>>>>>>>>>>>> {xvg.xvgfile:^40} <<<<<<<<<<<<<<\n"
            outstr += "-" * 70 + "\n"
            outstr += "|" + " " * 28 + "|      Average      |      Std.Err      |\n"
            outstr += "-" * 60 + "\n"
            for l, a, s in zip(legends, aves, stderrs):
                outstr += f"|{l:^28}|{a:^19.6f}|{s:^19.6f}|\n"
                outstr += "-" * 70 + "\n"
        print(outstr)
        if self.parm.output:
            outfile = self.check_output_exist(self.parm.output)
            with open(outfile, "w") as fo:
                fo.write(outstr)
            self.info(f"all average data have been saved to {outfile}")


class xvg_energy_compute(Command):
    """
    compute the interaction between protein and ligand by:
        binding energy  = prolig energy - pro energy - lig energy

    :parameters::
        xvgfiles: a list contains three xvg files
            prolig_xvg: energy xvg file of prolig
            pro_xvg: energy xvg file of protein
            lig_xvg: energy xvg file of ligand
        outfile: the output xvg file name

    IMPORTANT:
        the xvg file used here should contain and ONLY contain five columns:
        Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip.
    """

    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_energy_compute")
        print(self.parm.__dict__)

        ## check parameters
        if len(self.parm.input) != 3:
            self.error(
                "wrong number of input xvg files, must be prolig.xvg, pro.xvg and lig.xvg by order"
            )
        prolig_xvg = self.parm.input[0]
        pro_xvg = self.parm.input[1]
        lig_xvg = self.parm.input[2]
        if not self.parm.output:
            self.error("please specify output xvg file name")
        self.parm.output = self.check_output_exist(self.parm.output)

        prolig, pro, lig = XVG(prolig_xvg), XVG(pro_xvg), XVG(lig_xvg)
        if not (prolig.data_heads == pro.data_heads == lig.data_heads) or (
            len(prolig.data_heads) != 5
        ):
            self.error(
                "three xvg files should contain same number (5) of columns, "
                + "and the order should be: \n"
                + "    Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip. "
            )
        if not (
            ("Time" in prolig.data_heads[0])
            and ("LJ" in prolig.data_heads[1])
            and ("Disper" in prolig.data_heads[2])
            and ("Coulomb" in prolig.data_heads[3])
            and ("recip" in prolig.data_heads[4])
        ):
            self.error(
                "the legend order should be: \n"
                + "    Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip. "
            )
        if not (prolig.row_num == pro.row_num == lig.row_num):
            self.error("{}, {}, {} should contain same number of rows.")
        if not (prolig.data_columns[0] == pro.data_columns[0] == lig.data_columns[0]):
            self.error("the Time axis may not be the same, check the interval of time.")

        ## compute the bingding energy
        ## time
        out_data = [prolig.data_columns[0]] + [[] for _ in range(9)]
        out_heads = (
            [prolig.data_heads[0]]
            + [head for head in prolig.legends]
            + [
                "LJ(all)",
                "Coulomb(all)",
                "Short-Range(all)",
                "Long-Range(all)",
                "Total Energy",
            ]
        )
        ## LJ(SR)
        out_data[1] = [
            prolig.data_columns[1][row]
            - pro.data_columns[1][row]
            - lig.data_columns[1][row]
            for row in range(prolig.row_num)
        ]
        ## Disper.corr.
        out_data[2] = [
            prolig.data_columns[2][row]
            - pro.data_columns[2][row]
            - lig.data_columns[2][row]
            for row in range(prolig.row_num)
        ]
        ## Coulomb(SR)
        out_data[3] = [
            prolig.data_columns[3][row]
            - pro.data_columns[3][row]
            - lig.data_columns[3][row]
            for row in range(prolig.row_num)
        ]
        ## Coul.recip.
        out_data[4] = [
            prolig.data_columns[4][row]
            - pro.data_columns[4][row]
            - lig.data_columns[4][row]
            for row in range(prolig.row_num)
        ]
        for row in range(prolig.row_num):
            ## LJ(all)
            out_data[5].append(out_data[1][row] + out_data[2][row])
            ## Coulomb(all)
            out_data[6].append(out_data[3][row] + out_data[4][row])
            ## Short-Range(all)
            out_data[7].append(out_data[1][row] + out_data[3][row])
            ## Long-Range(all)
            out_data[8].append(out_data[2][row] + out_data[4][row])
            ## Total Energy
            out_data[9].append(out_data[5][row] + out_data[6][row])

        ## write energy computation results
        xvg = XVG(self.parm.output, is_file=False, new_file=True)
        xvg.title = prolig.title
        xvg.comments += "# this file was created by XVG.energy_compute through: \n"
        xvg.comments += (
            "#    binding = prolig energy - protein energy - ligand energy\n"
        )
        xvg.comments += (
            f"#    {self.parm.output} = {prolig_xvg} - {pro_xvg} - {lig_xvg}\n"
        )
        xvg.xlabel = out_heads[0]
        xvg.ylabel = "(kJ/mol)"
        xvg.legends = out_heads[1:]
        xvg.data_columns = out_data
        xvg.column_num = 10
        xvg.row_num = prolig.row_num
        xvg.data_heads = out_heads
        xvg.dump2xvg(self.parm.output)
        self.info(
            f"energy computation through {prolig_xvg}, {pro_xvg} and {lig_xvg} sucessfully"
        )


class xvg_combine(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_combine")
        print(self.parm.__dict__)

        ## check parm
        if not self.parm.output:
            self.error("please specify output xvg file name")
        self.parm.output = self.check_output_exist(self.parm.output)

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
        if (
            self.parm.legends != None
            and len(self.parm.legends) != sum([len(c) for c in self.parm.columns]) - 1
        ):
            self.error("number of legends you input can not pair to columns you select")

        # process xvg combination
        out_xvg = XVG(self.parm.output, is_file=False, new_file=True)
        title_list: str = []
        out_xvg.comments += "# this file was created by combination of:\n"
        xvgs = [XVG(xvg) for xvg in self.parm.input]
        for id, column_indexs in enumerate(self.parm.columns):
            xvg = xvgs[id]
            if xvg.title not in title_list:
                title_list.append(xvg.title)
            out_xvg.comments += f"# file {xvg.xvgfile}; indexs: {str(column_indexs)};\n"
            for column_index in column_indexs:
                xvg.check_column_index(column_index)
                out_xvg.data_heads.append(xvg.data_heads[column_index])
                out_xvg.data_columns.append(xvg.data_columns[column_index])
        if self.parm.title:
            out_xvg.title = self.parm.title
        else:
            out_xvg.title = " & ".join(title_list)
        if self.parm.xlabel:
            out_xvg.xlabel = self.parm.xlabel
        if self.parm.ylabel:
            out_xvg.ylabel = self.parm.ylabel
        if self.parm.legends:
            out_xvg.legends = self.parm.legends
        out_xvg.dump2xvg(self.parm.output)
        self.info("xvg files combined successfully")


class xvg_show_distribution(xvg_compare):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_show_distribution")
        print(self.parm.__dict__)

        ## TODO: fill the curve to zero, KDE density map
        self.check_parm()
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        xvgs = [XVG(xvg) for xvg in self.parm.input]
        self.file = xvgs[0]
        legends, xdata_list, data_list = [], [], []
        for id, column_indexs in enumerate(self.parm.columns):
            xvg = xvgs[id]
            for column_index in column_indexs:
                xvg.check_column_index(column_index)
                data = xvg.data_columns[column_index][begin:end:dt]
                if len(data) == 0:
                    self.error("wrong selection of begin, end, or dt, no data selected")
                xdata, data = self.calc_distribution(data, self.parm.bin)
                data_list.append(data)
                xdata_list.append(xdata)
                legend = xvg.data_heads[column_index]
                legends.append(f"{legend} - {xvg.xvgfile}")
        self.remove_latex()
        legends = self.remove_latex_msgs(legends)

        kwargs = {
            "data_list": data_list,
            "xdata_list": xdata_list,
            "legends": self.sel_parm(self.parm.legends, legends),
            "xmin": self.sel_parm(self.parm.xmin, None),
            "xmax": self.sel_parm(self.parm.xmax, None),
            "ymin": self.sel_parm(self.parm.ymin, None),
            "ymax": self.sel_parm(self.parm.ymax, None),
            "xlabel": self.sel_parm(self.parm.xlabel, "Distribution"),
            "ylabel": self.sel_parm(self.parm.ylabel, "Frequency %"),
            "title": self.sel_parm(self.parm.title, "XVG Distribution"),
            "x_precision": self.parm.x_precision,
            "y_precision": self.parm.y_precision,
            "highs": list(),
            "lows": list(),
            "alpha": self.sel_parm(self.parm.alpha, 0.4),
            "legend_location": self.sel_parm(self.parm.legend_location, "inside"),
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
        with open(self.parm.csv, "w") as fo:
            for leg in kwargs["legends"]:
                fo.write(
                    f"""Distribution_of_{leg.strip("$")},Frequency(%)_of_{leg.strip("$")},"""
                )
            fo.write("\n")
            for r in range(self.parm.bin):
                for c in range(len(kwargs["data_list"])):
                    fo.write(f"""{kwargs["xdata"][c][r]:.8f},""")
                    fo.write(f"""{kwargs["data_list"][c][r]:.8f},""")
                fo.write("\n")
        self.info(f"data has been dumped to {self.parm.csv} successfully")

    def calc_distribution(
        self, data: List[float], bin: int
    ) -> Tuple[List[float], List[float]]:
        """calculate the distribution of data

        Args:
            data (List[float]): data
            bin (int): bin number

        Returns:
            xdata (List[float]): xdata
            data (List[float]): distribution data
        """
        min, max = np.min(data), np.max(data)
        bin_window = (max - min) / bin
        if bin_window != 0:
            frequency = [0 for _ in range(bin)]
            for value in data:
                index = int((value - min) / bin_window)
                if index == bin:
                    index = bin - 1
                frequency[index] += 1
            if sum(frequency) != len(data):
                self.error("wrong in calculating distribution")
            frequency = [f * 100.0 / len(data) for f in frequency]
            x_value = [min + bin_window * b for b in range(bin)]
        else:
            frequency = [1]
            x_value = [min]
        return x_value, frequency


class xvg_show_scatter(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_show_scatter")
        print(self.parm.__dict__)

        ## check and convert parm
        if not self.parm.input:
            self.error("you must specify the xvg files to show")
        if not self.parm.columns:
            self.error("you must specify the columns to select")
        for xvg in self.parm.input:
            if not isinstance(xvg, str):
                self.error("files should be seperated by space not ,")
        for indexs in self.parm.columns:
            if not isinstance(indexs, list) or len(indexs) not in [2, 3]:
                self.error(
                    "for each file, you must specify 2 or 3 (as color) columns to draw scatter plot"
                )
        if len(self.parm.input) != len(self.parm.columns):
            self.error(f"columns must contain {len(self.parm.input)} list")
        if self.parm.legends != None and len(self.parm.legends) != len(self.parm.input):
            self.error(
                "for scatter plot, the number of legends must pair to the number of files"
            )

        # TODO: scatter density map
        # deal with data
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        xvgs = [XVG(xvg) for xvg in self.parm.input]
        self.file = xvgs[0]
        legends, xdata_list, data_list, color_list = [], [], [], []
        color_head, xlabel, ylabel = None, None, None
        for id, column_indexs in enumerate(self.parm.columns):
            xvg = xvgs[id]
            xvg.check_column_index(column_indexs)
            xdata_list.append(
                [
                    x * self.parm.xshrink
                    for x in xvg.data_columns[column_indexs[0]][begin:end:dt]
                ]
            )
            xlabel = xvg.data_heads[column_indexs[0]]
            data_list.append(
                [
                    y * self.parm.yshrink
                    for y in xvg.data_columns[column_indexs[1]][begin:end:dt]
                ]
            )
            ylabel = xvg.data_heads[column_indexs[1]]
            if len(column_indexs) == 3:
                color_list.append(
                    [
                        z * self.parm.zshrink
                        for z in xvg.data_columns[column_indexs[2]][begin:end:dt]
                    ]
                )
                color_head = xvg.data_heads[column_indexs[2]]
            else:
                color_list.append([1 for x in data_list[-1]])
            legends.append(xvg.xvgfile)
        legends = self.remove_latex_msgs(legends)
        xlabel = self.remove_latex_msgs([xlabel])[0]
        ylabel = self.remove_latex_msgs([ylabel])[0]
        if color_head:
            color_head = self.remove_latex_msgs([color_head])[0]

        kwargs = {
            "data_list": data_list,
            "xdata_list": xdata_list,
            "color_list": color_list,
            "legends": self.sel_parm(self.parm.legends, legends),
            "xmin": self.get_parm("xmin"),
            "xmax": self.get_parm("xmax"),
            "ymin": self.get_parm("ymin"),
            "ymax": self.get_parm("ymax"),
            "zmin": self.get_parm("zmin"),
            "zmax": self.get_parm("zmax"),
            "xlabel": self.sel_parm(self.parm.xlabel, xlabel),
            "ylabel": self.sel_parm(self.parm.ylabel, ylabel),
            "title": self.sel_parm(self.parm.title, self.file.title),
            "zlabel": self.sel_parm(self.parm.zlabel, color_head),
            "cmap": self.sel_parm(self.parm.colormap, None),
            "x_precision": self.parm.x_precision,
            "y_precision": self.parm.y_precision,
            "z_precision": self.parm.z_precision,
            "colorbar_location": self.parm.colorbar_location,
            "legend_location": self.sel_parm(self.parm.legend_location, "inside"),
        }
        if self.parm.engine == "matplotlib":
            line = ScatterMatplotlib(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "plotly":
            line = ScatterPlotly(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "plotext":
            line = ScatterPlotext(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "gnuplot":
            line = ScatterGnuplot(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        else:
            self.error("wrong selection of plot engine")


class xvg_show_stack(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_show_stack")
        print(self.parm.__dict__)

        ## check and convert parm
        if not self.parm.input:
            self.error("you must specify the xvg files to show")
        if not self.parm.columns:
            self.error("you must specify the columns to select")
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
        if self.parm.legends != None:
            for id, column_indexs in enumerate(self.parm.columns):
                if len(self.parm.legends) != len(column_indexs):
                    self.error(
                        f"number of legends you input can not pair to columns {column_indexs} you select"
                    )

        # deal with data
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        xvgs = [XVG(xvg) for xvg in self.parm.input]
        for id, column_indexs in enumerate(self.parm.columns):
            self.file = xvgs[id]
            column_indexs.reverse()  # First in, show at bottom
            if self.parm.legends:
                self.parm.legends.reverse()  # reverse as the column_indexs
            self.file.check_column_index(column_indexs)
            legends, xdata_list, data_list = [], [], []
            highs_list, lows_list = [], []
            for i in range(len(column_indexs)):
                legends.append(self.file.data_heads[column_indexs[i]])
                xdata_list.append(
                    [
                        x * self.parm.xshrink
                        for x in self.file.data_columns[0][begin:end:dt]
                    ]
                )
                data_list.append(
                    [
                        y * self.parm.yshrink
                        for y in self.file.data_columns[column_indexs[i]][begin:end:dt]
                    ]
                )
                data = []
                for r in range(self.file.row_num):
                    data.append(
                        sum(
                            [
                                self.file.data_columns[column_indexs[c]][r]
                                for c in range(i, len(column_indexs))
                            ]
                        )
                    )
                highs_list.append([y * self.parm.yshrink for y in data[begin:end:dt]])
                lows_list.append([0 for _ in range(len(data_list[0]))])
            legends = self.remove_latex_msgs(legends)
            title = f"{self.file.title} of {self.file.xvgfile}"
            title = self.remove_latex_msgs([title])[0]
            xmin = np.min(xdata_list[0])
            xmax = np.max(xdata_list[0])
            ymin = 0
            ymax = np.max(highs_list[0])

            kwargs = {
                "data_list": data_list,
                "xdata_list": xdata_list,
                "legends": self.sel_parm(self.parm.legends, legends),
                "xmin": self.sel_parm(self.parm.xmin, xmin),
                "xmax": self.sel_parm(self.parm.xmax, xmax),
                "ymin": self.sel_parm(self.parm.ymin, ymin),
                "ymax": self.sel_parm(self.parm.ymax, ymax),
                "xlabel": self.get_parm("xlabel"),
                "ylabel": self.get_parm("ylabel"),
                "title": self.sel_parm(self.parm.title, title),
                "x_precision": self.parm.x_precision,
                "y_precision": self.parm.y_precision,
                "highs": highs_list,
                "lows": lows_list,
                "alpha": self.sel_parm(self.parm.alpha, 1.0),
                "legend_location": self.sel_parm(self.parm.legend_location, "inside"),
            }
            if self.parm.engine == "matplotlib":
                line = StackMatplotlib(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            elif self.parm.engine == "plotly":
                line = StackPlotly(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            elif self.parm.engine == "plotext":
                kwargs["data_list"] = highs_list
                line = LinePlotext(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            elif self.parm.engine == "gnuplot":
                line = StackGnuplot(**kwargs)
                line.final(self.parm.output, self.parm.noshow)
            else:
                self.error("wrong selection of plot engine")


class xvg_box_compare(xvg_compare):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_box")
        print(self.parm.__dict__)

        self.check_parm()
        ## draw data relative to its original xdata
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        xvgs = [XVG(xvg) for xvg in self.parm.input]
        self.file = xvgs[0]
        legends, color_list, data_list = [], [], []
        for id, column_indexs in enumerate(self.parm.columns):
            xvg = xvgs[id]
            for column_index in column_indexs:
                xvg.check_column_index(column_index)
                data_list.append(
                    [
                        y * self.parm.yshrink
                        for y in xvg.data_columns[column_index][begin:end:dt]
                    ]
                )
                color_list.append(
                    [x * self.parm.zshrink for x in xvg.data_columns[0][begin:end:dt]]
                )  # zshrink for third data
                zlabel = xvg.data_heads[0]
                legend = xvg.data_heads[column_index]
                legends.append(f"{legend} - {xvg.xvgfile}")
        self.remove_latex()
        legends = self.remove_latex_msgs(legends)
        if self.parm.mode != "withoutScatter":
            self.info(
                "the scatter dots will be colored by the first column data of corresponding file"
            )

        kwargs = {
            "data_list": data_list,
            "color_list": color_list,
            "legends": self.sel_parm(self.parm.legends, legends),
            "xmin": self.parm.xmin,
            "xmax": self.parm.xmax,
            "ymin": self.parm.ymin,
            "ymax": self.parm.ymax,
            "xlabel": self.parm.xlabel,
            "ylabel": self.get_parm("ylabel"),
            "zlabel": self.sel_parm(self.parm.zlabel, zlabel),
            "title": self.sel_parm(self.parm.title, "XVG box comparison"),
            "x_precision": self.parm.x_precision,
            "y_precision": self.parm.y_precision,
            "z_precision": self.parm.z_precision,
            "alpha": self.sel_parm(self.parm.alpha, 0.4),
            "mode": self.parm.mode,
            "cmap": self.sel_parm(self.parm.colormap, None),
            "colorbar_location": self.parm.colorbar_location,
        }
        if self.parm.engine == "matplotlib":
            line = BoxMatplotlib(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "plotly":
            line = BoxPlotly(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "plotext":
            self.error("Plotext engine do not support box plot now.")
        elif self.parm.engine == "gnuplot":
            line = BoxGnuplot(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        else:
            self.error("wrong selection of plot engine")


class xvg_ave_bar(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_ave_bar")
        print(self.parm.__dict__)

        ## check and convert parm
        if not self.parm.input:
            self.error("you must specify the xvg files to show")
        if not self.parm.columns:
            self.error("you must specify the columns to select")
        for xvgs in self.parm.input:
            if isinstance(xvgs, list):
                break
        else:
            self.parm.input = [[xvg] for xvg in self.parm.input]
        for columns in self.parm.columns:
            if not isinstance(columns, int):
                self.error("the item of column_select must be int, do not use ,")
        if self.parm.legends != None and len(self.parm.legends) != len(self.parm.input):
            self.error(
                f"number of legends ({len(self.parm.legends)}) you input can not pair to the number of file groups ({len(self.parm.input)})"
            )
        if self.parm.additional_list != None and len(self.parm.additional_list) != len(
            self.parm.columns
        ):
            self.error(
                f"the number of xtitles ({len(self.parm.additional_list)}) you specified through 'additional_list' must pair to the number of columns {len(self.parm.columns)}"
            )

        ## deal with data
        begin, end, dt = self.parm.begin, self.parm.end, self.parm.dt
        final_aves, final_stds = [], []
        all_out = "\n" + ">" * 26 + "  detailed data  " + "<" * 26 + "\n"
        all_out += "XVGFILE                 , LEGEND                  ,   AVERAGE   ,   STD.ERR\n"
        xtitles, legends = ["" for _ in self.parm.columns], []
        for xvgfiles in self.parm.input:
            legends.append(xvgfiles[0])
            column_averages_matrix = [[] for _ in self.parm.columns]
            for xvgfile in xvgfiles:
                xvg = XVG(xvgfile)
                xvg.check_column_index(self.parm.columns)
                for i, c in enumerate(self.parm.columns):
                    head, ave, std = xvg.calc_ave(begin, end, dt, c)
                    all_out += (
                        f"{xvgfile:<24}, {head:<24}, {ave:^12.6f}, {std:^12.6f}\n"
                    )
                    xtitles[i] = head
                    column_averages_matrix[i].append(ave)
            column_aves, column_stds = [], []
            for lis in column_averages_matrix:
                column_aves.append(np.average(lis))
                column_stds.append(np.std(lis, ddof=1))
            final_aves.append(column_aves)
            final_stds.append(column_stds)

        xtitles = self.remove_latex_msgs(xtitles)
        legends = self.remove_latex_msgs(legends)
        xtitles = self.sel_parm(self.parm.additional_list, xtitles)
        legends = self.sel_parm(self.parm.legends, legends)

        # print averages
        print(all_out)
        outstr = "\n" + ">" * 28 + "  final data  " + "<" * 28
        outstr += "\n" + "-" * 70 + "\n"
        outstr += (
            "| Average "
            + " " * 20
            + "|"
            + "|".join(f"{t:^19}" for t in xtitles)
            + "|\n"
        )
        for i in range(len(final_aves)):
            outstr += f"|{legends[i]:<28} |"
            outstr += "|".join([f"{ave:^19.6}" for ave in final_aves[i]])
            outstr += "|\n"
        outstr += "-" * 70 + "\n"
        outstr += (
            "| std.err "
            + " " * 20
            + "|"
            + "|".join(f"{t:^19}" for t in xtitles)
            + "|\n"
        )
        for i in range(len(final_stds)):
            outstr += f"|{legends[i]:<28} |"
            outstr += "|".join([f"{std:^19.6}" for std in final_stds[i]])
            outstr += "|\n"
        outstr += "-" * 70 + "\n"
        print(outstr)

        if self.parm.csv:
            self.parm.csv = self.check_output_exist(self.parm.csv)
            with open(self.parm.csv, "w") as fo:
                fo.write(",".join(["Average"] + xtitles) + "\n")
                for i in range(len(final_aves)):
                    fo.write(legends[i] + ",")
                    fo.write(",".join(["{:.4f}".format(ave) for ave in final_aves[i]]))
                    fo.write("\n")
                fo.write(",".join(["std.err"] + xtitles) + "\n")
                for i in range(len(final_stds)):
                    fo.write(legends[i] + ",")
                    fo.write(",".join(["{:.4f}".format(std) for std in final_stds[i]]))
                    fo.write("\n")

        kwargs = {
            "data_list": final_aves,
            "stds_list": final_stds,
            "xtitles": xtitles,
            "legends": legends,
            "xmin": self.parm.xmin,
            "xmax": self.parm.xmax,
            "ymin": self.parm.ymin,
            "ymax": self.parm.ymax,
            "xlabel": self.parm.xlabel,
            "ylabel": self.parm.ylabel,
            "title": self.sel_parm(self.parm.title, "XVG ave bar comparison"),
            "x_precision": self.parm.x_precision,
            "y_precision": self.parm.y_precision,
            "legend_location": self.sel_parm(self.parm.legend_location, "inside"),
        }
        if self.parm.engine == "matplotlib":
            line = BarMatplotlib(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "plotly":
            line = BarPlotly(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "plotext":
            line = BarPlotext(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        elif self.parm.engine == "gnuplot":
            line = BarGnuplot(**kwargs)
            line.final(self.parm.output, self.parm.noshow)
        else:
            self.error("wrong selection of plot engine")


class xvg_rama(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xvg_rama")
        print(self.parm.__dict__)

        ## check parameters
        if not self.parm.input:
            self.error("you must specify the xvg files to draw")
        for xvg in self.parm.input:
            if not isinstance(xvg, str):
                self.error("files should be seperated by space not ,")
        if len(self.parm.input) > 1:
            self.warn(
                f"only the first file {self.parm.input[0]} you specified will be used to draw ramachandran"
            )

        xvg = XVG(self.parm.input[0])

        ## check column number
        if (
            xvg.column_num != 3
            or len(xvg.data_columns) != 3
            or (xvg.data_heads[0] != "Phi" or xvg.data_heads[1] != "Psi")
        ):
            self.error(
                "Check your input xvg file ! It has to contains 3 columns: Phi, Psi, AA name. And x-label should be Phi and Y-label should be Psi"
            )

        ## draw background
        ## Psi and Phi data are from DOI: 10.1002/prot.10286
        ## reference : pyrama
        rama_preferences = {
            "General": {
                "file": os.path.join("../", "data", "pref_general.data"),
                "cmap": ["#FFFFFF", "#B3E8FF", "#7FD9FF"],
                "bounds": [0, 0.0005, 0.02, 1],
            },
            "GLY": {
                "file": os.path.join("../", "data", "pref_glycine.data"),
                "cmap": ["#FFFFFF", "#FFE8C5", "#FFCC7F"],
                "bounds": [0, 0.002, 0.02, 1],
            },
            "PRO": {
                "file": os.path.join("../", "data", "pref_proline.data"),
                "cmap": ["#FFFFFF", "#D0FFC5", "#7FFF8C"],
                "bounds": [0, 0.002, 0.02, 1],
            },
            "Pre-PRO": {
                "file": os.path.join("../", "data", "pref_preproline.data"),
                "cmap": ["#FFFFFF", "#B3E8FF", "#7FD9FF"],
                "bounds": [0, 0.002, 0.02, 1],
            },
        }

        rama_pref_values = {}
        for key, val in rama_preferences.items():
            data_file_path = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__))
            )
            rama_pref_values[key] = [[0 for _ in range(361)] for _ in range(361)]
            with open(os.path.join(data_file_path, val["file"]), "r") as fn:
                for line in fn:
                    if line.startswith("#"):
                        continue
                    else:
                        phi = int(float(line.split()[0]))
                        psi = int(float(line.split()[1]))
                        ## plt.imshow show transpose of img
                        rama_pref_values[key][psi + 180][phi + 180] = float(
                            line.split()[2]
                        )
                        rama_pref_values[key][psi + 179][phi + 180] = float(
                            line.split()[2]
                        )
                        rama_pref_values[key][psi + 180][phi + 179] = float(
                            line.split()[2]
                        )
                        rama_pref_values[key][psi + 179][phi + 179] = float(
                            line.split()[2]
                        )

        normals, outliers = {}, {}
        for key in rama_preferences.keys():
            normals[key] = {"phi": [], "psi": [], "res": []}
            outliers[key] = {"phi": [], "psi": [], "res": []}
        for row in range(xvg.row_num):
            if row < xvg.row_num - 1 and "PRO" in xvg.data_columns[2][row + 1]:
                AA_type = "Pre-PRO"
            elif "PRO" in xvg.data_columns[2][row]:
                AA_type = "PRO"
            elif "GLY" in xvg.data_columns[2][row]:
                AA_type = "GLY"
            else:
                AA_type = "General"
            phi = xvg.data_columns[0][row]
            psi = xvg.data_columns[1][row]
            res = xvg.data_columns[2][row]
            if (
                rama_pref_values[AA_type][int(psi) + 180][int(phi) + 180]
                < rama_preferences[AA_type]["bounds"][1]
            ):
                outliers[AA_type]["phi"].append(phi)
                outliers[AA_type]["psi"].append(psi)
                outliers[AA_type]["res"].append(f"row index {row} : {res}")
            else:
                normals[AA_type]["phi"].append(phi)
                normals[AA_type]["psi"].append(psi)
                normals[AA_type]["res"].append(f"row index {row} : {res}")

        ## print some infos
        print(
            "ramachandran method can draw four types of figure: "
            + "\n        Pre-PRO: the dihedrals of amino acids before prolines"
            + "\n        PRO: the dihedrals of prolines"
            + "\n        GLY: the dihedrals of glynine"
            + "\n        General: the dihedrals of other amino acids"
        )
        print("\n" + "-" * 70)
        print(
            "{:<10} {:>20} {:>20}".format("", "Normal Dihedrals", "Outlier Dihedrals")
        )
        for key in ["General", "GLY", "Pre-PRO", "PRO"]:
            print(
                "{:<10} {:>20} {:>20}".format(
                    key, len(normals[key]["phi"]), len(outliers[key]["phi"])
                )
            )
        print("-" * 70)

        kwargs = {
            "normals": normals,
            "outliers": outliers,
            "rama_pref_values": rama_pref_values,
            "rama_preferences": rama_preferences,
            "xlabel": self.sel_parm(self.parm.xlabel, "$phi$"),
            "ylabel": self.sel_parm(self.parm.ylabel, "$psi$"),
            "title": self.parm.title,
            "x_precision": self.parm.x_precision,
            "y_precision": self.parm.y_precision,
            "outfig": self.parm.output,
            "noshow": self.parm.noshow,
        }
        if self.parm.engine == "matplotlib":
            line = RamachandranMatplotlib(**kwargs)
        elif self.parm.engine == "plotly":
            line = RamachandranPlotly(**kwargs)
        else:
            self.error(
                "Ramachandran plot only supported by matplotlib and plotly engine"
            )
