"""
DCCM module is part of DuIvyTools library, which is a tool for analysis and 
visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to generate dynamical cross correlation matrix from 
covarience dat file generated by `gmx covar`. 

This DCCM module contains:
    - DCCM class

This file is provided to you by GPLv2 license."""


import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pylab as pylab
from matplotlib import colors
import logging

from DuIvyTools.XPM import XPM

logging.basicConfig(level=logging.INFO, format="%(levelname)s -> %(message)s")
logger = logging.getLogger(__name__)


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

    def read_acsii(self, xpmfile: str) -> np.ndarray:
        covar = pd.read_csv(xpmfile, sep=" ", header=None)
        self.resnum = int(np.sqrt((covar.shape[0]) / 3))
        results = pd.DataFrame()
        for i in range(self.resnum):
            one_N = pd.DataFrame()
            for j in range(
                (i * self.resnum) * 3,
                int(len(covar) / self.resnum) * (i + 1),
                self.resnum,
            ):
                df = covar[j : self.resnum + j].reset_index(drop=True)
                one_N = pd.concat([one_N, df], ignore_index=True, axis=1)
            results = pd.concat([results, one_N], ignore_index=True, axis=0)
        results["sum"] = results.sum(axis=1)
        covar = results["sum"].to_numpy()
        covar = covar.reshape(self.resnum, self.resnum)
        return covar

    def covar2corr(self, covar_matrix: np.ndarray) -> np.ndarray:
        corr = np.zeros((self.resnum, self.resnum))
        for i in range(self.resnum):
            for j in range(self.resnum):
                corr[i, j] = covar_matrix[i, j] / np.sqrt(
                    covar_matrix[i, i] * covar_matrix[j, j]
                )
        return corr

    def draw_corr_origin(
        self, corr_matrix: np.ndarray, outpng: str, noshow: bool = False
    ) -> None:
        lis = [
            "#FF80FF",
            "#FFA8FF",
            "#FFD4FF",
            "#FFFCFF",
            "#FFFCFF",
            "#D4FFFF",
            "#A8FFFF",
            "#80FFFF",
        ]
        cm = colors.ListedColormap(lis)
        plt.clf()
        im = plt.imshow(
            corr_matrix, vmin=-1, vmax=1, origin="lower", interpolation="none"
        )
        cb = plt.colorbar(im)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.tight_layout()
        if outpng != None:
            if os.path.exists(outpng):
                logging.error("{} already in current directory".format(outpng))
                sys.exit()
            plt.savefig(outpng, dpi=300)
        if noshow == False:
            plt.show()

    def draw_corr_gaussian(
        self, corr_matrix: np.ndarray, outpng: str, noshow: bool = False
    ) -> None:
        lis = [
            "#FF80FF",
            "#FFA8FF",
            "#FFD4FF",
            "#FFFCFF",
            "#FFFCFF",
            "#D4FFFF",
            "#A8FFFF",
            "#80FFFF",
        ]
        cm = colors.ListedColormap(lis)
        plt.clf()
        im = plt.imshow(
            corr_matrix,
            cmap=cm,
            vmin=-1,
            vmax=1,
            origin="lower",
            interpolation="gaussian",
        )
        cb = plt.colorbar(im)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.tight_layout()
        if outpng != None:
            if os.path.exists(outpng):
                logging.error("{} already in current directory".format(outpng))
                sys.exit()
            plt.savefig(outpng, dpi=300)
        if noshow == False:
            plt.show()

    def draw_corr_bio3d(
        self, corr_matrix: np.ndarray, outpng: str, noshow: bool = False
    ) -> None:
        lis = [
            "#FF80FF",
            "#FFA8FF",
            "#FFD4FF",
            "#FFFCFF",
            "#FFFCFF",
            "#D4FFFF",
            "#A8FFFF",
            "#80FFFF",
        ]
        cm = colors.ListedColormap(lis)
        plt.clf()
        im = plt.contourf(corr_matrix, cmap=cm)
        plt.contour(
            corr_matrix,
            linewidths=0.2,
            levels=[-1.00, -0.75, -0.50, -0.25, 0.25, 0.50, 0.75, 1.00],
        )
        cb = plt.colorbar(im)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        if outpng != None:
            if os.path.exists(outpng):
                logging.error("{} already in current directory".format(outpng))
                sys.exit()
            plt.savefig(outpng, dpi=300)
        if noshow == False:
            plt.show()

    def draw(
        self,
        corr_matrix: np.ndarray,
        mode: str = "bio3d",
        noshow: bool = False,
        outpng: str = None,
    ) -> None:
        if mode == "bio3d":
            self.draw_corr_bio3d(corr_matrix, outpng, noshow)
        elif mode == "gaussian":
            self.draw_corr_gaussian(corr_matrix, outpng, noshow)
        else:
            self.draw_corr_origin(corr_matrix, outpng, noshow)


def dccm_from_ascii(datfile: str, mode, noshow, outpng, xlabel, ylabel, title) -> None:
    dccm = DCCM()
    dccm.xlabel = xlabel
    dccm.ylabel = ylabel
    dccm.title = title
    covar_matrix = dccm.read_acsii(datfile)
    corr_matrix = dccm.covar2corr(covar_matrix)
    dccm.draw(corr_matrix, mode, noshow, outpng)


def dccm_call_functions(arguments: list = None):
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]

    ## parse the command parameters
    parser = argparse.ArgumentParser(description="generate mdp file templates")
    parser.add_argument("-f", "--input", help="specify the input file")
    parser.add_argument("-o", "--output", help="file name to output")
    parser.add_argument(
        "-m",
        "--mode",
        default="bio3d",
        help="specify the figure style, 'origin', 'gaussian', 'bio3d'",
    )
    parser.add_argument(
        "-ns", "--noshow", default=False, help="whether not to show figure"
    )
    parser.add_argument(
        "-x", "--xlabel", default="Residue No.", help="specify the xlabel"
    )
    parser.add_argument(
        "-y", "--ylabel", default="Residue No.", help="specify the ylabel"
    )
    parser.add_argument(
        "-t",
        "--title",
        default="Dynamic Cross Correlation Matrix",
        help="specify the title of figure",
    )

    if len(arguments) < 2:
        logging.error("no input parameters, -h or --help for help messages")
        sys.exit()
    method = arguments[1]
    if method in ["-h", "--help"]:
        parser.parse_args(arguments[1:])
        sys.exit()

    args = parser.parse_args(arguments[2:])
    if method == "dccm_ascii":
        dccm_from_ascii(
            args.input,
            args.mode,
            args.noshow,
            args.output,
            args.xlabel,
            args.ylabel,
            args.title,
        )
    else:
        logging.error("unknown method {}".format(method))
        sys.exit()

    logging.info("May you good day !")


def main():
    dccm_call_functions()


if __name__ == "__main__":
    main()
