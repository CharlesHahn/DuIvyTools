"""
DCCM module is part of DuIvyTools library, which is a tool for analysis and 
visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to generate dynamical cross correlation matrix from 
covarience xpm file or dat file. 

This DCCM module contains:
    - DCCM class

This file is provided to you by GPLv2 license."""


import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab as pylab
import logging

from DuIvyTools.XPM import XPM

logging.basicConfig(level=logging.INFO, format="%(levelname)s -> %(message)s")
logger = logging.getLogger(__name__)

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

style_files = [file for file in os.listdir() if file[-9:] == ".mplstyle"]
if len(style_files) >= 1:
    plt.style.use(style_files[0])
    logging.info("using matplotlib style sheet from {}".format(style_files[0]))


class DCCM(object):
    """
    class DCCM are designed to generate dynamical cross correlation matrix
    from `gmx covar` command results.
    """

    def __init__(self) -> None:
        self.resnum = 0
        self.xlabel = ""
        self.ylabel = ""
        self.title = ""
        self.xaxis = []
        self.yaxis = []

    def read_xpm(self, xpmfile: str) -> np.ndarray:
        xpm = XPM(xpmfile)
        if xpm.xpm_width != xpm.xpm_height:
            logging.error("Width and height of the xpm file you specified are not equal ")
            sys.exit()

        self.resnum = xpm.xpm_width
        self.xlabel = xpm.xpm_xlabel
        self.ylabel = xpm.xpm_ylabel
        self.title = xpm.xpm_title
        self.xaxis = xpm.xpm_xaxis
        self.yaxis = xpm.xpm_yaxis

        corr_matrix = np.zeros((self.resnum, self.resnum))


        

    def read_xpma(self, xpmfile: str) -> np.ndarray:
        pass

    def read_acsii(self, xpmfile: str) -> np.ndarray:
        pass

    def triple2covar(self, triple_matrix: np.ndarray) -> np.ndarray:
        pass

    def covar2corr(self, covar_matrix: np.ndarray) -> np.ndarray:
        pass

    def draw_corr_origin(self, corr_matrix: np.ndarray) -> None:
        pass

    def draw_corr_gaussian(self, corr_matrix: np.ndarray) -> None:
        pass

    def draw_corr_bio3d(self, corr_matrix: np.ndarray) -> None:
        pass

    def show_or_save(self, plt_obj, outpng: str, noshow: bool = False) -> None:
        if outpng != None:
            if os.path.exists(outpng):
                logging.error("{} already in current directory".format(outpng))
                sys.exit()
            plt_obj.savefig(outpng, dpi=300)
        if noshow == False:
            plt_obj.show()

    def draw(
        self,
        corr_matrix: np.ndarray,
        mode: str = "bio3d",
        noshow: bool = False,
        outpng: str = None,
    ) -> None:
        pass


def dccm_from_xpma(xpmfile: str, mode, noshow, outpng) -> None:
    dccm = DCCM()
    triple_matrix = dccm.read_xpma(xpmfile)
    covar_matrix = dccm.triple2covar(triple_matrix)
    corr_matrix = dccm.covar2corr(covar_matrix)
    dccm.draw(corr_matrix, mode, noshow, outpng)

def dccm_from_ascii(datfile: str, mode, noshow, outpng) -> None:
    dccm = DCCM()
    triple_matrix = dccm.read_acsii(datfile)
    covar_matrix = dccm.triple2covar(triple_matrix)
    corr_matrix = dccm.covar2corr(covar_matrix)
    dccm.draw(corr_matrix, mode, noshow, outpng)

def dccm_from_xpm(xpmfile: str, mode, noshow, outpng) -> None:
    dccm = DCCM()
    covar_matrix = dccm.read_xpm(xpmfile)
    corr_matrix = dccm.covar2corr(covar_matrix)
    dccm.draw(corr_matrix, mode, noshow, outpng)

def dccm_call_functions(arguments: list = None):
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]

    ## parse the command parameters
    parser = argparse.ArgumentParser(description="generate mdp file templates")
    parser.add_argument("-i", "--input", help="specify the input file")
    parser.add_argument("-o", "--output", help="file name to output")
    parser.add_argument("-m", "--mode", help="specify the figure style, 'origin', 'gaussian', 'bio3d'")
    parser.add_argument("-ns", '--noshow', help="whether not to show figure")


    if len(arguments) < 2:
        logging.error("no input parameters, -h or --help for help messages")
        sys.exit()
    method = arguments[1]
    if method in ["-h", "--help"]:
        parser.parse_args(arguments[1:])
        sys.exit()

    args = parser.parse_args(arguments[2:])
    if method == "dccm_xpm":
        dccm_from_xpm(args.input, args.mode, args.noshow, args.output)
    elif method == "dccm_xpma":
        dccm_from_xpma(args.input, args.mode, args.noshow, args.output)
    elif method == "dccm_ascii":
        dccm_from_xpma(args.input, args.mode, args.noshow, args.output)
    else:
        logging.error("unknown method {}".format(method))
        sys.exit()

    logging.info("May you good day !")


def main():
    dccm_call_functions()


if __name__ == "__main__":
    main()
