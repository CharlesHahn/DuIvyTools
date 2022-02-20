"""
XVG module contains the code to process xvg files, including read information from xvg file, visualization, and data convertion.
"""

import os
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


class XVG():
    """XVG module was defined to process XVG file"""

    def __init__(self):
        pass

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
    pass

if __name__ == "__main__":
    main()

