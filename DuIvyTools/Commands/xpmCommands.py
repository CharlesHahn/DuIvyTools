"""
xpmCommander module is part of DuIvyTools providing xpm related commands.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union
from scipy.interpolate import interp2d, RectBivariateSpline

from Commands.Commands import Command
from FileParser.xpmParser import XPM, XPMS
from Visualizor.Visualizer_matplotlib import *
from Visualizor.Visualizer_plotext import *
from Visualizor.Visualizer_plotly import *
from Visualizor.Visualizer_gnuplot import *
from utils import Parameters


class xpm_show(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def calc_interpolation(
        self,
        xaxis: List[float],
        yaxis: List[float],
        matrix: List[List[float]],
        method: str,
        ip_fold: int,
    ) -> Union[List[float], List[List[float]]]:
        # interp2d : linear, cubic, quintic
        ip_func = interp2d(xaxis, yaxis, matrix, kind=method)
        # ip_func = RectBivariateSpline(xaxis, yaxis, matrix)#, kx=3, ky=3)
        x_new = np.linspace(np.min(xaxis), np.max(xaxis), ip_fold * len(xaxis))
        y_new = np.linspace(np.min(yaxis), np.max(yaxis), ip_fold * len(yaxis))
        matrix_new = ip_func(x_new, y_new)
        x_new_mg, y_new_mg = np.meshgrid(x_new, y_new)
        return x_new_mg, y_new_mg, matrix_new, x_new, y_new

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        res = tuple(int(value[i:i+2], 16) for i in (0, 2, 4))
        return res

    def __call__(self):  ## write process code

        self.info("in xpm_show")
        print(self.parm.__dict__)

        if not self.parm.input:
            self.error("you must specify a xpm file to show")

        # notes of mode: imshow, pcm, 3d, contour

        # IP for imshow: None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos'

        for xpmfile in self.parm.input:
            xpm = XPM(xpmfile)
            self.file = xpm
            self.remove_latex(filetype="XPM")

            xaxis = [x * self.parm.xshrink for x in xpm.xaxis]
            yaxis = [y * self.parm.yshrink for y in xpm.yaxis]
            value_matrix = []
            for y, _ in enumerate(yaxis):
                v_lis = []
                for x, _ in enumerate(xaxis):
                    v_lis.append(xpm.value_matrix[y][x] * self.parm.zshrink)
                value_matrix.append(v_lis)

            kwargs = {
                "data_list": value_matrix,
                "xdata_list": xaxis,
                "ydata_list": yaxis,
                "legends": self.sel_parm(self.parm.legends, xpm.notes),
                "color_list": xpm.colors,
                "xmin": self.parm.xmin,
                "xmax": self.parm.xmax,
                "ymin": self.parm.ymin,
                "ymax": self.parm.ymax,
                "xlabel": self.get_parm("xlabel"),
                "ylabel": self.get_parm("ylabel"),
                "zlabel": self.sel_parm(self.parm.zlabel, xpm.legend),
                "title": self.get_parm("title"),
                "x_precision": self.parm.x_precision,
                "y_precision": self.parm.y_precision,
                "z_precision": self.parm.z_precision,
                "alpha": self.parm.alpha,
                "legend_location": self.sel_parm(self.parm.legend_location, "outside"),
                "colorbar_location": self.parm.colorbar_location,
                "fig_type": xpm.type,
                "cmap": self.parm.colormap,
            }

            interpolation = self.parm.interpolation
            ip_fold = self.parm.interpolation_fold
            mode = self.parm.mode

            if self.parm.engine == "matplotlib":
                if mode in ["pcolormesh", "3d", "contour"]:
                    if interpolation != None:
                        if self.file.type != "Continuous":
                            self.warn(f"you are applying interpolation to {self.file.type} type of XPM. It should not be, but DIT would do it. BE CAREFUL for what you get !")
                        xaxis, yaxis, value_matrix, _, _ = self.calc_interpolation(xaxis, yaxis, value_matrix, interpolation, ip_fold)
                        kwargs["xdata_list"] = xaxis
                        kwargs["ydata_list"] = yaxis
                        kwargs["data_list"] = value_matrix
                    else:
                        xaxis, yaxis = np.meshgrid(xaxis, yaxis)
                        kwargs["xdata_list"] = np.array(xaxis)
                        kwargs["ydata_list"] = np.array(yaxis)
                        kwargs["data_list"] = np.array(kwargs["data_list"])
                if mode == "pcolormesh":
                    fig = PcolormeshMatplotlib(**kwargs)
                    fig.final(self.parm.output, self.parm.noshow)
                elif mode == "3d":
                    fig = ThreeDimensionMatplotlib(**kwargs)
                    fig.final(self.parm.output, self.parm.noshow)
                elif mode == "contour":
                    fig = ContourMatplotlib(**kwargs)
                    fig.final(self.parm.output, self.parm.noshow)
                else:
                    kwargs["interpolation"] = interpolation
                    fig = ImshowMatplotlib(**kwargs)
                    fig.final(self.parm.output, self.parm.noshow)

            elif self.parm.engine == "plotly":
                if interpolation != None:
                    if self.file.type != "Continuous":
                        self.warn(f"you are applying interpolation to {self.file.type} type of XPM. It should not be, but DIT would do it. BE CAREFUL for what you get !")
                    _, _, value_matrix, xaxis, yaxis = self.calc_interpolation(xaxis, yaxis, value_matrix, interpolation, ip_fold)
                    kwargs["xdata_list"] = xaxis
                    kwargs["ydata_list"] = yaxis
                    kwargs["data_list"] = value_matrix
                if mode == "3d":
                    fig = ThreeDimensionPlotly(**kwargs)
                    fig.final(self.parm.output, self.parm.noshow)
                elif mode == "contour":
                    fig = ContourPlotly(**kwargs)
                    fig.final(self.parm.output, self.parm.noshow)
                else:
                    fig = PcolormeshPlotly(**kwargs)
                    fig.final(self.parm.output, self.parm.noshow)
            
            elif self.parm.engine == "gnuplot":
                if interpolation != None:
                    if self.file.type != "Continuous":
                        self.warn(f"you are applying interpolation to {self.file.type} type of XPM. It should not be, but DIT would do it. BE CAREFUL for what you get !")
                    _, _, value_matrix, xaxis, yaxis = self.calc_interpolation(xaxis, yaxis, value_matrix, interpolation, ip_fold)
                    kwargs["xdata_list"] = xaxis
                    kwargs["ydata_list"] = yaxis
                    kwargs["data_list"] = value_matrix
                if mode not in ["3d", "contour"]:
                    mode = "imshow"
                fig = ImshowGnuplot(mode, **kwargs)
                fig.final(self.parm.output, self.parm.noshow)

            elif self.parm.engine == "plotext":
                if interpolation != None:
                    self.warn("plotext engine do not support interpolation now, ignored it")
                color_matrix = []
                for y, _ in enumerate(yaxis):
                    c_lis = []
                    for x, _ in enumerate(xaxis):
                        c = xpm.colors[xpm.chars.index(xpm.dot_matrix[y][x])]
                        c_lis.append(self.hex_to_rgb(c))
                    color_matrix.append(c_lis)
                kwargs["data_list"] = color_matrix
                ImshowPlotext(**kwargs)
            else:
                self.error("wrong selection of plot engine")


class xpm2csv(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xpm2csv")
        print(self.parm.__dict__)

        if not self.parm.input:
            self.error("you must specify a xpm file for converting to csv file")
        if len(self.parm.input) > 1:
            self.warn("only the first xpm file you specified will be used !")
        if not self.parm.output:
            self.error("you must specify a csv file to store results")
        self.parm.output = self.check_output_exist(self.parm.output)

        xpm = XPM(self.parm.input[0])
        with open(self.parm.output, "w") as fo:
            if xpm.type != "Continuous":
                fo.write("#### DIT: it's not a Continuous type xpm file\n")
                fo.write("#### labels of values were recorded below: \n")
                for index, label in enumerate(xpm.notes):
                    fo.write(f"#### {index} : {label}\n")
            x_title = (xpm.xlabel, "x-axis")[len(xpm.xlabel) == 0]
            y_title = (xpm.ylabel, "y-axis")[len(xpm.ylabel) == 0]
            z_title = (xpm.legend, "value")[len(xpm.legend) == 0]
            x_title = self.sel_parm(self.parm.xlabel, x_title)
            y_title = self.sel_parm(self.parm.ylabel, y_title)
            z_title = self.sel_parm(self.parm.zlabel, z_title)
            fo.write(f"{x_title},{y_title},{z_title}\n")
            for y, y_value in enumerate(xpm.yaxis):
                for x, x_value in enumerate(xpm.xaxis):
                    z_value = xpm.value_matrix[y][x]
                    x_value *= self.parm.xshrink
                    y_value *= self.parm.yshrink
                    z_value *= self.parm.zshrink
                    fo.write(f"{x_value:.6f},{y_value:.6f},{z_value:.6f}\n")
        self.info(
            f"extract data from {xpm.xpmfile} and saved into {self.parm.output} successfully"
        )


class xpm2dat(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xpm2dat")
        print(self.parm.__dict__)

        if not self.parm.input:
            self.error("you must specify a xpm file for converting to dat file")
        if len(self.parm.input) > 1:
            self.warn("only the first xpm file you specified will be used !")
        if not self.parm.output:
            self.error("you must specify a dat file to store results")
        self.parm.output = self.check_output_exist(self.parm.output)

        xpm = XPM(self.parm.input[0])
        with open(self.parm.output, "w") as fo:
            if xpm.type != "Continuous":
                fo.write("#### DIT: it's not a Continuous type xpm file\n")
                fo.write("#### labels of values were recorded below: \n")
                for index, label in enumerate(xpm.notes):
                    fo.write(f"#### {index} : {label}\n")
            x_title = (xpm.xlabel, "x-axis")[len(xpm.xlabel) == 0]
            y_title = (xpm.ylabel, "y-axis")[len(xpm.ylabel) == 0]
            z_title = (xpm.legend, "value")[len(xpm.legend) == 0]
            x_title = self.sel_parm(self.parm.xlabel, x_title)
            y_title = self.sel_parm(self.parm.ylabel, y_title)
            z_title = self.sel_parm(self.parm.zlabel, z_title)
            fo.write(
                "#### "
                + f"{x_title} (xaxis) data were shown below, from left to right:\n"
            )
            fo.write(",".join([f"{x*self.parm.xshrink:.6f}" for x in xpm.xaxis]) + "\n")
            fo.write(
                "#### "
                + f"{y_title} (yaxis) data were shown below, from top to bottom:\n"
            )
            fo.write(",".join([f"{y*self.parm.yshrink:.6f}" for y in xpm.yaxis]) + "\n")
            fo.write(
                "#### "
                + f"{y_title} (yaxis) data were shown below, from bottom to top:\n"
            )
            y_lis = [f"{y*self.parm.yshrink:.6f}" for y in xpm.yaxis]
            y_lis.reverse()
            fo.write(",".join(y_lis) + "\n")
            fo.write(
                "#### "
                + f"{z_title} (figure dots) data were shown below, from top to bottom, from left to right:\n"
            )
            for y, _ in enumerate(xpm.yaxis):
                line_list: List[str] = []
                for x, _ in enumerate(xpm.xaxis):
                    z_value = xpm.value_matrix[y][x]
                    line_list.append(f"{z_value*self.parm.zshrink:.6f}")
                fo.write(",".join(line_list) + "\n")
        self.info(
            f"extract data from {xpm.xpmfile} and saved into {self.parm.output} successfully"
        )


class xpm_diff(Command):
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xpm_diff")
        print(self.parm.__dict__)


class xpm_merge(Command): # TODO: merge two xpm half by half
    def __init__(self, parm: Parameters) -> None:
        self.parm = parm

    def __call__(self):
        self.info("in xpm_diff")
        print(self.parm.__dict__)
