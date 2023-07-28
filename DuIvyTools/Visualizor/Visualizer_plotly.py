"""
Visualizer_plotly module is part of DuIvyTools providing basic visualization tools based on plotly.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

import numpy as np
import pandas as pd

import plotly.express as plt
import plotly.graph_objs as go

from utils import log


class ParentPlotly(log):
    def __init__(self):
        self.figure = go.Figure()

    def final(self, outfig: str, noshow: bool) -> None:
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
            self.figure.show()


class LinePlotly(ParentPlotly):
    """A plotly line plot class for line plots

    Args:
        Parentplotly (object): plotly parent class

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
            self.figure.add_trace(
                go.Scatter(x=kwargs["xdata"], y=data, name=kwargs["legends"][i])
            )
        self.figure.update_layout(
            title=kwargs["title"],
            xaxis_title=kwargs["xlabel"],
            yaxis_title=kwargs["ylabel"],
            font=dict(family="Arial, Times New Roman", size=18),
            showlegend=True,
        )
        if kwargs["xmin"] != None or kwargs["xmax"] != None:
            self.figure.update_layout(xaxis_range=[kwargs["xmin"], kwargs["xmax"]])
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.figure.update_layout(yaxis_range=[kwargs["ymin"], kwargs["ymax"]])
        if kwargs["x_precision"] != None:
            self.figure.update_layout(xaxis_tickformat=f".{kwargs['x_precision']}f")
        if kwargs["y_precision"] != None:
            self.figure.update_layout(yaxis_tickformat=f".{kwargs['y_precision']}f")


class DistributionPlotly(ParentPlotly):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class StackPlotly(ParentPlotly):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ScatterPlotly(ParentPlotly):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BarPlotly(ParentPlotly):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BoxPlotly(ParentPlotly):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ViolinPlotly(ParentPlotly):
    def __init__(self, **kwargs) -> None:
        super().__init__()
