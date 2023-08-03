"""
Visualizer_plotext module is part of DuIvyTools providing visualization tools based on plotext engine.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union, Tuple

import numpy as np
import plotext as plt

from utils import log


class ParentPlotext(log):
    def __init__(self) -> None:
        plt.clear_figure()
        self.style = {
            "color_cycle": [
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
        }

    def hex2rgb(self, hex: str) -> Tuple[float]:
        rgb = [int(hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)]
        return tuple(rgb)

    def final(self, outfig: str, noshow: bool) -> None:
        if outfig != None:
            self.info(f"unable to save figure with plotext engine\n")
        plt.show()


class LinePlotext(ParentPlotext):
    """A plotext line plot class for line plots

    Args:
        ParentPlotext (object): plotext parent class

    Parameters:
        data_list :List[List[float]]
        xdata_list :List[List[[float]]
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
        # optional
        highs :List[List[float]]
        lows :List[List[float]]
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        for i, data in enumerate(kwargs["data_list"]):
            if len(kwargs["highs"]) != 0 and len(kwargs["lows"]) != 0:
                self.warn("unable to plot confidence intervals by plotext.")
            # plt.plot(kwargs["xdata"], data, label=kwargs["legends"][i], color=self.hex2rgb(self.style["color_cycle"][i]))
            plt.plot(kwargs["xdata_list"][i], data, label=kwargs["legends"][i])

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
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


class StackPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ScatterPlotext(ParentPlotext):
    """A plotext scatter plot class for scatter plots

    Args:
        ParentPlotext (object): plotext parent class

    Parameters:
        data_list :List[List[float]]
        xdata_list :List[List[float]]
        color_list :List[List[float]]
        legends :List[str]
        xmin :float
        xmax :flaot
        ymin :float
        ymax :float
        zmin :float
        zmax :float
        xlabel :str
        ylabel :str
        zlabel :str
        title :str
        x_precision :int
        y_precision :int
        z_precision :int
        cmap :str
        colorbar_location:str
    """
    def __init__(self, **kwargs) -> None:
        super().__init__()

        for i, data in enumerate(kwargs["data_list"]):
            plt.scatter(kwargs["xdata_list"][i], data, label=kwargs["legends"][i], color=kwargs["color_list"])

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
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
        
        for key in ["cmap", "colorbar_location", "z_precision", "zlabel", "color_list"]:
            if kwargs[key]:
                self.warn(f"{key} is not valid for plotext engine")


class BarPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BoxPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ViolinPlotext(ParentPlotext):
    def __init__(self, **kwargs) -> None:
        super().__init__()
