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
        self.gpl:str = ""
        self.outfig:str = "DIT_gnuplot_output.png"
    
    def dump(self) -> None:
        self.file = os.path.join("DIT_gnuplot_script_dump.gpl")
        with open(self.file, 'w') as fo:
            fo.write(self.gpl + "\n")
        self.info(f"temporarily dump gnuplot scripts to {self.file}")
    
    def clean(self) -> None:
        os.remove(self.file)
        self.info(f"removed gnuplot scripts {self.file}")
    
    def run(self) -> None:
        inCmd = f"""echo load "{self.file}" | gnuplot"""
        p = subprocess.Popen(inCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("pid -> ", p.pid)
        output, error = p.communicate()
        p.wait()
        status = ("Fail", "Success")[p.returncode == 0]
        output, error = output.decode(), error.decode()
        print(status, output, error)
    
    def add(self, msg) -> None:
        self.gpl += f"{msg}\n"

    
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
            pass
            self.info(f"save figure to {outfig} successfully")
        if noshow == False:
            pass


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

        self.add(f"set term png")
        self.add(f"""set output "{self.outfig}" """)
        self.add(f"""set title "{kwargs["title"]}" """)
        self.add(f"""set xlabel "{kwargs["xlabel"]}" """)
        self.add(f"""set ylabel "{kwargs["ylabel"]}" """)
        self.add("\n$data << EOD\n")

        for data in zip(kwargs["xdata"], *kwargs["data_list"]):
            self.add(" ".join([str(d) for d in data])) 

        self.add("EOD\n")

        self.add("""set term pngcairo enhanced truecolor font "Arial,85" fontscale 1 linewidth 20 pointscale 5 size 6000,5000""")
        self.gpl += "plot "
        for i, leg in enumerate(kwargs["legends"], 2):
            self.gpl += f"""$data u 1:{i} title "{leg}", """
        self.gpl += "\n"

        self.dump()
        self.run()

        """
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
            self.warn("unable to apply x_precision to Gnuplot engine")
        if kwargs["y_precision"] != None:
            self.warn("unable to apply y_precision to Gnuplot engine")
        """


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