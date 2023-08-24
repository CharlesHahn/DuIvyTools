"""
Visualizer_plotly module is part of DuIvyTools providing basic visualization tools based on plotly.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import json
from typing import Tuple

import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

from utils import log


class ParentPlotly(log):
    """parent class of plotly visualizer class"""

    def __init__(self):
        self.load_themes()
        self.templates_name = "plotly"
        self.figure = go.Figure()
        self.nticks: int = 7  # for tick location by hand
    

    def get_color(self, id:int) -> str:
        # colorcycle is by colorway in templates
        colors = pio.templates[self.templates_name].layout.colorway
        id %= len(colors)
        return colors[id]


    def load_themes(self):
        ## TODO plotly theme and style file system
        # pio.templates.default = "seaborn"
        # print(pio.templates["plotly"].layout)

        # https://github.com/AnnMarieW/dash-bootstrap-templates/tree/main/src/dash_bootstrap_templates/templates

        # https://plotly.com/python/templates/#creating-themes

        data_file_path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__), "../")
        )
        folder = os.path.join(
            data_file_path, os.path.join("data", "plotly_templates")
        )
        files = [f for f in os.listdir(folder) if f.endswith(".json")]
        for file in files:
            name = file[:-5]
            print(os.path.join(folder, file))
            path = os.path.join(folder, file)
            with open(path, 'r') as fo:
                template = json.load(fo)
            pio.templates[name] = template
            print(name)

        # pio.templates.default = "bootstrap"
        pio.templates.default = "DIT"
        self.templates_name = "DIT"

    def hex2rgb(self, hex: str) -> Tuple[float]:
        rgb = [int(hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)]
        return tuple(rgb)

    def final(self, outfig: str, noshow: bool) -> None:
        """do final process of drawing figure with plotly

        Args:
            outfig (str): the user specified output figure name
            noshow (bool): True for no display the figure
        """
        if outfig != None:
            self.warn("unable to save figure by DIT, please save figure by yourself")
        if noshow == False:
            self.figure.show()

    def set_xyprecision_xyt_label(self, **kwargs) -> None:
        """set x_precision, y_precision, xlabel, ylabel, title"""
        self.figure.update_layout(
            legend_orientation="h",
            title=kwargs["title"],
            xaxis_title=kwargs["xlabel"],
            yaxis_title=kwargs["ylabel"],
            font=dict(family="Arial, Times New Roman", size=18),
            showlegend=True,
        )
        if kwargs["x_precision"] != None:
            self.figure.update_layout(xaxis_tickformat=f".{kwargs['x_precision']}f")
        if kwargs["y_precision"] != None:
            self.figure.update_layout(yaxis_tickformat=f".{kwargs['y_precision']}f")

    def set_xytick_precision_xyt_label(self, **kwargs) -> None:
        """set Y tick, precision, Y tick, precision, xlabel, ylabel, title"""
        step = len(kwargs["xdata_list"]) // self.nticks
        step = [step, 1][step == 0]
        xdata_index = [i for i in range(0, len(kwargs["xdata_list"]), step)]
        step = len(kwargs["ydata_list"]) // self.nticks
        step = [step, 1][step == 0]
        ydata_index = [i for i in range(0, len(kwargs["ydata_list"]), step)]
        self.figure.update_xaxes(
            tickvals=xdata_index,
            ticktext=[
                f"{kwargs['xdata_list'][x]:.{kwargs['x_precision']}f}"
                for x in xdata_index
            ],
        )
        self.figure.update_yaxes(
            tickvals=ydata_index,
            ticktext=[
                f"{kwargs['ydata_list'][y]:.{kwargs['y_precision']}f}"
                for y in ydata_index
            ],
        )
        self.figure.update_layout(
            legend_orientation="h",
            title=kwargs["title"],
            xaxis_title=kwargs["xlabel"],
            yaxis_title=kwargs["ylabel"],
            font=dict(family="Arial, Times New Roman", size=18),
            showlegend=True,
        )

    def set_xy_min_max(self, **kwargs) -> None:
        """set xmin, xmax, ymin, ymax"""
        if kwargs["xmin"] != None or kwargs["xmax"] != None:
            self.figure.update_layout(xaxis_range=[kwargs["xmin"], kwargs["xmax"]])
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.figure.update_layout(yaxis_range=[kwargs["ymin"], kwargs["ymax"]])

    def check_repeat_values(self, values) -> bool:
        """True for repeat values exists in values"""
        if len(list(set(values))) < len(values):
            return True  # for repeat values
        else:
            return False

    def check_XY_repeat(self, **kwargs) -> bool:
        """True for repeat values exists in xdata_list or ydata_list"""
        if self.check_repeat_values(kwargs["xdata_list"]):
            return True
        if self.check_repeat_values(kwargs["ydata_list"]):
            return True
        return False


class LinePlotly(ParentPlotly):
    """A plotly line plot class for line plots

    Args:
        Parentplotly (object): plotly parent class

    Parameters:
        data_list :List[List[float]]
        xdata_list :List[List[float]]
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
        highs :List[List[float]]
        lows :List[List[float]]
        alpha :float
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        for i, data in enumerate(kwargs["data_list"]):
            self.figure.add_trace(
                go.Scatter(
                    x=kwargs["xdata_list"][i],
                    y=data,
                    name=kwargs["legends"][i],
                    line=dict(color=self.get_color(i)),
                    showlegend=(kwargs["legends"][i] != ""),
                )
            )
            if len(kwargs["highs"]) != 0 and len(kwargs["lows"]) != 0:
                rgb = self.hex2rgb(self.get_color(i))
                rgba = f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{kwargs['alpha']})"
                self.figure.add_trace(
                    go.Scatter(
                        name=f"""high-{kwargs["legends"][i]}""",
                        x=kwargs["xdata_list"][i],
                        y=kwargs["highs"][i],
                        line=dict(width=0, color=rgba),
                        showlegend=False,
                    )
                )
                self.figure.add_trace(
                    go.Scatter(
                        name=f"""low-{kwargs["legends"][i]}""",
                        x=kwargs["xdata_list"][i],
                        y=kwargs["lows"][i],
                        fillcolor=rgba,
                        fill="tonexty",
                        line=dict(width=0, color=rgba),
                        showlegend=False,
                    )
                )

        self.set_xyprecision_xyt_label(**kwargs)
        self.set_xy_min_max(**kwargs)


class StackPlotly(ParentPlotly):
    """A plotly line plot class for line plots

    Args:
        Parentplotly (object): plotly parent class

    Parameters:
        data_list :List[List[float]]
        xdata_list :List[List[float]]
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
        highs :List[List[float]]
        lows :List[List[float]]
        alpha :float
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        kwargs["data_list"].reverse()  # first in, show at bottom
        kwargs["legends"].reverse()  # reverse as data
        for i, data in enumerate(kwargs["data_list"]):
            rgb = self.hex2rgb(self.get_color(i))
            rgba = f"rgba({rgb[0]},{rgb[1]},{rgb[2]},{kwargs['alpha']})"
            self.figure.add_trace(
                go.Scatter(
                    x=kwargs["xdata_list"][i],
                    y=data,
                    name=kwargs["legends"][i],
                    showlegend=True,
                    stackgroup="stack",
                    fillcolor=rgba,
                    fill="tonexty",
                    line=dict(width=0, color=rgba),
                )
            )

        self.set_xyprecision_xyt_label(**kwargs)
        self.set_xy_min_max(**kwargs)


class ScatterPlotly(ParentPlotly):
    """A plotly scatter plot class for scatter plots

    Args:
        ParentPlotly (object): plotly parent class

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
        alpha
        cmap :str
        colorbar_location:str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        ## TODO: two or more list cause colorbar error
        for i, data in enumerate(kwargs["data_list"]):
            self.figure.add_trace(
                go.Scatter(
                    x=kwargs["xdata_list"][i],
                    y=data,
                    mode="markers",
                    name=kwargs["legends"][i],
                    showlegend=(len(kwargs["legends"]) > 1),
                    marker=dict(
                        colorbar={
                            "title": {"text": kwargs["zlabel"], "side": "right"},
                            "tickformat": f".{kwargs['z_precision']}f",
                            "lenmode": "fraction",
                            "len": 0.50,
                            "xanchor": "left",
                            "yanchor": "top",
                        },
                        opacity=kwargs["alpha"],
                        color=kwargs["color_list"][i],
                        colorscale=kwargs["cmap"],
                        symbol=i,
                        showscale=True,
                    ),
                )
            )
        if kwargs["colorbar_location"]:
            self.warn("colorbar_location parameter is not valid for plotly")

        self.set_xyprecision_xyt_label(**kwargs)
        self.set_xy_min_max(**kwargs)


class BarPlotly(ParentPlotly):
    """A plotly bar plot class for bar plots

    Args:
        ParentPlotly (object): matplotlib parent class

    Parameters:
        data_list :List[List[float]]
        stds_list :List[List[float]]
        xtitles :List[str]
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
        legend_location :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        for i, data in enumerate(kwargs["data_list"]):
            self.figure.add_trace(
                go.Bar(
                    x=[x for x in range(len(data))],
                    y=data,
                    name=kwargs["legends"][i],
                    error_y=dict(
                        type="data",
                        array=kwargs["stds_list"][i],
                        width=10,
                        visible=True,
                    ),
                )
            )
        self.figure.update_xaxes(
            tickvals=[i for i in range(len(kwargs["data_list"]))],
            ticktext=kwargs["xtitles"],
        )

        self.figure.update_layout(barmode="group")
        self.set_xyprecision_xyt_label(**kwargs)
        self.set_xy_min_max(**kwargs)


class BoxPlotly(ParentPlotly):
    """A plotly box plot class for box plots

    Args:
        ParentPlotly (object): Plotly parent class

    Parameters:
        data_list :List[List[float]]
        color_list :List[List[float]]
        legends :List[str]
        xmin :float
        xmax :flaot
        ymin :float
        ymax :float
        xlabel :str
        ylabel :str
        zlabel :str
        title :str
        x_precision :int
        y_precision :int
        z_precision :int
        alpha :float
        cmap :str
        colorbar_location:str
        mode :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        loc = 1.0
        if kwargs["mode"] != "withoutScatter":
            loc = 0.75
            for i, data in enumerate(kwargs["data_list"]):
                self.figure.add_trace(
                    go.Scatter(
                        x=np.random.normal(i + 1.25, 0.04, len(data)),
                        y=data,
                        mode="markers",
                        name=kwargs["legends"][i],
                        showlegend=(len(kwargs["legends"]) > 1),
                        marker=dict(
                            colorbar={
                                "title": {"text": kwargs["zlabel"], "side": "right"},
                                "tickformat": f".{kwargs['z_precision']}f",
                                "lenmode": "fraction",
                                "len": 0.50,
                                "xanchor": "left",
                                "yanchor": "top",
                            },
                            opacity=kwargs["alpha"],
                            color=kwargs["color_list"][i],
                            colorscale=kwargs["cmap"],
                            symbol=i,
                            showscale=True,
                        ),
                    )
                )

        for i, data in enumerate(kwargs["data_list"]):
            self.figure.add_trace(
                go.Violin(
                    x=[i + loc for _ in data],
                    y=data,
                    x0=kwargs["legends"][i],
                    box_visible=True,
                    meanline_visible=True,
                    showlegend=False,
                )
            )
        self.figure.update_xaxes(
            tickvals=[i + 1 for i in range(len(kwargs["data_list"]))],
            ticktext=kwargs["legends"],
        )
        if kwargs["colorbar_location"]:
            self.warn("colorbar_location parameter is not valid for plotly")

        self.set_xyprecision_xyt_label(**kwargs)
        self.set_xy_min_max(**kwargs)


class RamachandranPlotly(ParentPlotly):
    """A Plotly ramachandran plot class for ramachandran plots

    Args:
        ParentPlotly (object): plotly parent class

    Parameters:
        normals :Dict[Dict[List[float|str]]]
        outliers :Dict[Dict[List[float|str]]]
        rama_pref_values :List[List[float]]
        rama_preferences :Dict[Dict[str:str|List]]
        xlabel :str
        ylabel :str
        title :str
        outfig :str
        noshow :bool
    """

    def __init__(self, **kwargs) -> None:

        ## draw ramachandran plot
        normals = kwargs["normals"]
        outliers = kwargs["outliers"]
        rama_pref_values = kwargs["rama_pref_values"]
        rama_preferences = kwargs["rama_preferences"]
        outfig = kwargs["outfig"]
        noshow = kwargs["noshow"]
        for key in ["General", "GLY", "Pre-PRO", "PRO"]:
            self.figure = go.Figure()
            if len(normals[key]["phi"]) + len(outliers[key]["phi"]) == 0:
                continue
            bounds = rama_preferences[key]["bounds"]
            cmap = rama_preferences[key]["cmap"]
            colorscale = [[b, c] for b, c in zip(bounds, cmap)]
            colorscale += [[bounds[-1], cmap[-1]]]
            self.figure.add_trace(
                go.Heatmap(
                    x=[x - 180 for x in range(361)],
                    y=[y - 180 for y in range(361)],
                    z=rama_pref_values[key],
                    colorscale=colorscale,
                    showscale=False,
                    name="Probability",
                )
            )
            self.figure.add_trace(
                go.Scatter(
                    x=normals[key]["phi"],
                    y=normals[key]["psi"],
                    mode="markers",
                    name=f"normals (>{bounds[1]})",
                    hovertext=normals[key]["res"],
                    hoverinfo="text",
                    marker=dict(
                        color="#38A7D0",
                    ),
                )
            )
            self.figure.add_trace(
                go.Scatter(
                    x=outliers[key]["phi"],
                    y=outliers[key]["psi"],
                    mode="markers",
                    name=f"outliers (<{bounds[1]})",
                    hovertext=outliers[key]["res"],
                    hoverinfo="text",
                    marker=dict(
                        color="#F67088",
                    ),
                )
            )
            if kwargs["title"] == None:
                kwargs["title"] = key
            self.figure.update_layout(
                xaxis_range=[-180, 180],
                yaxis_range=[-180, 180],
            )
            self.set_xyprecision_xyt_label(**kwargs)

            if outfig != None:
                self.warn(
                    "unable to save figure by DIT, please save figure by yourself"
                )
            if noshow == False:
                self.figure.show()


class PcolormeshPlotly(ParentPlotly):
    """A plotly pcolormesh plot class for heatmap

    Args:
        ParentPlotly (object): plotly parent class

    Parameters:
        data_list :List[List[float]]
        xdata_list :List[float]
        ydata_list :List[float]
        legends :List[str]
        color_list :List[str]
        xlabel :str
        ylabel :str
        zlabel :str
        title :str
        x_precision :int
        y_precision :int
        z_precision :int
        colorbar_location :str
        cmap :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        ## TODO: using original colors, use user-defined?
        if kwargs["fig_type"] != "Continuous":
            colorscale, tickvals, length = [], [], len(kwargs["legends"])
            for i in range(length):
                colorscale.append([i / length, kwargs["color_list"][i]])
                colorscale.append([(i + 1) / length, kwargs["color_list"][i]])
            for i in range(length):
                tickvals.append((i + 0.5) / length * (length - 1))

            if not self.check_XY_repeat(**kwargs):
                self.figure.add_trace(
                    go.Heatmap(
                        x=kwargs["xdata_list"],
                        y=kwargs["ydata_list"],
                        z=kwargs["data_list"],
                        colorscale=colorscale,
                        showscale=True,
                        colorbar={
                            "title": {"text": kwargs["zlabel"], "side": "right"},
                            "ticktext": kwargs["legends"],
                            "tickvals": tickvals,
                            "lenmode": "fraction",
                            "len": 0.50,
                            "xanchor": "left",
                            "yanchor": "top",
                        },
                    )
                )
                self.set_xyprecision_xyt_label(**kwargs)
            else:
                self.figure.add_trace(
                    go.Heatmap(
                        z=kwargs["data_list"],
                        colorscale=colorscale,
                        showscale=True,
                        colorbar={
                            "title": {"text": kwargs["zlabel"], "side": "right"},
                            "ticktext": kwargs["legends"],
                            "tickvals": tickvals,
                            "lenmode": "fraction",
                            "len": 0.50,
                            "xanchor": "left",
                            "yanchor": "top",
                        },
                    )
                )
                self.set_xytick_precision_xyt_label(**kwargs)
        else:
            if not self.check_XY_repeat(**kwargs):
                self.figure.add_trace(
                    go.Heatmap(
                        x=kwargs["xdata_list"],
                        y=kwargs["ydata_list"],
                        z=kwargs["data_list"],
                        colorscale=kwargs["cmap"],
                        showscale=True,
                        colorbar={
                            "title": {"text": kwargs["zlabel"], "side": "right"},
                            "tickformat": f".{kwargs['z_precision']}f",
                            "lenmode": "fraction",
                            "len": 0.50,
                            "xanchor": "left",
                            "yanchor": "top",
                        },
                    )
                )
                if kwargs["colorbar_location"]:
                    self.warn("colorbar_location parameter is not valid for plotly")
                self.set_xyprecision_xyt_label(**kwargs)
            else:
                self.figure.add_trace(
                    go.Heatmap(
                        z=kwargs["data_list"],
                        colorscale=kwargs["cmap"],
                        showscale=True,
                        colorbar={
                            "title": {"text": kwargs["zlabel"], "side": "right"},
                            "tickformat": f".{kwargs['z_precision']}f",
                            "lenmode": "fraction",
                            "len": 0.50,
                            "xanchor": "left",
                            "yanchor": "top",
                        },
                    )
                )
                if kwargs["colorbar_location"]:
                    self.warn("colorbar_location parameter is not valid for plotly")
                self.set_xytick_precision_xyt_label(**kwargs)


class ThreeDimensionPlotly(ParentPlotly):
    """A plotly 3d plot class for heatmap

    Args:
        ParentPlotly (object): plotly parent class

    Parameters:
        data_list :List[List[float]]
        xdata_list :List[float]
        ydata_list :List[float]
        legends :List[str]
        color_list :List[str]
        xlabel :str
        ylabel :str
        zlabel :str
        title :str
        x_precision :int
        y_precision :int
        z_precision :int
        colorbar_location :str
        cmap :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        if len(kwargs["data_list"]) <= 1 or len(kwargs["data_list"][0]) <= 1:
            self.error("!!! 3d plot unable to proper deal with 1 dimension data !!!")

        if not self.check_XY_repeat(**kwargs):
            self.figure.add_trace(
                go.Surface(
                    x=kwargs["xdata_list"],
                    y=kwargs["ydata_list"],
                    z=kwargs["data_list"],
                    colorscale=kwargs["cmap"],
                    showscale=True,
                    colorbar={
                        "title": {"text": kwargs["zlabel"], "side": "right"},
                        "tickformat": f".{kwargs['z_precision']}f",
                        "lenmode": "fraction",
                        "len": 0.50,
                        "xanchor": "left",
                        "yanchor": "top",
                    },
                )
            )
            self.figure.update_layout(
                legend_orientation="h",
                title=kwargs["title"],
                font=dict(family="Arial, Times New Roman", size=18),
                showlegend=True,
                scene=dict(
                    xaxis=dict(
                        tickfont=dict(size=14, family="Arial, Times New Roman"),
                        title=kwargs["xlabel"],
                    ),
                    yaxis=dict(
                        tickfont=dict(size=14, family="Arial, Times New Roman"),
                        title=kwargs["ylabel"],
                    ),
                    zaxis=dict(
                        tickfont=dict(size=14, family="Arial, Times New Roman"),
                        title=kwargs["zlabel"],
                    ),
                ),
            )
            self.figure.update_traces(
                contours_z=dict(show=True, usecolormap=True, project_z=True)
            )
            if kwargs["x_precision"] != None:
                self.figure.update_scenes(xaxis_tickformat=f".{kwargs['x_precision']}f")
            if kwargs["y_precision"] != None:
                self.figure.update_scenes(yaxis_tickformat=f".{kwargs['y_precision']}f")
            if kwargs["z_precision"] != None:
                self.figure.update_scenes(zaxis_tickformat=f".{kwargs['z_precision']}f")
            if kwargs["colorbar_location"]:
                self.warn("colorbar_location parameter is not valid for plotly")
        else:
            self.figure.add_trace(
                go.Surface(
                    z=kwargs["data_list"],
                    colorscale=kwargs["cmap"],
                    showscale=True,
                    colorbar={
                        "title": {"text": kwargs["zlabel"], "side": "right"},
                        "tickformat": f".{kwargs['z_precision']}f",
                        "lenmode": "fraction",
                        "len": 0.50,
                        "xanchor": "left",
                        "yanchor": "top",
                    },
                )
            )
            self.figure.update_layout(
                legend_orientation="h",
                title=kwargs["title"],
                font=dict(family="Arial, Times New Roman", size=18),
                showlegend=True,
                scene=dict(
                    xaxis=dict(
                        tickfont=dict(size=14, family="Arial, Times New Roman"),
                        title=kwargs["xlabel"],
                    ),
                    yaxis=dict(
                        tickfont=dict(size=14, family="Arial, Times New Roman"),
                        title=kwargs["ylabel"],
                    ),
                    zaxis=dict(
                        tickfont=dict(size=14, family="Arial, Times New Roman"),
                        title=kwargs["zlabel"],
                    ),
                ),
            )
            self.figure.update_traces(
                contours_z=dict(show=True, usecolormap=True, project_z=True)
            )
            step = len(kwargs["xdata_list"]) // self.nticks
            step = [step, 1][step == 0]
            xdata_index = [i for i in range(0, len(kwargs["xdata_list"]), step)]
            step = len(kwargs["ydata_list"]) // self.nticks
            step = [step, 1][step == 0]
            ydata_index = [i for i in range(0, len(kwargs["ydata_list"]), step)]
            if kwargs["x_precision"] != None:
                self.figure.update_scenes(
                    xaxis_tickvals=xdata_index,
                    xaxis_ticktext=[
                        f"{kwargs['xdata_list'][x]:.{kwargs['x_precision']}f}"
                        for x in xdata_index
                    ],
                )
            if kwargs["y_precision"] != None:
                self.figure.update_scenes(
                    yaxis_tickvals=ydata_index,
                    yaxis_ticktext=[
                        f"{kwargs['ydata_list'][y]:.{kwargs['y_precision']}f}"
                        for y in ydata_index
                    ],
                )
            if kwargs["z_precision"] != None:
                self.figure.update_scenes(zaxis_tickformat=f".{kwargs['z_precision']}f")
            if kwargs["colorbar_location"]:
                self.warn("colorbar_location parameter is not valid for plotly")


class ContourPlotly(ParentPlotly):
    """A plotly contour plot class for heatmap

    Args:
        ParentPlotly (object): plotly parent class

    Parameters:
        data_list :List[List[float]]
        xdata_list :List[float]
        ydata_list :List[float]
        legends :List[str]
        color_list :List[str]
        xlabel :str
        ylabel :str
        zlabel :str
        title :str
        x_precision :int
        y_precision :int
        z_precision :int
        colorbar_location :str
        cmap :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        if len(kwargs["data_list"]) <= 1 or len(kwargs["data_list"][0]) <= 1:
            self.error("!!! contour unable to proper deal with 1 dimension data !!!")

        if not self.check_XY_repeat(**kwargs):
            self.figure.add_trace(
                go.Contour(
                    x=kwargs["xdata_list"],
                    y=kwargs["ydata_list"],
                    z=kwargs["data_list"],
                    colorscale=kwargs["cmap"],
                    showscale=True,
                    colorbar={
                        "title": {"text": kwargs["zlabel"], "side": "right"},
                        "tickformat": f".{kwargs['z_precision']}f",
                        "lenmode": "fraction",
                        "len": 0.50,
                        "xanchor": "left",
                        "yanchor": "top",
                    },
                    contours=dict(showlines=False),
                )
            )
            if kwargs["colorbar_location"]:
                self.warn("colorbar_location parameter is not valid for plotly")
            self.set_xyprecision_xyt_label(**kwargs)
        else:
            self.figure.add_trace(
                go.Contour(
                    z=kwargs["data_list"],
                    colorscale=kwargs["cmap"],
                    showscale=True,
                    colorbar={
                        "title": {"text": kwargs["zlabel"], "side": "right"},
                        "tickformat": f".{kwargs['z_precision']}f",
                        "lenmode": "fraction",
                        "len": 0.50,
                        "xanchor": "left",
                        "yanchor": "top",
                    },
                    contours=dict(showlines=False),
                )
            )
            if kwargs["colorbar_location"]:
                self.warn("colorbar_location parameter is not valid for plotly")
            self.set_xytick_precision_xyt_label(**kwargs)
