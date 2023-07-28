"""
Visualizer_plotext module is part of DuIvyTools providing visualization tools based on plotext engine.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

import numpy as np
import plotext as plt

from utils import log


class ParentPlotext(log):
    def __init__(self) -> None:
        plt.clear_figure()

    def final(self, outfig: str, noshow: bool) -> None:
        if outfig != None:
            if os.path.exists(outfig):
                time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())
                new_outfig = f'{".".join(outfig.split(".")[:-1])}_{time_info}.{outfig.split(".")[-1]}'
                self.warn(
                    f"{outfig} is already in current directory, save to {new_outfig} for instead."
                )
                outfig = new_outfig
            outfig = os.path.join(os.getcwd(), outfig)
            plt.save_fig(outfig)
            self.info(f"save figure to {outfig} successfully")
        if noshow == False:
            plt.show()


class LinePlotext(ParentPlotext):
    """A plotext line plot class for line plots

    Args:
        ParentPlotext (object): plotext parent class

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

        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])
        plt.title(kwargs["title"])

        if kwargs["x_precision"] != None:
            self.warn("unable to apply x_precision to plotext engine")
        if kwargs["y_precision"] != None:
            self.warn("unable to apply y_precision to plotext engine")


class DistributionPlotexet(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class StackPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ScatterPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BarPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BoxPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ViolinPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()
