"""
Visualizer_gnuplot module is part of DuIvyTools providing visualization tools based on gnuplot engine.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
import subprocess
from typing import List, Union

import numpy as np

from utils import log


class Gnuplot(log):
    """Gnuplot class for plotting with gnuplot"""

    def __init__(self) -> None:
        self.style = {
            "font": "Arial",
            "fontsize": 14,
            "fontscale": 1,
            "linewidth": 2,
            "pointscale": 1,
            "width": 1200,
            "height": 1000,
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
        self.term: str = None
        self.outfig: str = None
        self.title: str = None
        self.xlabel: str = None
        self.ylabel: str = None
        self.zlabel: str = None
        self.xmin: float = None
        self.xmax: float = None
        self.ymin: float = None
        self.ymax: float = None
        self.zmin: float = None
        self.zmax: float = None
        self.x_precision: int = None
        self.y_precision: int = None
        self.z_precision: int = None
        self.legends: List[str] = None
        self.xdata: List[List[float]] = None
        self.ydata: List[List[float]] = None
        self.data: List[List[float]] = None
        self.highs: List[List[float]] = None
        self.lows: List[List[float]] = None
        self.color_list: List[List[float]] = None
        self.colorbar_location: str = None
        self.legend_location: str = "inside"
        self.colormap: str = None
        self.plot_type: str = "line"
        self.mode: str = None
        self.xtitles: List[str] = None
        self.stds_list: List[List[str]] = None

    def dump2str(self) -> str:
        """dump gnuplot properties to gnuplot input scripts

        Returns:
            str: result string for gnuplto input
        """
        gpl: str = ""
        if self.term != None:
            gpl += f"""set term {self.term}\n"""
        if self.outfig != None:
            gpl += f"""set output "{self.outfig}"\n"""
        if self.title != None:
            gpl += f"""set title "{self.title}"\n"""
        if self.xlabel != None:
            gpl += f"""set xlabel "{self.xlabel}"\n"""
        if self.ylabel != None:
            gpl += f"""set ylabel "{self.ylabel}"\n"""
        if self.zlabel != None:
            gpl += f"""set zlabel "{self.zlabel}"\n"""
        if self.legend_location == "inside":
            gpl += f"""set key inside\n"""
        elif self.legend_location == "outside":
            gpl += f"""set key outside reverse Left\n"""

        if self.xmin == None:
            self.xmin = ""
        if self.xmax == None:
            self.xmax = ""
        # gpl += f"""set xrange [{self.xmin}:{self.xmax}]\n"""
        if self.ymin == None:
            self.ymin = ""
        if self.ymax == None:
            self.ymax = ""
        # gpl += f"""set yrange [{self.ymin}:{self.ymax}]\n"""

        if self.x_precision != None:
            gpl += f"""set xtics format "%.{self.x_precision}f" \n"""
        if self.y_precision != None:
            gpl += f"""set ytics format "%.{self.y_precision}f" \n"""
        if self.z_precision != None:
            gpl += f"""set ztics format "%.{self.z_precision}f" \n"""

        gpl += f"""set term pngcairo enhanced truecolor font \"{self.style["font"]},{self.style["fontsize"]}\" fontscale {self.style["fontscale"]} linewidth {self.style["linewidth"]} pointscale {self.style["pointscale"]} size {self.style["width"]},{self.style["height"]} \n"""

        if self.plot_type == "line":
            gpl = self.line_plot(gpl)
        elif self.plot_type == "scatter":
            gpl = self.scatter_plot(gpl)
        elif self.plot_type == "stack":
            gpl = self.stack_plot(gpl)
        elif self.plot_type == "violin":
            gpl = self.violin_plot(gpl)
        elif self.plot_type == "bar":
            gpl = self.bar_plot(gpl)
        elif self.plot_type == "imshow":
            gpl = self.imshow(gpl)
        elif self.plot_type == "3d":
            gpl = self.threeDimension(gpl)
        elif self.plot_type == "contour":
            gpl = self.contour(gpl)

        return gpl
    
    def imshow(self, gpl:str) -> str:
        if len(self.data) == 1:
            self.error("gnuplot engine can not deal with heatmap with only 1 dimension")
        if self.xpm_type != "Continuous":
            gpl += "set key out reverse Left spacing 2 samplen 1/2\n"
            gpl += "unset colorbox\n"
            pal_line = "set pal defined("
            for index, color in enumerate(self.color_list):
                pal_line += f"""{index} "{color}","""
            pal_line = pal_line.strip(",") + ")"
            gpl += pal_line + "\n\n"
            gpl += f"\n$matrix << EOD\n"
            for y, y_value in enumerate(self.ydata):
                for x, x_value in enumerate(self.xdata):
                    gpl += f"""{x_value} {y_value} {self.data[y][x]}\n"""
                gpl += "\n"
            gpl += "EOD\n\n"
            gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
            gpl += f"""$matrix using 1:2:3 with image notitle, \\\n"""
            for id, leg in enumerate(self.legends):
                gpl += f"""{np.floor(np.min(self.ydata))-1} w p ps 4 pt 5 lc rgb "{self.color_list[id]}" title "{leg}", \\\n"""
            gpl = gpl.strip("\n").strip("\\").strip().strip(",")

        else:
            if self.zlabel != None:
                gpl += f"""set cblabel "{self.zlabel}"\n"""
            if self.z_precision != None:
                gpl += f"""set cbtics format "%.{self.z_precision}f"\n"""
            gpl += f"\n$matrix << EOD\n"
            for y, y_value in enumerate(self.ydata):
                for x, x_value in enumerate(self.xdata):
                    gpl += f"""{x_value} {y_value} {self.data[y][x]}\n"""
                gpl += "\n"
            gpl += "EOD\n\n"
            gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
            gpl += f"""$matrix using 1:2:3 with image notitle """
            gpl += "\n"

        return gpl

    def threeDimension(self, gpl:str) -> str:

        return gpl

    def contour(self, gpl:str) -> str:

        return gpl

    def stack_plot(self, gpl: str) -> str:
        gpl += f"""set style fill transparent solid {self.style["alpha"]} noborder\n"""
        for c in range(len(self.data)):
            gpl += f"\n$data{c} << EOD\n"
            for r in range(len(self.xdata[c])):
                gpl += f"""{self.xdata[c][r]} {self.data[c][r]} {self.highs[c][r]} {self.lows[c][r]}\n"""
            gpl += "EOD\n\n"
        gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
        for c in range(len(self.data)):
            gpl += f"""$data{c} using 1:3:4 with filledcurves lt rgb "{self.style["color_cycle"][c]}" title "{self.legends[c]}", \\\n"""
        gpl += "\n"

        return gpl

    def violin_plot(self, gpl: str) -> str:
        if self.data and self.legends:
            for c in range(len(self.data)):
                gpl += f"\n$data{c} << EOD\n"
                for r in range(len(self.data[c])):
                    gpl += f"""{self.data[c][r]} {self.color_list[c][r]}\n"""
                gpl += "EOD\n\n"

            gpl += """set errorbars front 1.000000  lt black linewidth 1.000 dashtype solid
set boxwidth 0.075 absolute
set style fill solid 1.00 border lt -1
set style data filledcurves below 
set colorbox vertical origin screen 0.9, 0.2 size screen 0.05, 0.6 front  noinvert bdefault\n"""
            gpl += """set xtics ("""
            gpl += ",".join(
                [f""""{leg}" {i+1}""" for i, leg in enumerate(self.legends)]
            )
            gpl += """)\n"""
            for c in range(len(self.data)):
                gpl += f"""set table $kdedata{c}\n"""
                gpl += f"""plot $data{c} using 1:(1) smooth kdensity with filledcurves above y lt {c+1} title "{self.legends[c]}"\n"""
            gpl += "unset table\n"
            gpl += "unset key\n"
            for c in range(len(self.data)):
                gpl += (
                    f"""stats $kdedata{c} using 2 nooutput name "kdedata{c}_stats" \n"""
                )
            ## scatter plot
            loc = 1.0
            if self.mode != "withoutScatter":
                loc = 0.75
                if self.zlabel != None:
                    gpl += f"""set cblabel "{self.zlabel}"\n"""
                if self.z_precision != None:
                    gpl += f"""set cbtics format "%.{self.z_precision}f"\n"""
                gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
                for c in range(len(self.data)):
                    gpl += f"""$data{c} u ({c+1.25}+0.04*invnorm(rand(0))):1:2 title "{self.legends[c]}" with points palette, \\\n"""

            if self.mode == "withoutScatter":
                gpl += f"\nplot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
            for c in range(len(self.data)):
                gpl += f"""$kdedata{c} using ({c+loc}+$2/(4.2*kdedata{c}_stats_max)):1 with filledcurve x={c+loc} lt {c+1},\\\n"""
                gpl += f"""$kdedata{c} using ({c+loc}-$2/(4.2*kdedata{c}_stats_max)):1 with filledcurve x={c+loc} lt {c+1},\\\n"""
                gpl += f"""$data{c} u ({c+loc}):1 with boxplot fc "white" lw 1 ,\\\n"""
            gpl += "\n"

        return gpl

    def scatter_plot(self, gpl: str) -> str:
        # TODO colorbar_location
        # TODO cmap
        if self.zlabel != None:
            gpl += f"""set cblabel "{self.zlabel}"\n"""
        if self.z_precision != None:
            gpl += f"""set cbtics format "%.{self.z_precision}f"\n"""
        if self.data and self.legends:
            for c in range(len(self.data)):
                gpl += f"\n$data{c} << EOD\n"
                for r in range(len(self.xdata[c])):
                    gpl += f"""{self.xdata[c][r]} {self.data[c][r]} {self.color_list[c][r]}\n"""
                gpl += "EOD\n\n"
            gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
            for c in range(len(self.data)):
                gpl += f"""$data{c} u 1:2:3 title "{self.legends[c]}" with points palette, \\\n"""
            gpl += "\n"

        return gpl

    def line_plot(self, gpl: str) -> str:
        if self.data and self.legends and len(self.highs) == 0 and len(self.lows) == 0:
            for c in range(len(self.data)):
                gpl += f"\n$data{c} << EOD\n"
                for r in range(len(self.xdata[c])):
                    gpl += f"""{self.xdata[c][r]} {self.data[c][r]}\n"""
                gpl += "EOD\n\n"
            gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
            for c in range(len(self.data)):
                gpl += f"""$data{c} u 1:2 title "{self.legends[c]}" with lines lt rgb "{self.style["color_cycle"][c]}", \\\n"""
            gpl += "\n"

        if self.data and self.legends and len(self.highs) != 0 and len(self.lows) != 0:
            gpl += (
                f"""set style fill transparent solid {self.style["alpha"]} noborder\n"""
            )
            for c in range(len(self.data)):
                gpl += f"\n$data{c} << EOD\n"
                for r in range(len(self.xdata[c])):
                    gpl += f"""{self.xdata[c][r]} {self.data[c][r]} {self.highs[c][r]} {self.lows[c][r]}\n"""
                gpl += "EOD\n\n"
            gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
            for c in range(len(self.data)):
                gpl += f"""$data{c} using 1:3:4 with filledcurves notitle lt rgb "{self.style["color_cycle"][c]}", $data{c} u 1:2 title "{self.legends[c]}" with lines lt rgb "{self.style["color_cycle"][c]}", \\\n"""
            gpl += "\n"

        return gpl

    def bar_plot(self, gpl: str) -> str:
        if self.data and self.legends:
            for c in range(len(self.data)):
                gpl += f"\n$data{c} << EOD\n"
                xdata = [x for x in range(len(self.data[c]))]
                for x, d, s in zip(xdata, self.data[c], self.stds_list[c]):
                    gpl += f"""{x} {d} {s}\n"""
                gpl += "EOD\n\n"
            gpl += """set xtics ("""
            gpl += ",".join([f""""{xt}" {i}""" for i, xt in enumerate(self.xtitles)])
            gpl += """)\n"""
            gpl += """set style histogram errorbars lw 2\n"""
            gpl += """set style fill solid border -1\n"""
            gpl += f"plot [{self.xmin}:{self.xmax}][{self.ymin}:{self.ymax}] "
            for c in range(len(self.data)):
                gpl += f"""$data{c} u 2:3 title "{self.legends[c]}" with histogram lt rgb "{self.style["color_cycle"][c]}", \\\n"""
            gpl += "\n"

        return gpl


class ParentGnuplot(log):
    """the parent class of varieties of gnuplot figures"""

    def __init__(self) -> None:
        time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.outfig: str = f"DIT_gnuplot_output_{time_info}.png"
        self.gpl_file: str = f"DIT_gnuplot_script_dump_{time_info}.gpl"
        self.gnuplot = Gnuplot()

    def dump(self) -> None:
        """dump gnuplot input scripts into a input file"""
        gpl = self.gnuplot.dump2str()
        with open(self.gpl_file, "w") as fo:
            fo.write(gpl)
        self.info(f"temporarily dump gnuplot scripts to {self.gpl_file}")

    def clean(self) -> None:
        """remove the gnuplot input script file"""
        os.remove(self.gpl_file)
        self.info(f"removed gnuplot scripts {self.gpl_file}")

    def run(self) -> None:
        """run the gnuplot script to get figure"""
        inCmd = f"""echo load "{self.gpl_file}" | gnuplot"""
        p = subprocess.Popen(
            inCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.info(f"running gnuplot at pid -> {p.pid}")
        output, error = p.communicate()
        p.wait()
        status = ("Fail", "Success")[p.returncode == 0]
        output, error = output.decode(), error.decode()
        self.info(f"gnuplot status -> {status}")
        if output:
            self.info(f"gnuplot output -> {output}")
        if error:
            self.error(f"gnuplot error -> {error}")

    def final(self, outfig: str, noshow: bool) -> None:
        """deal with final process of plotting by gnuplot

        Args:
            outfig (str): the user specified output figure name
            noshow (bool): True for not delete the gnuplot scripts file
        """
        if outfig != None:
            if os.path.exists(outfig):
                time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())
                new_outfig = f'{".".join(outfig.split(".")[:-1])}_{time_info}.{outfig.split(".")[-1]}'
                self.warn(
                    f"{outfig} is already in current directory, save to {new_outfig} for instead."
                )
                outfig = new_outfig
            self.outfig = outfig
        self.gnuplot.outfig = self.outfig
        self.dump()
        if not noshow:
            self.run()
            self.clean()


class LineGnuplot(ParentGnuplot):
    """A Gnuplot line plot class for line plots

    Args:
        ParentGnuplot (object): Gnuplot parent class

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
        legend_location :str # {inside, outside}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.gnuplot.term = "png"
        self.gnuplot.title = kwargs["title"]
        self.gnuplot.xlabel = kwargs["xlabel"]
        self.gnuplot.ylabel = kwargs["ylabel"]

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
            self.gnuplot.xmin = kwargs["xmin"]
            self.gnuplot.xmax = kwargs["xmax"]
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.gnuplot.ymin = kwargs["ymin"]
            self.gnuplot.ymax = kwargs["ymax"]
        if kwargs["x_precision"] != None:
            self.gnuplot.x_precision = kwargs["x_precision"]
        if kwargs["y_precision"] != None:
            self.gnuplot.y_precision = kwargs["y_precision"]

        if len(kwargs["legends"]) != len(kwargs["data_list"]):
            self.error(
                f"""unable to pair {len(kwargs["legends"])} legends to {len(kwargs["data_list"])} column data."""
            )
        self.gnuplot.xdata = kwargs["xdata_list"]
        self.gnuplot.data = kwargs["data_list"]
        self.gnuplot.legends = kwargs["legends"]
        self.gnuplot.highs = kwargs["highs"]
        self.gnuplot.lows = kwargs["lows"]
        self.gnuplot.style["alpha"] = kwargs["alpha"]
        self.gnuplot.legend_location = kwargs["legend_location"]


class StackGnuplot(LineGnuplot):
    """A Gnuplot stack line plot class for stack line plots

    Args:
        ParentGnuplot (object): Gnuplot parent class

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
        legend_location :str # {inside, outside}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.gnuplot.plot_type = "stack"


class ScatterGnuplot(ParentGnuplot):
    """A gnuplot scatter plot class for scatter plots

    Args:
        ParentGnuplot (object): gnuplot parent class

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
        legend_location :str # {inside, outside}
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.gnuplot.term = "png"
        self.gnuplot.title = kwargs["title"]
        self.gnuplot.xlabel = kwargs["xlabel"]
        self.gnuplot.ylabel = kwargs["ylabel"]

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
            self.gnuplot.xmin = kwargs["xmin"]
            self.gnuplot.xmax = kwargs["xmax"]
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.gnuplot.ymin = kwargs["ymin"]
            self.gnuplot.ymax = kwargs["ymax"]
        self.gnuplot.x_precision = kwargs["x_precision"]
        self.gnuplot.y_precision = kwargs["y_precision"]
        self.gnuplot.z_precision = kwargs["z_precision"]

        if len(kwargs["legends"]) != len(kwargs["data_list"]):
            self.error(
                f"""unable to pair {len(kwargs["legends"])} legends to {len(kwargs["data_list"])} column data."""
            )
        self.gnuplot.xdata = kwargs["xdata_list"]
        self.gnuplot.data = kwargs["data_list"]
        self.gnuplot.legends = kwargs["legends"]
        self.gnuplot.color_list = kwargs["color_list"]
        self.gnuplot.zlabel = kwargs["zlabel"]
        self.gnuplot.plot_type = "scatter"
        self.gnuplot.legend_location = kwargs["legend_location"]
        # self.gnuplot.colormap = kwargs["cmap"]
        if kwargs["cmap"]:
            self.warn(
                "DIT is unable to set colormap for gnuplot now. The https://github.com/Gnuplotting/gnuplot-palettes may help you"
            )
        # self.gnuplot.colorbar_location = kwargs["colorbar_location"]
        if kwargs["colorbar_location"]:
            self.warn("DIT is unable to set colorbar location for gnuplot now.")


class BarGnuplot(ParentGnuplot):
    """A Gnuplot bar plot class for bar plots

    Args:
        ParentGnuplot (object): gnuplot parent class

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

        self.gnuplot.term = "png"
        self.gnuplot.title = kwargs["title"]
        self.gnuplot.xlabel = kwargs["xlabel"]
        self.gnuplot.ylabel = kwargs["ylabel"]

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
            self.gnuplot.xmin = kwargs["xmin"]
            self.gnuplot.xmax = kwargs["xmax"]
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.gnuplot.ymin = kwargs["ymin"]
            self.gnuplot.ymax = kwargs["ymax"]
        if kwargs["x_precision"] != None:
            self.gnuplot.x_precision = kwargs["x_precision"]
        if kwargs["y_precision"] != None:
            self.gnuplot.y_precision = kwargs["y_precision"]

        if len(kwargs["legends"]) != len(kwargs["data_list"]):
            self.error(
                f"""unable to pair {len(kwargs["legends"])} legends to {len(kwargs["data_list"])} column data."""
            )
        self.gnuplot.data = kwargs["data_list"]
        self.gnuplot.legends = kwargs["legends"]
        self.gnuplot.legend_location = kwargs["legend_location"]
        self.gnuplot.xtitles = kwargs["xtitles"]
        self.gnuplot.stds_list = kwargs["stds_list"]
        self.gnuplot.plot_type = "bar"


class BoxGnuplot(ParentGnuplot):
    """A gnuplot box plot class for box plots

    Args:
        ParentGnuplot (object): gnuplot parent class

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

        self.gnuplot.term = "png"
        self.gnuplot.title = kwargs["title"]
        self.gnuplot.xlabel = kwargs["xlabel"]
        self.gnuplot.ylabel = kwargs["ylabel"]

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
            self.gnuplot.xmin = kwargs["xmin"]
            self.gnuplot.xmax = kwargs["xmax"]
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.gnuplot.ymin = kwargs["ymin"]
            self.gnuplot.ymax = kwargs["ymax"]
        self.gnuplot.x_precision = kwargs["x_precision"]
        self.gnuplot.y_precision = kwargs["y_precision"]
        self.gnuplot.z_precision = kwargs["z_precision"]

        if len(kwargs["legends"]) != len(kwargs["data_list"]):
            self.error(
                f"""unable to pair {len(kwargs["legends"])} legends to {len(kwargs["data_list"])} column data."""
            )

        self.gnuplot.data = kwargs["data_list"]
        self.gnuplot.legends = kwargs["legends"]
        self.gnuplot.color_list = kwargs["color_list"]
        self.gnuplot.zlabel = kwargs["zlabel"]
        self.gnuplot.plot_type = "violin"
        self.gnuplot.mode = kwargs["mode"]
        # self.gnuplot.colormap = kwargs["cmap"]
        if kwargs["cmap"]:
            self.warn(
                "DIT is unable to set colormap for gnuplot now. The https://github.com/Gnuplotting/gnuplot-palettes may help you"
            )
        # self.gnuplot.colorbar_location = kwargs["colorbar_location"]
        if kwargs["colorbar_location"]:
            self.warn("DIT is unable to set colorbar location for gnuplot now.")


class ImshowGnuplot(ParentGnuplot):
    """A gnuplot imshow plot class for heatmap

    Args:
        ParentGnuplot (object): matplotlib parent class

    Parameters:
        fig_type :str
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
        colorbar_location :str
        cmap :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.gnuplot.term = "png"
        self.gnuplot.title = kwargs["title"]
        self.gnuplot.xlabel = kwargs["xlabel"]
        self.gnuplot.ylabel = kwargs["ylabel"]
        self.gnuplot.zlabel = kwargs["zlabel"]

        if kwargs["xmin"] != None or kwargs["xmax"] != None:
            self.gnuplot.xmin = kwargs["xmin"]
            self.gnuplot.xmax = kwargs["xmax"]
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.gnuplot.ymin = kwargs["ymin"]
            self.gnuplot.ymax = kwargs["ymax"]

        data = kwargs["xdata_list"]
        dot_len_x = (np.max(data) - np.min(data))/(len(data)-1)
        data = kwargs["ydata_list"]
        dot_len_y = (np.max(data) - np.min(data))/(len(data)-1)
        if self.gnuplot.xmin == None:
            self.gnuplot.xmin = np.min(kwargs["xdata_list"]) - 0.5*dot_len_x
        if self.gnuplot.xmax == None:
            self.gnuplot.xmax = np.max(kwargs["xdata_list"]) + 0.5*dot_len_x
        if self.gnuplot.ymin == None:
            self.gnuplot.ymin = np.min(kwargs["ydata_list"]) - 0.5*dot_len_y
        if self.gnuplot.ymax == None:
            self.gnuplot.ymax = np.max(kwargs["ydata_list"]) + 0.5*dot_len_y

        self.gnuplot.x_precision = kwargs["x_precision"]
        self.gnuplot.y_precision = kwargs["y_precision"]
        self.gnuplot.z_precision = kwargs["z_precision"]

        self.gnuplot.data = kwargs["data_list"]
        self.gnuplot.xdata = kwargs["xdata_list"]
        self.gnuplot.ydata = kwargs["ydata_list"]
        self.gnuplot.legends = kwargs["legends"]
        self.gnuplot.color_list = kwargs["color_list"]
        self.gnuplot.plot_type = "imshow"
        self.gnuplot.xpm_type = kwargs["fig_type"]

        # self.gnuplot.colormap = kwargs["cmap"]
        if kwargs["cmap"]:
            self.warn(
                "DIT is unable to set colormap for gnuplot now. The https://github.com/Gnuplotting/gnuplot-palettes may help you"
            )
        # self.gnuplot.colorbar_location = kwargs["colorbar_location"]
        if kwargs["colorbar_location"]:
            self.warn("DIT is unable to set colorbar location for gnuplot now.")


class ThreeDimensionGnuplot(ParentGnuplot):
    """A gnuplot 3d plot class for heatmap

    Args:
        ParentGnuplot (object): matplotlib parent class

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
        cmap :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()



class ContourGnuplot(ParentGnuplot):
    """A gnuplot Contour plot class for heatmap

    Args:
        ParentGnuplot (object): matplotlib parent class

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
        cmap :str
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()
