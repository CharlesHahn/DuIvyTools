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
from matplotlib import patches
from matplotlib.ticker import AutoLocator, FormatStrFormatter

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class ParentMatplotlib(log):
    """parent class for drawing figure by matplotlib"""

    def __init__(self):
        self.load_style()
        self.figure = plt.figure()

    def load_style(self):
        """load matplotlib style file"""
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
        """do final process of drawing figure with matplotlib

        Args:
            outfig (str): the user specified output figure name
            noshow (bool): True for no display the figure
        """
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
        # optional
        highs :List[List[float]]
        lows :List[List[float]]
        alpha :float
        legend_location:str #{inside, outside}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        for i, data in enumerate(kwargs["data_list"]):
            if len(kwargs["highs"]) != 0 and len(kwargs["lows"]) != 0:
                plt.fill_between(
                    kwargs["xdata_list"][i],
                    kwargs["highs"][i],
                    kwargs["lows"][i],
                    alpha=kwargs["alpha"],
                )
            plt.plot(kwargs["xdata_list"][i], data, label=kwargs["legends"][i])

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
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

        if kwargs["legend_location"] == "outside":
            ## TODO hard code the legend location???
            plt.legend(bbox_to_anchor=(1.02, 1.00), loc="upper left")
        else:
            plt.legend()
        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])
        plt.title(kwargs["title"])


class ScatterMatplotlib(ParentMatplotlib):
    """A matplotlib scatter plot class for scatter plots

    Args:
        ParentMatplotlib (object): matplotlib parent class

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
        legend_location:str #{inside, outside}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        ## TODO think again, user to define marker by scatter.marker
        marker_list = [
            "o",
            "v",
            "^",
            "<",
            ">",
            "8",
            "s",
            "p",
            "*",
            "h",
            ".",
            "H",
            "D",
            "d",
            "P",
            "X",
        ]
        for i, data in enumerate(kwargs["data_list"]):
            plt.scatter(
                kwargs["xdata_list"][i],
                data,
                c=kwargs["color_list"][i],
                label=kwargs["legends"][i],
                marker=marker_list[i],
                cmap=kwargs["cmap"],
            )
        if kwargs["z_precision"] != None:
            plt.colorbar(
                label=kwargs["zlabel"],
                format=FormatStrFormatter(f"""%.{kwargs["z_precision"]}f"""),
                location=kwargs["colorbar_location"],
            )
        else:
            plt.colorbar(
                label=kwargs["zlabel"],
                location=kwargs["colorbar_location"],
            )

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
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

        if kwargs["legend_location"] == "outside":
            plt.legend(bbox_to_anchor=(1.02, 1.00), loc="upper left")
        else:
            plt.legend()
        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])
        plt.title(kwargs["title"])


class StackMatplotlib(ParentMatplotlib):
    """A matplotlib stack line plot class for stack line plots

    Args:
        ParentMatplotlib (object): matplotlib parent class

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
        # optional
        highs :List[List[float]]
        lows :List[List[float]]
        alpha :float
        legend_location:str #{inside, outside}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        for i, _ in enumerate(kwargs["data_list"]):
            plt.fill_between(
                kwargs["xdata_list"][i],
                kwargs["highs"][i],
                kwargs["lows"][i],
                alpha=kwargs["alpha"],
                label=kwargs["legends"][i],
            )

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
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

        if kwargs["legend_location"] == "outside":
            plt.legend(bbox_to_anchor=(1.02, 1.00), loc="upper left")
        else:
            plt.legend()
        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])
        plt.title(kwargs["title"])


class BarMatplotlib(ParentMatplotlib):
    """A matplotlib bar plot class for bar plots

    Args:
        ParentMatplotlib (object): matplotlib parent class

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

        width = 84 // len(kwargs["data_list"]) * 0.01
        x_loc = [x - 0.42 + width / 2.0 for x in range(len(kwargs["data_list"][0]))]
        for i, data in enumerate(kwargs["data_list"]):
            plt.bar(
                [x + width * i for x in x_loc],
                data,
                width,
                yerr=kwargs["stds_list"][i],
                capsize=4,
                label=kwargs["legends"][i],
            )
        plt.xticks(
            [x for x in range(len(kwargs["data_list"][0]))], labels=kwargs["xtitles"]
        )
        plt.axhline(0, color="k", linewidth=1)

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
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

        if kwargs["legend_location"] == "outside":
            ## TODO hard code the legend location???
            plt.legend(bbox_to_anchor=(1.02, 1.00), loc="upper left")
        else:
            plt.legend()
        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])
        plt.title(kwargs["title"])


class BoxMatplotlib(ParentMatplotlib):
    """A matplotlib box plot class for box plots

    Args:
        ParentMatplotlib (object): matplotlib parent class

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

        ## scatter
        loc = 1.0
        if kwargs["mode"] != "withoutScatter":
            loc = 0.75
            for i, data in enumerate(kwargs["data_list"]):
                plt.scatter(
                    np.random.normal(i + 1.25, 0.04, len(data)),
                    data,
                    alpha=kwargs["alpha"],
                    c=kwargs["color_list"][i],
                    cmap=kwargs["cmap"],
                )
            if kwargs["z_precision"] != None:
                plt.colorbar(
                    label=kwargs["zlabel"],
                    format=FormatStrFormatter(f"""%.{kwargs["z_precision"]}f"""),
                    location=kwargs["colorbar_location"],
                )
            else:
                plt.colorbar(
                    label=kwargs["zlabel"],
                    location=kwargs["colorbar_location"],
                )

        box_positions = [i + loc for i in range(len(kwargs["data_list"]))]
        plt.violinplot(
            kwargs["data_list"],
            showmeans=False,
            showmedians=False,
            showextrema=False,
            positions=box_positions,
        )
        plt.boxplot(
            kwargs["data_list"],
            sym=".",
            meanline=True,
            showmeans=True,
            # patch_artist=True,
            notch=True,
            widths=0.1,
            positions=box_positions,
        )
        plt.xticks([i + 1 for i in range(len(kwargs["data_list"]))], kwargs["legends"])

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
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

        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])
        plt.title(kwargs["title"])


class RamachandranMatplotlib(ParentMatplotlib):
    """A matplotlib ramachandran plot class for ramachandran plots

    Args:
        ParentMatplotlib (object): matplotlib parent class

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
        super().__init__()

        ## draw ramachandran plot
        normals = kwargs["normals"]
        outliers = kwargs["outliers"]
        rama_pref_values = kwargs["rama_pref_values"]
        rama_preferences = kwargs["rama_preferences"]
        for key in ["General", "GLY", "Pre-PRO", "PRO"]:
            if len(normals[key]["phi"]) + len(outliers[key]["phi"]) == 0:
                continue
            plt.clf()
            plt.imshow(
                rama_pref_values[key],
                cmap=mplcolors.ListedColormap(rama_preferences[key]["cmap"]),
                norm=mplcolors.BoundaryNorm(
                    rama_preferences[key]["bounds"],
                    mplcolors.ListedColormap(rama_preferences[key]["cmap"]).N,
                ),
                extent=(-180, 180, 180, -180),
            )
            plt.scatter(normals[key]["phi"], normals[key]["psi"], s=8)
            plt.scatter(outliers[key]["phi"], outliers[key]["psi"], s=8)
            plt.xlim([-180, 180])
            plt.ylim([-180, 180])
            plt.xticks([-180, -120, -60, 0, 60, 120, 180])
            plt.yticks([-180, -120, -60, 0, 60, 120, 180])
            plt.tick_params(left=False, bottom=False, top=False, right=False)
            if kwargs["title"] != None:
                title = kwargs["title"]
            else:
                title = key
            plt.title(title)
            plt.xlabel(kwargs["xlabel"])
            plt.ylabel(kwargs["ylabel"])
            plt.tight_layout()

            outfig = kwargs["outfig"]
            noshow = kwargs["noshow"]
            if outfig != None:
                if os.path.exists(outfig):
                    time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    new_outfig = f'{".".join(outfig.split(".")[:-1])}_{time_info}.{outfig.split(".")[-1]}'
                    self.warn(
                        f"{outfig} is already in current directory, save to {new_outfig} for instead."
                    )
                    outfig = new_outfig
                outfig = outfig.split(".")[0] + "_" + key + ".png"
                self.figure.savefig(outfig)
                self.info(f"save figure to {outfig} successfully")
            if noshow == False:
                plt.show()


class ImshowMatplotlib(ParentMatplotlib):
    """A matplotlib imshow plot class for heatmap

    Args:
        ParentMatplotlib (object): matplotlib parent class

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
        xmin :float
        xmax :float
        ymin :float
        ymax :float
        x_precision :int
        y_precision :int
        z_precision :int
        alpha :float
        legend_location :str
        colorbar_location :str
        interpolation :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        ## TODO: original color
        if kwargs["fig_type"] != "Continuous":
            im = plt.imshow(kwargs["data_list"], interpolation=kwargs["interpolation"], alpha=kwargs["alpha"])
            legend_patches = []
            for ind, note in enumerate(kwargs["legends"]):
                leg_patch = patches.Patch(color=kwargs["color_list"][ind], label=note)
                legend_patches.append(leg_patch)
            plt.legend(
                handles=legend_patches,
                bbox_to_anchor=(1.02, 1.00),
                loc="upper left",
                borderaxespad=0,
            )
        else:
            im = plt.imshow(kwargs["data_list"], interpolation=kwargs["interpolation"], alpha=kwargs["alpha"])
            plt.colorbar(im, label=kwargs["zlabel"])

        plt.title(kwargs["title"])
        plt.xlabel(kwargs["xlabel"])
        plt.ylabel(kwargs["ylabel"])


class PcolormeshMatplotlib(ParentMatplotlib):
    """A matplotlib pcolormesh plot class for heatmap

    Args:
        ParentMatplotlib (object): matplotlib parent class

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
        xmin :float
        xmax :float
        ymin :float
        ymax :float
        x_precision :int
        y_precision :int
        z_precision :int
        alpha :float
        legend_location :str
        colorbar_location :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()



class ThreeDimensionMatplotlib(ParentMatplotlib):
    """A matplotlib 3d plot class for heatmap

    Args:
        ParentMatplotlib (object): matplotlib parent class

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
        xmin :float
        xmax :float
        ymin :float
        ymax :float
        x_precision :int
        y_precision :int
        z_precision :int
        alpha :float
        legend_location :str
        colorbar_location :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()






class ContourMatplotlib(ParentMatplotlib):
    """A matplotlib contour plot class for heatmap

    Args:
        ParentMatplotlib (object): matplotlib parent class

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
        xmin :float
        xmax :float
        ymin :float
        ymax :float
        x_precision :int
        y_precision :int
        z_precision :int
        alpha :float
        legend_location :str
        colorbar_location :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

