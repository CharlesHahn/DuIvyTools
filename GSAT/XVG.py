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
        self.xvg_row_numn = 0
        self.xvg_columns = []

        self.ylabel_list = []
        self.data = {}

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
                    self.xvg_columns = [ [] for i in range(len(items)) ]
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

        self.data[self.xvg_xlabel] = [ float(c) for c in self.xvg_columns[0] ]
        if len(self.xvg_legends) == 0 and len(self.xvg_columns) > 1:
            self.ylabel_list.append(self.xvg_ylabel)
            self.data[self.xvg_ylabel] = [ float(c) for c in self.xvg_columns[1] ]
        if len(self.xvg_legends) > 0 and len(self.xvg_columns) > len(self.xvg_legends):
            items = [ item.strip() for item in self.xvg_ylabel.split(",") ]
            self.ylabel_list = self.xvg_legends
            if len(items) == len(self.xvg_legends):
                for i in range(len(items)):
                    self.ylabel_list[i] += " " + items[i]
            for i in range(len(self.ylabel_list)):
                self.data[self.ylabel_list[i]] = [ float(c) for c in self.xvg_columns[i+1]]

        print("Info -> read {} sucessfully".format(self.xvg_filename))


    def calc_average(self):
        pass

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
    XVG(file)





if __name__ == "__main__":
    main()

