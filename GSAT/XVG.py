"""This module is part of GMX_Simple_Analysis_Tool library. Written by CharlesHahn.

XVG module contains the code to process xvg files, including read information from xvg file, visualization, and data convertion.

This module requires Numpy, Matplotlib and argparse. 

This module contains:
    class XVG
    function xvg_combine, xvg_compare, energy_compute, ramachandran

This file is provided to you under GPLv2 License"""


import os
import sys
import math
import argparse
import logging
import numpy as np
import scipy.stats as stats
from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib import pylab as pylab
from matplotlib import colors
import matplotlib.colors as mplcolors


logging.basicConfig(level=logging.INFO)

myparams = {
    "axes.labelsize": "12",
    "xtick.labelsize": "12",
    "ytick.labelsize": "12",
    "ytick.left": True,
    "ytick.direction": "in",
    "xtick.bottom": True,
    "xtick.direction": "in",
    "lines.linewidth": "2",
    "axes.linewidth": "1",
    "legend.fontsize": "12",
    "legend.loc": "upper right",
    "legend.fancybox": False,
    "legend.frameon": False,
    "font.family": "Arial",
    "font.size": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "axes.prop_cycle": cycler(
        "color",
        [
            "#38A7D0",
            "#F67088",
            "#66C2A5",
            "#FC8D62",
            "#8DA0CB",
            "#E78AC3",
            "#A6D854",
            "#FFD92F",
            "#E5C494",
            "#B3B3B3",
            "#66C2A5",
            "#FC8D62",
        ],
    ),
}
pylab.rcParams.update(myparams)


class XVG(object):
    """XVG module was defined to process XVG file

    Attributes:
    xvg_filename: the name of xvg file
    xvg_title: the title of xvg file
    xvg_xlabel: the x-label of xvg file
    xvg_ylabel: the y-label of xvg file
    xvg_legends: a list to store legends
    xvg_columns: a list to store data
    xvg_data: a dict to store data

    Functions:
    __init__: read xvg file and extract infos
    calc_average: calculate the average of xvg data
    calc_mvave: calculate the moving average of xvg data
    xvg2csv : convert xvg data to csv format
    draw: draw xvg data to figure
    """

    def __init__(self, xvgfile: str = "") -> None:
        """read xvg file and extract infos"""

        self.xvg_filename = xvgfile
        self.xvg_title = ""
        self.xvg_xlabel = ""
        self.xvg_ylabel = ""
        self.xvg_legends = []
        self.xvg_column_num = 0
        self.xvg_row_num = 0
        self.xvg_columns = []

        self.data_heads = []
        self.data_columns = []

        ## check kand read xpm file
        if not os.path.exists(xvgfile):
            print("ERROR -> no {} in current directory".format(xvgfile))
            exit()
        if xvgfile[-4:] != ".xvg":
            print("Error -> specify a xvg file with suffix xvg")
            exit()
        with open(xvgfile, "r") as fo:
            lines = [line.strip() for line in fo.readlines() if line.strip() != ""]

        ## extract data from xvg file content
        for line in lines:
            if line.startswith("#") or line.startswith("&"):
                continue
            elif line.startswith("@"):
                if " title " in line:
                    self.xvg_title = line.strip('"').split('"')[-1]
                elif " xaxis " in line and " label " in line:
                    self.xvg_xlabel = line.strip('"').split('"')[-1]
                elif " yaxis " in line and " label " in line:
                    self.xvg_ylabel = line.strip('"').split('"')[-1]
                elif line.startswith("@ s") and " legend " in line:
                    self.xvg_legends.append(line.strip('"').split('"')[-1])
            else:
                ## extract the column data part
                items = line.split()
                if len(self.xvg_columns) == 0:
                    self.xvg_columns = [[] for _ in range(len(items))]
                    self.xvg_column_num = len(items)
                    self.xvg_row_num = 0
                if len(items) != len(self.xvg_columns):
                    print(
                        "Error -> the number of columns in {} is not equal. ".format(
                            self.xvg_filename
                        )
                    )
                    print("{} -> ".format(self.xvg_row_num) + line)
                    exit()
                for i in range(len(items)):
                    self.xvg_columns[i].append(items[i])
                self.xvg_row_num += 1

        ## post-process the infos
        for c in range(self.xvg_column_num):
            if len(self.xvg_columns[c]) != self.xvg_row_num:
                print(
                    "Error -> length of column {} if not equal to count of rows".format(
                        c
                    )
                )
                exit()
        if self.xvg_column_num == 0 or self.xvg_row_num == 0:
            print("Error -> no data line detected in xvg file")
            exit()

        self.data_heads.append(self.xvg_xlabel)
        self.data_columns.append([float(c) for c in self.xvg_columns[0]])
        if len(self.xvg_legends) == 0 and len(self.xvg_columns) > 1:
            self.data_heads.append(self.xvg_ylabel)
            self.data_columns.append([float(c) for c in self.xvg_columns[1]])
        if len(self.xvg_legends) > 0 and len(self.xvg_columns) > len(self.xvg_legends):
            items = [item.strip() for item in self.xvg_ylabel.split(",")]
            heads = [l for l in self.xvg_legends]
            if len(items) == len(self.xvg_legends):
                for i in range(len(items)):
                    heads[i] += " " + items[i]
            elif len(items) == 1 and (items[0][0] == "(" and items[0][-1] == ")"):
                for i in range(len(heads)):
                    heads[i] += " " + items[0]
            else:
                print(
                    "Warning -> failed to pair ylabels and legends, use legends in xvg file"
                )
            self.data_heads += heads
            for i in range(len(heads)):
                self.data_columns.append([float(c) for c in self.xvg_columns[i + 1]])

        ## test
        # print(self.xvg_title)
        # print(self.xvg_xlabel)
        # print(self.xvg_ylabel)
        # print(self.xvg_legends)
        # print(self.xvg_column_num)
        # print(self.xvg_row_num)
        # print(len(self.xvg_columns))
        # print(self.data_heads)
        # print(len(self.data_columns))

        print("Info -> read {} successfully. ".format(self.xvg_filename))

    def calc_average(self, start: int = None, end: int = None) -> tuple:
        """
        calculate the average of each column

        :parameters:
            start: the start index
            end: the end index
        :return:
            data_heads: a list contains all data legends
            column_averages: a list contains all average numbers
            column_stds: a list contains all standard error numbers
        """

        if (start != None and end != None) and (start >= end):
            print("Error -> start index should be less than end index")
            exit()
        if (start != None and start >= self.xvg_row_num) or (
            end != None and end >= self.xvg_row_num
        ):
            print(
                "Error -> start or end index should be less than the number of rows in xvg file"
            )
            exit()

        column_averages = []
        column_stds = []
        for column in self.data_columns:
            column_averages.append(np.average(column[start:end]))
            column_stds.append(np.std(column[start:end]))

        return self.data_heads, column_averages, column_stds

    def calc_mvave(self, windowsize: int = 10, confidence: float = 0.95) -> tuple:
        """
        calculate the moving average of each column

        :parameters:
            windowsize: the window size for calculating moving average
            confidence: the confidence to calculate interval

        :return:
            data_heads: a list contains all data legends
            column_mvaves: a list contains all moving average
            column_highs: the high value of interval of moving averages
            column_lows: the low value of interval of moving averages
        """

        if windowsize <= 0 or windowsize > int(self.xvg_row_num / 2):
            print("Error -> windowsize value is not proper")
            exit()
        if confidence <= 0 or confidence >= 1:
            print("Error -> confidence value is not proper, it should be in (0,1)")
            exit()

        column_mvaves, column_highs, column_lows = [], [], []
        for column in self.data_columns:
            mv_ave = [np.nan for _ in range(windowsize)]
            high = [np.nan for _ in range(windowsize)]
            low = [np.nan for _ in range(windowsize)]
            for i in range(windowsize, self.xvg_row_num):
                window_data = column[i - windowsize : i]
                ave = np.mean(window_data)
                std = np.std(window_data)
                interval = stats.norm.interval(confidence, ave, std)
                mv_ave.append(ave)
                low.append(interval[0])
                high.append(interval[1])
            column_mvaves.append(mv_ave)
            column_lows.append(low)
            column_highs.append(high)

        return self.data_heads, column_mvaves, column_highs, column_lows

    def xvg2csv(self, outcsv: str = "") -> None:
        """
        convert xvg data into csv file

        :parameters:
            outcsv: the csv file name for output
        """

        ## check parameters
        if outcsv == "":
            outcsv = self.xvg_filename[:-4] + ".csv"
        if outcsv[-4:] != ".csv":
            print("Error -> please specify a csv file name with suffix .csv")
            exit()
        if os.path.exists(outcsv):
            print("Error -> already a {} in current directory".format(outcsv))
            exit()

        ## write csv file
        out_data = []
        if len(self.data_columns) == len(self.xvg_columns):
            out_data = [column for column in self.data_columns]
        elif len(self.data_columns) < len(self.xvg_columns):
            out_data = [column for column in self.data_columns]
            out_data += [
                column for column in self.xvg_columns[len(self.data_columns) :]
            ]
        with open(outcsv, "w") as fo:
            fo.write(",".join(self.data_heads) + "\n")
            for row in range(self.xvg_row_num):
                fo.write(",".join([str(column[row]) for column in out_data]) + "\n")

        print(
            "Info -> convert {} into {} successfully.".format(self.xvg_filename, outcsv)
        )

    def draw(self) -> None:
        """
        draw xvg data into figure
        """

        column_num = len(self.data_columns)
        x_min = np.min(self.data_columns[0])
        x_max = np.max(self.data_columns[0])
        x_space = int((x_max - x_min) / 100)
        grid = (plt.GridSpec(1, column_num), plt.GridSpec(2, int(column_num / 2)))[
            column_num > 2
        ]
        for i in range(1, column_num):
            ## use grid for subplots layout
            if i == column_num - 1:
                ax = plt.subplot(
                    grid[
                        (1, 0)[i - 1 < int((column_num) / 2)],
                        (i - 1) % int((column_num) / 2) :,
                    ]
                )
            else:
                ax = plt.subplot(
                    grid[
                        (1, 0)[i - 1 < int((column_num) / 2)],
                        (i - 1) % int((column_num) / 2),
                    ]
                )
            ax.plot(self.data_columns[0], self.data_columns[i])
            ax.set_ylabel(self.data_heads[i])
            plt.xlim(int(x_min - x_space), int(x_max + x_space))
            plt.xlabel(self.data_heads[0])
        plt.suptitle(self.xvg_title)
        plt.tight_layout()
        plt.show()

    def draw_distribution(self, bin: int = 100) -> None:
        """
        calculate the distribution of each column and draw

        :parameters:
            bin: the bin size of frequency calculation
        """

        column_num = len(self.data_columns)
        grid = plt.GridSpec(2, int((column_num + 1) / 2))
        for i in range(column_num):
            column = self.data_columns[i]
            ## calculate distribution
            column_min = np.min(column)
            column_max = np.max(column)
            bin_window = (column_max - column_min) / bin
            if bin_window != 0:
                frequency = [0 for _ in range(bin)]
                for value in column:
                    index = int((value - column_min) / bin_window)
                    if index == bin:  # for the column_max
                        index = bin - 1
                    frequency[index] += 1
                if sum(frequency) != self.xvg_row_num:
                    print("Error -> wrong in calculating distribution")
                    exit()
                frequency = [f * 100.0 / self.xvg_row_num for f in frequency]
                x_value = [column_min + bin_window * b for b in range(bin)]
            else:  # for data without fluctuation
                frequency = [1]
                x_value = [column_min]
            ## draw distribution
            if i == column_num - 1:
                ax = plt.subplot(
                    grid[
                        (1, 0)[i < int((column_num + 1) / 2)],
                        i % int((column_num + 1) / 2) :,
                    ]
                )
            else:
                ax = plt.subplot(
                    grid[
                        (1, 0)[i < int((column_num + 1) / 2)],
                        i % int((column_num + 1) / 2),
                    ]
                )
            # ax = plt.subplot(int((column_num+1)/2), 2, i+1)
            ax.plot(x_value, frequency)
            ax.set_xlabel(self.data_heads[i])
            ax.set_ylabel("Frequency %")
            plt.xlim(column_min - bin_window, column_max + bin_window)
        plt.suptitle("Frequency of " + self.xvg_title)
        # plt.subplots_adjust(wspace=0.8)
        plt.tight_layout()
        plt.show()

    def draw_stacking(
        self, column_index2start: int = 1, column_index2end: int = None
    ) -> None:
        """
        draw xvg data into stacking figure

        :parameters:
            column_index2start: the index of data column to start plot
            column_index2end: the index of data column to end plot
        """

        ## check parameters
        if column_index2start >= len(self.data_columns):
            print(
                "Warning -> column_index2start not in proper range, use default value."
            )
            column_index2start = 1
        if column_index2end == None:
            column_index2end = len(self.data_columns)
        else:
            if column_index2end <= column_index2start or column_index2end > len(
                self.data_columns
            ):
                print(
                    "Warning -> column_index2end not in proper range, use default value."
                )
                column_index2end = len(self.data_columns)

        ## draw stacked plot
        ylim_max, ylim_min = 0, 0
        for stack_index in range(column_index2start, column_index2end):
            stack_data = [
                sum(
                    [
                        self.data_columns[i][row]
                        for i in range(
                            column_index2start,
                            column_index2end - (stack_index - column_index2start),
                        )
                    ]
                )
                for row in range(self.xvg_row_num)
            ]
            # plt.plot(self.data_columns[0], stack_data, label=self.data_heads[stack_index])
            plt.fill_between(
                self.data_columns[0],
                stack_data,
                [0 for _ in range(len(stack_data))],
                label=self.data_heads[
                    column_index2end + column_index2start - stack_index - 1
                ],
            )
            ylim_max = (ylim_max, max(stack_data))[ylim_max < max(stack_data)]
            ylim_min = (ylim_min, min(stack_data))[ylim_min > min(stack_data)]
        # print(ylim_min, ylim_max)
        plt.xlabel(self.data_heads[0])
        plt.ylabel(self.xvg_ylabel)
        plt.title("Stacked plot of " + self.xvg_title)
        plt.xlim(np.min(self.data_columns[0]), np.max(self.data_columns[0]))
        plt.ylim(ylim_min, ylim_max)
        plt.legend(loc=3)
        plt.show()

    def draw_scatter(self, x_index: int = 0, y_index: int = None) -> None:
        """
        draw xvg data to scatter plot

        :parameters:
            x_index: the column index of x values for scatter plot
            y_index: the column index of y values for scatter plot
        """

        ## check parameters
        if x_index >= len(self.data_columns) or x_index < 0:
            print("Warning -> x_index not in proper range, use default value.")
            x_index = 0
        if y_index == None:
            y_index = len(self.data_columns) - 1
        else:
            if y_index >= len(self.data_columns) or y_index < 0:
                print("Warning -> y_index not in proper range, use default value.")
                y_index = len(self.data_columns) - 1

        ## draw scatter plot
        plt.scatter(self.data_columns[x_index], self.data_columns[y_index])
        plt.ylabel(self.data_heads[y_index])
        plt.xlabel(self.data_heads[x_index])
        plt.title(
            "Scatter plot of {} vs {}".format(
                self.data_heads[x_index], self.data_heads[y_index]
            )
        )
        plt.show()


def xvg_combine(
    xvgfile_0: str = "",
    xvgfile_1: str = "",
    column_select_0: list = [],
    column_select_1: list = [],
    outfilename: str = "",
) -> None:
    """
    combine two xvg files by specified column index

    :parameters:
        xvgfile_0: the first xvg file you wanna combine
        xvgfile_1: the last xvg file you wanna combine
        column_select_0: a list to store all column index you wanna combine in xvgfile_0
        column_select_1: a list to store all column index you wanna combine in xvgfile_1
        outfilename: the output xvg file name
    """

    ## check parameters
    if not os.path.exists(xvgfile_0) or not os.path.exists(xvgfile_1):
        print("Error -> No {} or {} in current directory".format(xvgfile_0, xvgfile_1))
        exit()
    if os.path.exists(outfilename):
        print("Error -> {} already in current directory".format(outfilename))
        exit()
    if len(outfilename) < 4 or outfilename[-4:] != ".xvg":
        print("Error -> please specify a output filename with suffix .xvg")
        exit()

    xvg_0, xvg_1 = XVG(xvgfile_0), XVG(xvgfile_1)
    if len(column_select_0) == 0:
        column_select_0 = [i for i in range(len(xvg_0.data_columns))]
    if len(column_select_1) == 0:
        column_select_1 = [i for i in range(len(xvg_1.data_columns))]
    if not (set(column_select_0) <= set([i for i in range(len(xvg_0.data_columns))])):
        print(
            "Error -> column_select_0 should be in proper range, [{},{})".format(
                0, len(xvg_0.data_columns)
            )
        )
        exit()
    if not (set(column_select_1) <= set([i for i in range(len(xvg_1.data_columns))])):
        print(
            "Error -> column_select_1 should be in proper range, [{},{})".format(
                0, len(xvg_1.data_columns)
            )
        )
        exit()
    if xvg_0.xvg_row_num != xvg_1.xvg_row_num:
        print("Error -> the numbers of rows in your input xvg files are not equal !")
        exit()

    ## process xvg combination
    combined_data_heads = [xvg_0.data_heads[i] for i in column_select_0]
    combined_data_heads += [xvg_1.data_heads[i] for i in column_select_1]
    combined_data_columns = [xvg_0.data_columns[i] for i in column_select_0]
    combined_data_columns += [xvg_1.data_columns[i] for i in column_select_1]
    combined_title = (
        " And ".join([xvg_0.xvg_title, xvg_1.xvg_title]),
        xvg_0.xvg_title,
    )[xvg_0.xvg_title == xvg_1.xvg_title]
    combined_xlabel = combined_data_heads[0]
    ## write combined results
    with open(outfilename, "w") as fo:
        fo.write("# this file was created by combination of thess two xvg file:\n")
        fo.write(
            "#     file 0: {}, column index: {};\n".format(
                xvgfile_0, " ".join([str(i) for i in column_select_0])
            )
        )
        fo.write(
            "#     file 1: {}, column index: {};\n".format(
                xvgfile_1, " ".join([str(i) for i in column_select_1])
            )
        )
        fo.write('@    title "{}"\n'.format(combined_title))
        fo.write('@    xaxis label "{}"\n'.format(combined_xlabel))
        fo.write("@TYPE xy\n@ view 0.15, 0.15, 0.75, 0.85\n")
        fo.write("@ legend on\n@ legend box on\n@ legend loctype view\n")
        fo.write(
            "@ legend 0.78, 0.8\n@ legend length {}\n".format(
                len(combined_data_heads) - 1
            )
        )
        for s in range(1, len(combined_data_heads)):
            fo.write('@ s{} legend "{}"\n'.format(s - 1, combined_data_heads[s]))
        for row in range(xvg_0.xvg_row_num):
            fo.write(
                " ".join(
                    [
                        "{:>20.6f}".format(combined_data_columns[i][row])
                        for i in range(len(combined_data_columns))
                    ]
                )
                + "\n"
            )
    print("Info -> {} and {} combined sucessfully.".format(xvgfile_0, xvgfile_1))


def energy_compute(
    prolig_xvg: str = "", pro_xvg: str = "", lig_xvg: str = "", outfile: str = ""
):
    """
    compute the interaction between protein and ligand by:
        binding energy  = prolig energy - pro energy - lig energy

    :parameters::
        prolig_xvg: energy xvg file of prolig
        pro_xvg: energy xvg file of protein
        lig_xvg: energy xvg file of ligand
        outfile: the output xvg file name

    IMPORTANT:
        the xvg file used here should contain and ONLY contain five columns:
        Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip.
    """

    ## check parameters
    for xvgfile in [prolig_xvg, pro_xvg, lig_xvg]:
        if not os.path.exists(xvgfile):
            print("Error -> No {} in current directory".format(xvgfile))
            exit()
    if os.path.exists(outfile):
        print("Error -> {} already in current directory".format(outfile))
        exit()
    if len(outfile) < 4 or outfile[-4:] != ".xvg":
        print("Error -> please specify a output filename with suffix .xvg")
        exit()
    prolig, pro, lig = XVG(prolig_xvg), XVG(pro_xvg), XVG(lig_xvg)
    if not (prolig.data_heads == pro.data_heads == lig.data_heads) or (
        len(prolig.data_heads) != 5
    ):
        print(
            "Error -> three xvg files should contain same number (5) of columns, "
            + "and the order should be: \n"
            + "    Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip. "
        )
        exit()
    if not (
        ("Time" in prolig.data_heads[0])
        and ("LJ" in prolig.data_heads[1])
        and ("Disper" in prolig.data_heads[2])
        and ("Coulomb" in prolig.data_heads[3])
        and ("recip" in prolig.data_heads[4])
    ):
        print(
            "Error ->  the legend order should be: \n"
            + "    Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip. "
        )
        exit()
    if not (prolig.xvg_row_num == pro.xvg_row_num == lig.xvg_row_num):
        print("Error -> {}, {}, {} should contain same number of rows.")
        exit()
    if not (prolig.data_columns[0] == pro.data_columns[0] == lig.data_columns[0]):
        print("Error -> the Time axis may not be the same, check the interval of time.")
        exit()

    ## compute the bingding energy
    ## time
    out_data = [prolig.data_columns[0]] + [[] for i in range(9)]
    out_heads = (
        [prolig.data_heads[0]]
        + [head for head in prolig.xvg_legends]
        + ["LJ(all)", "Coulomb(all)", "Short-Range", "Long-Range", "Total Energy"]
    )
    ## LJ(SR)
    out_data[1] = [
        prolig.data_columns[1][row]
        - pro.data_columns[1][row]
        - lig.data_columns[1][row]
        for row in range(prolig.xvg_row_num)
    ]
    ## Disper.corr.
    out_data[2] = [
        prolig.data_columns[2][row]
        - pro.data_columns[2][row]
        - lig.data_columns[2][row]
        for row in range(prolig.xvg_row_num)
    ]
    ## Coulomb(SR)
    out_data[3] = [
        prolig.data_columns[3][row]
        - pro.data_columns[3][row]
        - lig.data_columns[3][row]
        for row in range(prolig.xvg_row_num)
    ]
    ## Coul.recip.
    out_data[4] = [
        prolig.data_columns[4][row]
        - pro.data_columns[4][row]
        - lig.data_columns[4][row]
        for row in range(prolig.xvg_row_num)
    ]
    ## LJ(all)
    out_data[5] = [
        out_data[1][row] + out_data[2][row] for row in range(prolig.xvg_row_num)
    ]
    ## Coulomb(all)
    out_data[6] = [
        out_data[3][row] + out_data[4][row] for row in range(prolig.xvg_row_num)
    ]
    ## Short-Range
    out_data[7] = [
        out_data[1][row] + out_data[3][row] for row in range(prolig.xvg_row_num)
    ]
    ## Long-Range
    out_data[8] = [
        out_data[2][row] + out_data[4][row] for row in range(prolig.xvg_row_num)
    ]
    ## Total Energy
    out_data[9] = [
        out_data[5][row] + out_data[6][row] for row in range(prolig.xvg_row_num)
    ]

    ## write energy computation results
    with open(outfile, "w") as fo:
        fo.write("# this file was created by XVG.energy_compute through: \n")
        fo.write("#    binding = prolig energy - protein energy - ligand energy\n")
        fo.write('@    title "{}"\n'.format(prolig.xvg_title))
        fo.write('@    xaxis label "{}"\n'.format(out_heads[0]))
        fo.write('@    yaxis label "{}"\n'.format("(kJ/mol)"))
        fo.write("@TYPE xy\n@ view 0.15, 0.15, 0.75, 0.85\n")
        fo.write("@ legend on\n@ legend box on\n@ legend loctype view\n")
        fo.write("@ legend 0.78, 0.8\n@ legend length 9\n")
        for s in range(1, 10):
            fo.write('@ s{} legend "{}"\n'.format(s - 1, out_heads[s]))
        for row in range(prolig.xvg_row_num):
            fo.write(
                " ".join(["{:>16.6f}".format(out_data[i][row]) for i in range(10)])
                + "\n"
            )

    print(
        "Info -> energy computation through {}, {} and {} sucessfully.".format(
            prolig_xvg, pro_xvg, lig_xvg
        )
    )


def ramachandran(xvgfile: str = "") -> None:
    """
    convert xvg data into ramachandran plot

    :parameters:
        xvgfile: a xvg file contains phi, psi and AA name data which generated by gmx rama
    """

    ## check parameters
    if not os.path.exists(xvgfile):
        print("Error -> No {} in current directory".format(xvgfile))
        exit()

    xvg = XVG(xvgfile)

    ## check column number
    if (
        len(xvg.xvg_columns) != 3
        or len(xvg.data_columns) != 2
        or (xvg.data_heads[0] != "Phi" or xvg.data_heads[1] != "Psi")
    ):
        print("Error -> Check your input xvg file !")
        print("         It has to contains 3 columns: Phi, Psi, AA name")
        print("         X-label should be Phi and Y-label should be Psi")
        exit()

    ## draw background
    ## Psi and Phi data are from DOI: 10.1002/prot.10286
    ## reference : pyrama
    rama_preferences = {
        "General": {
            "file": os.path.join("data", "pref_general.data"),
            "cmap": mplcolors.ListedColormap(["#FFFFFF", "#B3E8FF", "#7FD9FF"]),
            "bounds": [0, 0.0005, 0.02, 1],
        },
        "GLY": {
            "file": os.path.join("data", "pref_glycine.data"),
            "cmap": mplcolors.ListedColormap(["#FFFFFF", "#FFE8C5", "#FFCC7F"]),
            "bounds": [0, 0.002, 0.02, 1],
        },
        "PRO": {
            "file": os.path.join("data", "pref_proline.data"),
            "cmap": mplcolors.ListedColormap(["#FFFFFF", "#D0FFC5", "#7FFF8C"]),
            "bounds": [0, 0.002, 0.02, 1],
        },
        "Pre-PRO": {
            "file": os.path.join("data", "pref_preproline.data"),
            "cmap": mplcolors.ListedColormap(["#FFFFFF", "#B3E8FF", "#7FD9FF"]),
            "bounds": [0, 0.002, 0.02, 1],
        },
    }

    rama_pref_values = {}
    for key, val in rama_preferences.items():
        data_file_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        rama_pref_values[key] = [[0 for i in range(361)] for i in range(361)]
        with open(os.path.join(data_file_path, val["file"])) as fn:
            for line in fn:
                if line.startswith("#"):
                    continue
                else:
                    phi = int(float(line.split()[0]))
                    psi = int(float(line.split()[1]))
                    ## plt.imshow show transpose of img
                    rama_pref_values[key][psi + 180][phi + 180] = float(line.split()[2])
                    rama_pref_values[key][psi + 179][phi + 180] = float(line.split()[2])
                    rama_pref_values[key][psi + 180][phi + 179] = float(line.split()[2])
                    rama_pref_values[key][psi + 179][phi + 179] = float(line.split()[2])

    normals, outliers = {}, {}
    for key in rama_preferences.keys():
        normals[key] = {"phi": [], "psi": []}
        outliers[key] = {"phi": [], "psi": []}
    for row in range(xvg.xvg_row_num):
        if row < xvg.xvg_row_num - 1 and "PRO" in xvg.xvg_columns[2][row + 1]:
            AA_type = "Pre-PRO"
        elif "PRO" in xvg.xvg_columns[2][row]:
            AA_type = "PRO"
        elif "GLY" in xvg.xvg_columns[2][row]:
            AA_type = "GLY"
        else:
            AA_type = "General"
        phi, psi = xvg.data_columns[0][row], xvg.data_columns[1][row]
        if (
            rama_pref_values[AA_type][int(psi) + 180][int(phi) + 180]
            < rama_preferences[AA_type]["bounds"][1]
        ):
            outliers[AA_type]["phi"].append(phi)
            outliers[AA_type]["psi"].append(psi)
        else:
            normals[AA_type]["phi"].append(phi)
            normals[AA_type]["psi"].append(psi)

    ## print some infos
    print("Info -> ramachandran method can draw four types of figure: ")
    print("        Pre-PRO: the dihedrals of amino acids before prolines")
    print("        PRO: the dihedrals of prolines")
    print("        GLY: the dihedrals of glynine")
    print("        General: the dihedrals of other amino acids")
    print("\n{:<10} {:>20} {:>20}".format("", "Normal Dihedrals", "Outlier Dihedrals"))
    for key in ["General", "GLY", "Pre-PRO", "PRO"]:
        print("{:<10} {:>20} {:>20}".format(
            key, len(normals[key]["phi"]), len(outliers[key]["phi"])))

    ## draw ramachandran plot
    for key in ["General", "GLY", "Pre-PRO", "PRO"]:
        if len(normals[key]["phi"]) + len(outliers[key]["phi"]) == 0 :
            continue
        plt.title(key)
        plt.imshow(
            rama_pref_values[key],
            cmap=rama_preferences[key]["cmap"],
            norm=colors.BoundaryNorm(
                rama_preferences[key]["bounds"], rama_preferences[key]["cmap"].N
            ),
            extent=(-180, 180, 180, -180),
        )
        plt.scatter(normals[key]["phi"], normals[key]["psi"], s=8)
        plt.scatter(outliers[key]["phi"], outliers[key]["psi"], s=8)
        plt.xlim([-180, 180])
        plt.ylim([-180, 180])
        plt.xticks([-180, -120, -60, 0, 60, 120, 180])
        plt.yticks([-180, -120, -60, 0, 60, 120, 180])
        plt.tick_params(left=False, bottom=False)
        plt.xlabel("Phi")
        plt.ylabel("Psi")
        plt.show()


def xvg_compare(xvgfiles: list = [], column_select:list=[], legend_list:list=None, 
                start:int=0, end:int=None, xlabel:str=None, ylabel:str=None, 
                title:str=None, showMV:bool=False, windowsize:int=50, 
                confidence:float=0.95, alpha:float=0.4) -> None:
    """
    comparison of xvgfiles, draw different columns into figure.

    :parameters:
        xvgfiles: a list to store all xvg files you want to compare
        column_select: a list to store the columns you select to compare
                        This list has to contain lists with same number to xvg files
        legend_list: a list to store the legends you specify, and it's number should 
                     be the same with column_index_list and xvgfilees
        start: the start index of column data you want to compare
        end: the end index of column data you want to compare
        xlabel: the xlabel of final figure
        ylabel: the ylbael of final figure
        title: the title of final figure
        showMV: whether to show moving average
        windowsize: the size of window for calculation of moving average
        confidence: the confidence to calculate interval
    
    :example:
        xvg_compare([file1, file2], [[1,2], [2,3]], 
                    ["legend1", "legend2", "legend3", "legend4"],
                    0, 100, "Time", "ylabel", "title")
    """

    ## check parameters
    if len(xvgfiles) == 0:
        print("Error -> no input xvg file to compare")
        exit()
    if len(xvgfiles) != len(column_select):
        print("Error -> column_select must contain {} list".format(len(xvgfiles)))
        exit()
    for column in column_select:
        if not isinstance(column, list):
            print("Error -> the item in column_select must be list type")
            exit()
    if legend_list != None and len(legend_list) != sum(
            [len(column) for column in column_select]):
        print("Error -> number of legends you input can not pair to columns you select")
        exit()
    if title == None:
        title = "XVG Comparison"

    ## draw comparison
    XVGS = [ XVG(xvg) for xvg in xvgfiles]
    legend_count, xmin, xmax = 0, None, None
    for id, column_indexs in enumerate(column_select):
        xvg = XVGS[id]
        if showMV == True:
            _, mvaves, highs, lows = xvg.calc_mvave(windowsize, confidence)
        else:
            _, mvaves, highs, lows = [], [], [], []
        if start != None and start < 0:
            start = 0
        if end != None and end >= xvg.xvg_row_num:
            end = None
        if xlabel == None:
            xlabel = xvg.xvg_xlabel
        if ylabel == None:
            ylabel = xvg.xvg_ylabel
        for index in column_indexs:
            if legend_list != None:
                legend = legend_list[legend_count]
            else:
                legend = "{} of {}".format(xvg.data_heads[index], xvg.xvg_filename)
            legend_count += 1
            if xmin == None:
                xmin = min(xvg.data_columns[0][start:end])
            if xmax == None:
                xmax = max(xvg.data_columns[0][start:end])
            xmin = (min(xvg.data_columns[0][start:end]), xmin)[
                xmin < min(xvg.data_columns[0][start:end])]
            xmax = (max(xvg.data_columns[0][start:end]), xmax)[
                xmax > max(xvg.data_columns[0][start:end])]
            if showMV == True:
                plt.fill_between(xvg.data_columns[0], highs[index], 
                                 lows[index], alpha=alpha)
                plt.plot(xvg.data_columns[0], mvaves[index], label=legend)
            else:
                plt.plot(xvg.data_columns[0][start: end], 
                        xvg.data_columns[index][start: end], label=legend)
    plt.xlim(xmin, xmax)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()



def average_bar_draw(xvgfiles: list = []):
    pass


def average_box_draw(xvgfiles: list = []):
    pass


def main():
    f1 = sys.argv[1]

    xvg_compare([f1], [[1,2,3,4]], ["1", "2", "3", "4"], showMV=True)


if __name__ == "__main__":
    main()
