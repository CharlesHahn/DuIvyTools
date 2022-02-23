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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab as pylab

myparams = {
    "axes.labelsize": "12",
    "xtick.labelsize": "12",
    "ytick.labelsize": "12",
    "ytick.left": False,
    "ytick.direction": "in",
    "xtick.bottom": False,
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

    def __init__(self, xvgfile:str = "") -> None:
        """ read xvg file and extract infos """

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
                if "title" in line:
                    self.xvg_title = line.strip("\"").split("\"")[-1]
                elif "xaxis" in line and "label" in line:
                    self.xvg_xlabel = line.strip("\"").split("\"")[-1]
                elif "yaxis" in line and "label" in line:
                    self.xvg_ylabel = line.strip("\"").split("\"")[-1]
                elif line.startswith("@ s") and "legend" in line:
                    self.xvg_legends.append(line.strip("\"").split("\"")[-1])
            else:
                ## extract the column data part
                items = line.split()
                if len(self.xvg_columns) == 0:
                    self.xvg_columns = [ [] for _ in range(len(items)) ]
                    self.xvg_column_num = len(items)
                    self.xvg_row_num = 0
                if len(items) != len(self.xvg_columns):
                    print("Error -> the number of columns in {} is not equal. ".format(self.xvg_filename))
                    print("        " + line)
                    exit()
                for i in range(len(items)):
                    self.xvg_columns[i].append(items[i])
                self.xvg_row_num += 1

        ## post-process the infos
        for c in range(self.xvg_column_num):
            if len(self.xvg_columns[c]) != self.xvg_row_num:
                print("Error -> length of column {} if not equal to count of rows".format(c))
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
            items = [ item.strip() for item in self.xvg_ylabel.split(",") ]
            heads = [ l for l in self.xvg_legends]
            if len(items) == len(self.xvg_legends):
                for i in range(len(items)):
                    heads[i] += " " + items[i]
            elif len(items) == 1:
                for i in range(len(self.data_heads)):
                    heads[i] += " " + items[0]
            else:
                print("Warning -> failed to pair ylabels and legends, use legends in xvg file")
            self.data_heads += heads
            for i in range(len(heads)):
                self.data_columns.append([ float(c) for c in self.xvg_columns[i+1]])

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

        print("Info -> read {} sucessfully".format(self.xvg_filename))


    def calc_average(self, start:int=None, end:int=None) -> tuple:
        """
        calculate the average of each column

        parameters:
            start: the start index 
            end: the end index
        return:
            data_heads: a list contains all data legends
            column_averages: a list contains all average numbers
            column_stds: a list contains all standard error numbers
        """

        if (start != None and end != None) and (start >= end):
            print("Error -> start index should be less than end index")
            exit()
        if (start != None and start >= self.xvg_row_num) or (
                end != None and end >= self.xvg_row_num):
            print("Error -> start or end index should be less than the number of rows in xvg file")
            exit()
        
        column_averages = []
        column_stds = []
        for column in self.data_columns:
            column_averages.append(np.average(column[start:end]))
            column_stds.append(np.std(column[start:end]))

        return self.data_heads, column_averages, column_stds

    def calc_mvave(self):
        pass

    def xvg2csv(self):
        pass

    def draw(self):
        pass


def xvg_combine(xvgfiles:list=[]):
    pass


def xvg_compare(xvgfiles:list=[]):
    pass


def energy_compute(xvgfiles:list=[]):
    pass


def ramachandran(xvgfiles:list=[]):
    pass


def main():
    file = sys.argv[1]
    xvg = XVG(file)
    heads, aves, stds = xvg.calc_average()
    for i in range(len(heads)):
        print("{:>20} {:.2f} {:.2f}".format(heads[i], aves[i], stds[i]))





if __name__ == "__main__":
    main()

