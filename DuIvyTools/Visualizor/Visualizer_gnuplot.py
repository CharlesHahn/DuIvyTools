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

"""
set datafile separator ','
set term pngcairo size 20cm,20cm
set out filename

unset key
set grid
set border lw 1.5

set title the_title
set xrange [x_max-1.1*x_max:x_max*1.1]
set yrange [-1.1*amp:1.1*amp]

plot data u 1:2 w lp pt 7 ps 0.5 lw 2

set out
"""


class ParentGnuplot(log):
    def __init__(self) -> None:
        self.gpl: str = ""
        self.outfig: str = "DIT_gnuplot_output.png"
        self.file: str = "DIT_gnuplot_script_dump.gpl"

    def dump(self) -> None:
        with open(self.file, "w") as fo:
            fo.write(self.gpl + "\n")
        self.info(f"temporarily dump gnuplot scripts to {self.file}")

    def clean(self) -> None:
        os.remove(self.file)
        self.info(f"removed gnuplot scripts {self.file}")

    def run(self) -> None:
        inCmd = f"""echo load "{self.file}" | gnuplot"""
        p = subprocess.Popen(
            inCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print("pid -> ", p.pid)
        output, error = p.communicate()
        p.wait()
        status = ("Fail", "Success")[p.returncode == 0]
        output, error = output.decode(), error.decode()
        print(status, output, error)

    def add(self, msg: str) -> None:
        self.gpl += f"{msg}\n"

    def xlabel(self, msg: str) -> None:
        self.gpl += f"""set xlabel "{msg}"\n"""

    def ylabel(self, msg: str) -> None:
        self.gpl += f"""set ylabel "{msg}"\n"""

    def zlabel(self, msg: str) -> None:
        self.gpl += f"""set zlabel "{msg}"\n"""

    def title(self, msg: str) -> None:
        self.gpl += f"""set title "{msg}"\n"""

    def term(self, msg: str) -> None:
        self.gpl += f"""set term {msg}\n"""

    def output(self, outfig: str) -> None:
        if outfig != None:
            if os.path.exists(outfig):
                time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())
                new_outfig = f'{".".join(outfig.split(".")[:-1])}_{time_info}.{outfig.split(".")[-1]}'
                self.warn(
                    f"{outfig} is already in current directory, save to {new_outfig} for instead."
                )
                outfig = new_outfig
            self.outfig = outfig
        self.gpl += f"""set output "{self.outfig}"\n"""

    def font(
        self,
        font: str = "Arial",
        fontsize: int = 12,
        fontscale: int = 1,
        linewidth: int = 2,
        pointscale: int = 1,
        width: int = 600,
        height: int = 500,
    ) -> None:
        self.gpl += f"""set term pngcairo enhanced truecolor font "{font},{fontsize}" fontscale {fontscale} linewidth {linewidth} pointscale {pointscale} size {width},{height} \n"""

    def xrange(self, xmin: float, xmax: float) -> None:
        if xmin == None:
            xmin = ""
        if xmax == None:
            xmax == ""
        self.gpl += f"""set xrange [{xmin}:{xmax}]\n"""

    def yrange(self, ymin: float, ymax: float) -> None:
        if ymin == None:
            ymin = ""
        if ymax == None:
            ymax == ""
        self.gpl += f"""set yrange [{ymin}:{ymax}]\n"""

    def ytics(self, precision: int) -> None:
        self.add(f"""set ytics  format "%.{precision}f" """)

    def xtics(self, precision: int) -> None:
        self.add(f"""set xtics  format "%.{precision}f" """)

    def data(
        self, xdata: List[float], data_list: List[List[float]], legends: List[str]
    ) -> None:
        self.add("\n$data << EOD")
        for data in zip(xdata, *data_list):
            self.add(" ".join([str(d) for d in data]))
        self.add("EOD\n")

        self.gpl += "plot "
        for i, leg in enumerate(legends, 2):
            self.gpl += f"""$data u 1:{i} title "{leg}" with lines, """
        self.gpl += "\n"

    def final(self) -> None:
        self.dump()
        self.run()
        self.clean()


class LineGnuplot(ParentGnuplot):
    """A Gnuplot line plot class for line plots

    Args:
        ParentGnuplot (object): Gnuplot parent class

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

        self.term("png")
        self.output(kwargs["output"])
        self.title(kwargs["title"])
        self.xlabel(kwargs["xlabel"])
        self.ylabel(kwargs["ylabel"])
        self.font()
        x_min, x_max = np.min(kwargs["xdata"]), np.max(kwargs["xdata"])
        if kwargs["xmin"] == None and kwargs["xmax"] == None:
            x_space = int((x_max - x_min) / 100)
            if int(x_min - x_space) < int(x_max + x_space) - 1.0:
                self.xrange(int(x_min - x_space), int(x_max + x_space))
        else:
            self.xrange(kwargs["xmin"], kwargs["xmax"])
        if kwargs["ymin"] != None or kwargs["ymax"] != None:
            self.yrange(kwargs["ymin"], kwargs["ymax"])
        if kwargs["x_precision"] != None:
            self.xtics(kwargs["x_precision"])
        if kwargs["y_precision"] != None:
            self.ytics(kwargs["y_precision"])

        self.data(kwargs["xdata"], kwargs["data_list"], kwargs["legends"])


class DistributionPlotexet(ParentGnuplot):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class StackGnuplot(ParentGnuplot):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ScatterGnuplot(ParentGnuplot):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BarGnuplot(ParentGnuplot):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class BoxGnuplot(ParentGnuplot):
    def __init__(self, **kwargs) -> None:
        super().__init__()


class ViolinGnuplot(ParentGnuplot):
    def __init__(self, **kwargs) -> None:
        super().__init__()
