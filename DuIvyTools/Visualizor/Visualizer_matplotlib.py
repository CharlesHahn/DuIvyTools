"""
Visualizer_matplotlib module is part of DuIvyTools providing basic visualization tools based on matplotlib.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors as mplcolors
from matplotlib.ticker import AutoLocator, FormatStrFormatter

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class ParentMatplotlib(log):
    def __init__(self):
        self.figure = plt.figure()
        self.load_style()

    def load_style(self):
        style_files = [file for file in os.listdir() if file[-9:] == ".mplstyle"]
        if len(style_files) == 1:
            plt.style.use(style_files[0])
            self.info(f"using matplotlib style sheet from {style_files[0]}")
        elif len(style_files) > 1:
            plt.style.use(style_files[0])
            self.info(
                f"more than one mplstyle files detected, using the {style_files[0]}"
            )
        else:
            data_file_path = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__), "../")
            )
            mplstyle = os.path.join(
                data_file_path, os.path.join("data", "DIT.mplstyle")
            )
            plt.style.use(mplstyle)
            self.info(
                "using default matplotlib style sheet, to inspect its content, use 'dit show_style'"
            )

    def final(self, outfig: str, noshow: bool) -> None:

        plt.tight_layout()
        if outfig != None:
            if os.path.exists(outfig):
                time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())
                new_outfig = f'{".".join(outfig.split(".")[:-1])}_{time_info}.{outfig.split(".")[-1]}'
                self.warn(
                    f"{outfig} is already in current directory, save to {new_outfig} for instead."
                )
                outfig = new_outfig
            self.figure.savefig(outfig)
            self.info(f"save figure to {outfig} successfully")
        if noshow == False:
            plt.show()


class LineMatplotlib(ParentMatplotlib):
    """A matplotlib line plot class for line plots

    Args:
        ParentMatplotlib (object): matplotlib parent class

    Parameters:
        data_list :List[List[float]]
        xdata :List[float]
        legends :List[str]
        xmin :float
        xmax :flaot
        ymin :float
        ymax :float
        xlabel :str
        ylabel :str
        title :str
        x_precision :int
        y_precision :int
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        for i, data in enumerate(kwargs["data_list"]):
            plt.plot(kwargs["xdata"], data, label=kwargs["legends"][i])

        x_min, x_max = np.min(kwargs["xdata"]), np.max(kwargs["xdata"])
        if kwargs["xmin"] == None and kwargs["xmax"] == None:
            x_space = int((x_max - x_min) / 100)
            if int(x_min - x_space) < int(x_max + x_space) - 1.0:
                plt.xlim(int(x_min - x_space), int(x_max + x_space))
        else:
            plt.xlim(kwargs["xmin"], kwargs["xmax"])

        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            plt.ylim(kwargs["ymin"], kwargs["ymax"])

        ax = plt.gca()
        if kwargs["x_precision"] != None:
            x_p = kwargs["x_precision"]
            ax.xaxis.set_major_formatter(FormatStrFormatter(f"%.{x_p}f"))
        if kwargs["y_precision"] != None:
            y_p = kwargs["y_precision"]
            ax.yaxis.set_major_formatter(FormatStrFormatter(f"%.{y_p}f"))

        plt.legend()
        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])
        plt.title(kwargs["title"])


class DistributionMatplotlib(ParentMatplotlib):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class StackMatplotlib(ParentMatplotlib):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ScatterMatplotlib(ParentMatplotlib):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BarMatplotlib(ParentMatplotlib):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BoxMatplotlib(ParentMatplotlib):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ViolinMatplotlib(ParentMatplotlib):
    def __init__(self, **kwargs) -> None:
        super().__init__()
