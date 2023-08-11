"""
utils module is part of DuIvyTools. This module provides log parent class.

Written by DuIvy and provided to you by GPLv3 license.
"""

import sys
import time
import logging
import argparse
from colorama import Fore, Back, Style

from typing import List


class log(object):
    """log class, a logging system parent class, provied five functions for
    output debug, info, warning, error, and critical messages.
    """

    logging.basicConfig(
        level=logging.INFO,
        ## TODO the line number
        ## format="%(asctime)s-%(filename)s[line:%(lineno)d]\n%(message)s",
        format="%(message)s",
    )
    logger = logging.getLogger(__name__)

    def debug(self, msg):
        time_info = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger.debug(
            Fore.CYAN + Back.WHITE + f"{time_info}\nDebug -> {msg}" + Style.RESET_ALL
        )

    def info(self, msg):
        time_info = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger.info(Fore.GREEN + f"{time_info}\nInfo -> {msg}" + Style.RESET_ALL)

    def warn(self, msg):
        time_info = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger.warning(
            Fore.YELLOW + f"{time_info}\nWarning -> {msg}" + Style.RESET_ALL
        )

    def error(self, msg):
        time_info = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger.error(
            Fore.WHITE + Back.RED + f"{time_info}\nError -> {msg}" + Style.RESET_ALL
        )
        sys.exit()

    def critical(self, msg):
        time_info = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.logger.critical(
            Fore.WHITE + Back.RED + f"{time_info}\nCRITICAL -> {msg}" + Style.RESET_ALL
        )
        sys.exit()


class Parameters(log):
    def __init__(self) -> None:

        parser = argparse.ArgumentParser(
            description="DuIvyTools: A Simple MD Analysis Tool"
        )
        parser.add_argument("cmd", type=str, help="command of DIT")

        parser.add_argument(
            "-f", "--input", nargs="+", help="specify the input file or files"
        )
        parser.add_argument("-o", "--output", type=str, help="specify the output file")
        parser.add_argument(
            "-ns", "--noshow", action="store_true", help="not to show figure"
        )
        parser.add_argument(
            "-c", "--columns", nargs="+", help="select column indexs for visualization"
        )
        parser.add_argument(
            "-l", "--legends", nargs="+", help="legends you wanna specify"
        )
        parser.add_argument(
            "-b", "--begin", type=int, help="specify the index beginning (include)"
        )
        parser.add_argument(
            "-e", "--end", type=int, help="specify the index ending (not include)"
        )
        parser.add_argument(
            "-dt",
            "--dt",
            type=int,
            default=1,
            help="specify the index step, default to 1",
        )
        parser.add_argument(
            "-x", "--xlabel", type=str, help="specify the xlabel of figure"
        )
        parser.add_argument(
            "-y", "--ylabel", type=str, help="specify the ylabel of figure"
        )
        parser.add_argument(
            "-z", "--zlabel", type=str, help="specify the zlabel of figure"
        )
        parser.add_argument(
            "-t", "--title", type=str, help="specify the title of figure"
        )
        parser.add_argument(
            "-xmin", "--xmin", type=float, help="specify the X value limitation, x_min"
        )
        parser.add_argument(
            "-xmax", "--xmax", type=float, help="specify the X value limitation, x_max"
        )
        parser.add_argument(
            "-ymin", "--ymin", type=float, help="specify the Y value limitation, y_min"
        )
        parser.add_argument(
            "-ymax", "--ymax", type=float, help="specify the Y value limitation, y_max"
        )
        parser.add_argument(
            "-zmin", "--zmin", type=float, help="specify the Z value limitation, z_min"
        )
        parser.add_argument(
            "-zmax", "--zmax", type=float, help="specify the Z value limitation, z_max"
        )
        parser.add_argument(
            "--x_precision",
            type=int,
            help="specify the precision of x values",
        )
        parser.add_argument(
            "--y_precision",
            type=int,
            help="specify the precision of y values",
        )
        parser.add_argument(
            "--z_precision",
            type=int,
            help="specify the precision of z values",
        )
        parser.add_argument(
            "-xs",
            "--xshrink",
            type=float,
            default=1.0,
            help="modify x values by multipling xshrink",
        )
        parser.add_argument(
            "-ys",
            "--yshrink",
            type=float,
            default=1.0,
            help="modify y values by multipling yshrink",
        )
        parser.add_argument(
            "-zs",
            "--zshrink",
            type=float,
            default=1.0,
            help="modify z values by multipling zshrink",
        )
        parser.add_argument(
            "-smv",
            "--showMV",
            action="store_true",
            help="whether to show moving average",
        )
        parser.add_argument(
            "-ws",
            "--windowsize",
            type=int,
            default=50,
            help="window size for moving average calculation",
        )
        parser.add_argument(
            "-cf",
            "--confidence",
            type=float,
            default=0.95,
            help="confidence for confidence interval calculation",
        )
        parser.add_argument(
            "--alpha", type=float, help="the alpha of background lines"
        )
        parser.add_argument("-csv", "--csv", help="store data into csv file")
        parser.add_argument(
            "-eg",
            "--engine",
            type=str,
            default="matplotlib",
            choices=["matplotlib", "plotext", "plotly", "gnuplot"],
            help="specify the engine for plotting, 'matplotlib', 'plotext', 'plotly', 'gnuplot'",
        )
        parser.add_argument(
            "-cmap",
            "--colormap",
            help="specify the figure style, 'origin', 'gaussian', 'bio3d'",
        )
        parser.add_argument(
            "-bin",
            "--bin",
            type=int,
            default=100,
            help="the bin number for distribution calculation",
        )
        parser.add_argument(
            "--colorbar_location",
            type=str,
            default=None,
            choices=[None, "left", "top", "bottom", "right"],
            help="the location of colorbar, also determining the orientation of colorbar",
        )
        parser.add_argument(
            "--legend_location",
            type=str,
            default=None,
            choices=["inside", "outside"],
            help="the location of legend box",
        )
        parser.add_argument(
            "--mode",
            type=str,
            choices=[None, "withoutScatter", "pcolormesh", "3d", "contour"],
            help="additional parameter: withoutScatter will NOT show scatter plot for xvg_box_compare; imshow, pcolormesh, 3d, contour were used for xpm_show command",
        )
        parser.add_argument(
            "-al", "--additional_list", nargs="+", help="additional parameters"
        )
        parser.add_argument(
            "-ip",
            "--interpolation",
            type=str,
            default=None,
            help="specify the interpolation method",
        )
        parser.add_argument(
            "--interpolation_fold",
            type=int,
            default=10,
            help="specify the interpolation fold",
        )
        ## TODO: when mode, show choices of ip methods

        """
        parser.add_argument(
            "-3d",
            "--threeDimensions",
            action="store_true",
            help="whether to draw 3D figure",
        )

        ## TODO think twice
        parser.add_argument(
            "-pcm",
            "--pcolormesh",
            action="store_true",
            help="whether to apply pcolormesh function to draw",
        )

        parser.add_argument(
            "-gl", "--grouplist", nargs="+", help="specify a list of group names"
        )
        parser.add_argument(
            "-int",
            "--interactive",
            action="store_true",
            help="whether to initiate interactive mode",
        )
        parser.add_argument(
            "-gn", "--groupname", type=str, help="specify the group name"
        )
        parser.add_argument(
            "-on", "--oldname", type=str, help="specify the old group name"
        )
        parser.add_argument(
            "-nn", "--newname", type=str, help="specify the new group name"
        )
        parser.add_argument(
            "-a",
            "--application",
            choices=["ions", "em", "nvt", "npt", "md", "blank"],
            help="specify the application of mdp, choices: ions, em, nvt, npt, md, blank",
        )
        parser.add_argument("-n", "--index", help="index file")
        parser.add_argument(
            "-vg", action="store_true", help="whether to get vector by index group"
        )
        parser.add_argument(
            "-vec", nargs=3, type=float, help="get vector by your input, eg. -vec 6 6 6"
        )
        parser.add_argument(
            "-select", nargs="*", help="select the groups, eg. -select ring1 ring2"
        )
        parser.add_argument(
            "-aa",
            "--AllAtoms",
            action="store_true",
            help="if to find center in all atoms of gro file",
        )
        parser.add_argument("-m", "--map", help="hbond map file for input")
        parser.add_argument(
            "-hnf",
            "--hbond_name_format",
            help="define the hbond name format by user! Each atom has four"
            + " features: resname, resnum, atomname, atomnum. Distinguish "
            + "donor, hydrogen, acceptor by adding one prefix to each feature,"
            + " like: d_resname, a_resnum, h_atomname. \nSo you may able to "
            + "define hbond name style by: 'd_resname(d_resnum)@d_atomname(d_"
            + "atomnum)->h_atomname(h_atomnum)...a_resname(a_resnum)@a_atomn"
            + "ame(a_atomnum)' which is the default style,  or also you could"
            + " specify 'd_atomname@h_atomname...a_atomname' or some format you "
            + "would like. \nOr you could just set the hnf to be 'number' or 'id'",
        )
        parser.add_argument(
            "-genscript",
            "--genscript",
            action="store_true",
            help="whether to generate scripts for calculating distance and angle of hbonds",
        )
        parser.add_argument(
            "-cda",
            "--calc_distance_angle",
            action="store_true",
            help="whether to calculate distance and angle of hbonds from distance xvg file and angle xvg file",
        )
        parser.add_argument(
            "-distancefile", "--distancefile", help="distance file of hbonds for input"
        )
        parser.add_argument(
            "-anglefile", "--anglefile", help="angle file of hbonds for input"
        )
        parser.add_argument(
            "-so",
            "--set_operation",
            type=str,
            help="use AND or OR to operate different hbonds. eg. -so AND1-2,4,7  -so OR0,4,6-8",
        )
        """

        args = parser.parse_args()
        self.__dict__ = args.__dict__
        self.__check_convert()

    def __check_convert(self) -> None:

        ## deal parameters
        if self.input != None and "," in "".join(self.input):
            self.input = [fs.strip(",").split(",") for fs in self.input]

        column_select = []
        if self.columns != None:
            if "," in "".join(self.columns):
                for columns in self.columns:
                    lis: List[int] = []
                    for c in columns.strip(",").split(","):
                        if "-" in c.strip("-"):
                            b, e = int(c.split("-")[0]), int(c.split("-")[1])
                            lis += [i for i in range(b, e)]
                        else:
                            lis.append(int(c))
                    column_select.append(lis)
            else:
                column_select = [int(c) for c in self.columns]
            self.columns = column_select

        if self.legends != None and "," in "".join(self.legends):
            self.legends = [ls.strip(",").split(",") for ls in self.legends]

        ## TODO: check the range of parameters
        if self.begin and self.begin < 0:
            self.error("parameter 'begin' should not be a minus")
        if self.end and self.end < 0:
            self.error("parameter 'end' should not be a minus")
        if self.x_precision and self.x_precision < 0:
            self.error("parameter 'x_precision' should not be a minus")
        if self.y_precision and self.y_precision < 0:
            self.error("parameter 'y_precision' should not be a minus")
        if self.z_precision and self.z_precision < 0:
            self.error("parameter 'z_precision' should not be a minus")
