"""
XPM module is part of DuIvyTools library, which is a tool for analysis and 
visualization of GROMACS result files. This module is written by CharlesHahn.

XPM module process xpm files, including getting information from xpm, 
visualization and data convertion. 

This module requires Numpy, Scipy, Matplotlib and argparse. 

This module contains:
    class XPM
    function xpm_combine
    ......

This file is provided to you under GPLv2 License"""

## TODO: data convertion and process in XPM class

import os
import sys
import math
import argparse
import numpy as np
from scipy.interpolate import interp2d
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, FormatStrFormatter
from matplotlib import pylab as pylab
from matplotlib import patches

myparams = {
    "axes.labelsize": "12",
    "xtick.labelsize": "12",
    "ytick.labelsize": "12",
    "ytick.left": False,
    "ytick.direction": "in",
    "xtick.bottom": False,
    "xtick.direction": "in",
    "lines.linewidth": "2",
    "axes.linewidth": "1",
    "legend.fontsize": "12",
    "legend.loc": "upper right",
    "legend.fancybox": False,
    "legend.frameon": False,
    "font.family": "Arial",
    "font.size": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
}
pylab.rcParams.update(myparams)

style_files = [file for file in os.listdir() if file[-9:] == ".mplstyle"]
if len(style_files) >= 1:
    plt.style.use(style_files[0])
    print("Info -> using matplotlib style sheet from {}".format(style_files[0]))


class XPM(object):
    """class XPM was defined to process xpm files

    Attributes:
    xpmfile: the name of xpm file
    xpm_title: the title of xpm file
    xpm_legend: the legend of xpm file
    xpm_type: two type of xpm file, "Continuous", "Discrete"
    xpm_xlabel: the x-label of xpm file
    xpm_ylabel: the y-label of xpm file
    xpm_width: the width of xpm file
    xpm_height: the height of xpm file
    xpm_color_num: the number of colors in xpm file
    xpm_char_per_pixel: the number of chars to represent a pixel of xpm figure
    chars: a list to store the chars which reprent pixels in xpm figure
    colors: a list to store the colors in xpm figure
    notes: a list to store the notes (comments to chars and colors) in xpm figure
    colors_rgb: a list of colors in rgb type
    xpm_xaxis: a list to store x-axis values
    xpm_yaxis: a list to store y-axis values
    xpm_datalines: a list to store each line of xpm figure content

    Methods:
    get_scatter_data(self): convert xpm figure content to scatter data
        return:
            scatter_x, scatter_y, x, y, v
    xpm2csv(self, outcsv: str = ""): convert xpm data to csv data
            outcsv: the output csv file name
    xpm2gpl(self, outgpl: str = ""): convert xpm data to gnuplot script
            outgpl: the output gpl file name
    draw_origin(self, IP: bool = False, outputpng: str = None, noshow: bool = False): draw xpm by plt.imshow()
            IP : whether to do interpolation
            outputpng : the output figure file name
            noshow: whether not to show figure, useful for computer without GUI
    draw_pcm(self, IP: bool = False, outputpng: str = None, noshow: bool = False): draw xpm by plt.pcolormesh()
            IP : whether to do interpolation
            outputpng : the output figure file name
            noshow: whether not to show figure, useful for computer without GUI
    draw_3D(self, IP: bool = False, outputpng: str = None, noshow: bool = False): draw xpm in 3D style
            IP : whether to do interpolation
            outputpng : the output figure file name
            noshow: whether not to show figure, useful for computer without GUI
    """

    def __init__(
        self,
        xpmfile: str = None,
        xlabel: str = None,
        ylabel: str = None,
        title: str = None,
        xshrink: float = 1.0,
    ):
        """
        read xpm file and save infos to class xpm

        :parameters:
            xpmfile: the xpm file name
            xlabel: specify the xlabel of figure
            ylabel: specify the ylabel of figure
            title: specify the title of figure
            xshrink: specify the factor for multiplication of x-axis
        """

        ## check parameters
        if xpmfile == None:
            print("Error -> no input xpm file detected")
            exit()
        if not os.path.exists(xpmfile):
            print("ERROR -> no {} in current directory".format(xpmfile))
            exit()
        if xpmfile[-4:] != ".xpm":
            print("Error -> specify a xpm file with suffix xpm")
            exit()
        if xshrink == None:
            xshrink = 1.0

        self.xpmfile = xpmfile
        self.xpm_title = ""
        self.xpm_legend = ""
        self.xpm_type = ""
        self.xpm_xlabel = ""
        self.xpm_ylabel = ""
        self.xpm_width = 0
        self.xpm_height = 0
        self.xpm_color_num = 0
        self.xpm_char_per_pixel = 0
        self.chars = []
        self.colors = []
        self.notes = []
        self.colors_rgb = []
        self.xpm_xaxis = []
        self.xpm_yaxis = []
        self.xpm_datalines = []

        ## read xpm file
        with open(xpmfile, "r") as fo:
            lines = [line.strip() for line in fo.readlines()]

        ## parse content of xpmfile
        flag_4_code = 0  ## means haven't detected yet
        for line in lines:
            ## find the 4 code line and parse
            if flag_4_code == 1:  ## means this line is code4 line
                flag_4_code = 2  ## means have detected
                code4 = [int(c) for c in line.strip().strip(",").strip('"').split()]
                self.xpm_width, self.xpm_height = code4[0], code4[1]
                self.xpm_color_num, self.xpm_char_per_pixel = code4[2], code4[3]
                continue
            elif (flag_4_code == 0) and line.startswith("static char"):
                flag_4_code = 1  ## means next line is code4 line
                continue

            ## parse comments and axis parts
            if line.startswith("/* x-axis"):
                self.xpm_xaxis += [float(n) for n in line.strip().split()[2:-1]]
                continue
            elif line.startswith("/* y-axis"):
                self.xpm_yaxis += [float(n) for n in line.strip().split()[2:-1]]
                continue
            elif line.startswith("/* title"):
                self.xpm_title = line.strip().split('"')[1]
                continue
            elif line.startswith("/* legend"):
                self.xpm_legend = line.strip().split('"')[1]
                continue
            elif line.startswith("/* x-label"):
                self.xpm_xlabel = line.strip().split('"')[1]
                continue
            elif line.startswith("/* y-label"):
                self.xpm_ylabel = line.strip().split('"')[1]
                continue
            elif line.startswith("/* type"):
                self.xpm_type = line.strip().split('"')[1]
                continue

            items = line.strip().split()
            ## for char-color-note part
            if len(items) == 7 and items[1] == "c":
                if len(items[0].strip('"')) == self.xpm_char_per_pixel:
                    self.chars.append(items[0].strip('"'))
                    self.colors.append(items[2])
                    self.notes.append(items[5].strip('"'))
                ## deal with blank
                if len(items[0].strip('"')) < self.xpm_char_per_pixel:
                    print("Warning -> space in char of line : {}".format(line))
                    char_item = items[0].strip('"')
                    self.chars.append(
                        char_item + " " * (self.xpm_char_per_pixel - len(char_item))
                    )
                    self.colors.append(items[2])
                    self.notes.append(items[5].strip('"'))
                continue

            ## for content part
            if line.strip().startswith('"') == 1 and (
                len(line.strip().strip(",").strip('"'))
                == self.xpm_width * self.xpm_char_per_pixel
            ):
                self.xpm_datalines.append(line.strip().strip(",").strip('"'))

        ## check infos
        if len(self.chars) != len(self.colors) != len(self.notes) != self.xpm_color_num:
            print("Wrong -> length of chars, colors, notes != xpm_color_num")
            print(
                "chars : {}, colors : {}, notes : {}, xpm_color_num : {}".format(
                    len(self.chars),
                    len(self.colors),
                    len(self.notes),
                    self.xpm_color_num,
                )
            )
            exit()

        if len(self.xpm_datalines) != self.xpm_height:
            print(
                "ERROR -> rows of data ({}) is not equal to xpm height ({}), check it !".format(
                    len(self.xpm_datalines), self.xpm_height
                )
            )
            exit()
        if (
            len(self.xpm_xaxis) != self.xpm_width
            and len(self.xpm_xaxis) != self.xpm_width + 1
        ):
            print(
                "ERROR -> length of x-axis ({}) != xpm width ({}) or xpm width +1".format(
                    len(self.xpm_xaxis), self.xpm_width
                )
            )
            exit()
        if (
            len(self.xpm_yaxis) != self.xpm_height
            and len(self.xpm_yaxis) != self.xpm_height + 1
        ):
            print(
                "ERROR -> length of y-axis ({}) != xpm height ({}) or xpm height +1".format(
                    len(self.xpm_yaxis), self.xpm_height
                )
            )
            exit()

        if len(self.xpm_xaxis) == self.xpm_width + 1:
            self.xpm_xaxis = [
                (self.xpm_xaxis[i - 1] + self.xpm_xaxis[i]) / 2.0
                for i in range(1, len(self.xpm_xaxis))
            ]
            print(
                "Warning -> length of x-axis is 1 more than xpm width, use intermediate value for instead. "
            )
        if len(self.xpm_yaxis) == self.xpm_height + 1:
            self.xpm_yaxis = [
                (self.xpm_yaxis[i - 1] + self.xpm_yaxis[i]) / 2.0
                for i in range(1, len(self.xpm_yaxis))
            ]
            print(
                "Warning -> length of y-axis is 1 more than xpm height, use intermediate value for instead. "
            )

        ## hex color to rgb values
        for color in self.colors:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            self.colors_rgb.append([r, g, b])

        ## for xlabel and ylabel modification
        if xlabel != None:
            self.xpm_xlabel = xlabel
        if ylabel != None:
            self.xpm_ylabel = ylabel
        if title != None:
            self.xpm_title = title
        if xshrink != None:
            self.xpm_xaxis = [x * float(xshrink) for x in self.xpm_xaxis]

        ## the read order of pixels is from top to bottom
        ## but the y-axis is from bottom to top, so reverse() is important !
        self.xpm_yaxis.reverse()

        print("Info -> all data has been read from {} successfully.".format(xpmfile))

    def get_scatter_data(self) -> tuple:
        """convert xpm data to scatter data"""

        ## parse xpm_data into x, y, v
        x, y, v = [], [], []
        scatter_x, scatter_y = [], []
        # print(len(xpm_xaxis))
        # print(len(xpm_yaxis))
        for l in range(len(self.xpm_datalines)):
            for i in range(
                0, self.xpm_width * self.xpm_char_per_pixel, self.xpm_char_per_pixel
            ):
                v.append(
                    float(
                        self.notes[
                            self.chars.index(
                                self.xpm_datalines[l][i : i + self.xpm_char_per_pixel]
                            )
                        ]
                    )
                )
                x.append(self.xpm_xaxis[int(i / self.xpm_char_per_pixel)])
                y.append(self.xpm_yaxis[l])

        ## parse x, y, v into scatter_x, scatter_y
        v_max = max(v)
        scatter_weight = 1
        for i in range(len(v)):
            count = round((v_max - v[i]) * scatter_weight)
            for _ in range(count):
                scatter_x.append(x[i])
                scatter_y.append(y[i])

        return scatter_x, scatter_y, x, y, v

    def xpm2csv(self, outcsv: str = "") -> None:
        """convert xpm file to csv file
        outcsv: the name of output csv file
        """

        if outcsv == None:
            outcsv = ""
        if outcsv == "":
            outcsv = self.xpmfile[:-4] + ".csv"
        if outcsv[-4:] != ".csv":
            print("ERROR -> specify a output file with suffix csv")
            exit()
        if os.path.exists(outcsv):
            print("ERROR -> {} already in current directory".format(outcsv))
            exit()

        if self.xpm_type != "Continuous":
            print("ERROR -> can not extract data from xpm whose type is not Continuous")
            exit()

        ## only x, y, v values are needed
        _, _, x, y, v = self.get_scatter_data()
        if len(x) != len(y) != len(v):
            print("ERROR -> wrong in length of x, y, v")
            exit()
        ## write results
        with open(outcsv, "w") as fo:
            x_title = (self.xpm_xlabel, "x-axis")[len(self.xpm_xlabel) == 0]
            y_title = (self.xpm_ylabel, "y-axis")[len(self.xpm_ylabel) == 0]
            z_title = (self.xpm_legend, "value")[len(self.xpm_legend) == 0]
            fo.write("{},{},{}\n".format(x_title, y_title, z_title))
            for i in range(len(x)):
                fo.write("{:.6f},{:.6f},{:.6f}\n".format(x[i], y[i], v[i]))
        print("Info -> extract data from {} successfully".format(self.xpmfile))
        print("Info -> data are saved into {}".format(outcsv))

    def xpm2gpl(self, outgpl: str = "") -> None:
        """convert xpm file to gnuplot script
        outgpl: the name of output gnuplot script
        """

        ## check files
        if outgpl == None:
            outgpl = ""
        if outgpl == "":
            outgpl = self.xpmfile[:-4] + ".gpl"
        if os.path.exists(outgpl):
            print("ERROR -> {} already in current directory".format(outgpl))
            exit()
        outpng = self.xpmfile[:-4] + ".png"

        ## write gnuplot scripts
        gpl_lines = "set term png\n"
        gpl_lines += """set output "{}" \n""".format(outpng)
        gpl_lines += "unset colorbox\n"
        pal_line = "set pal defined("
        for index, color in enumerate(self.colors):
            pal_line += """{} "{}",""".format(index, color)
        pal_line = pal_line.strip(",") + ")"
        gpl_lines += pal_line + "\n\n"
        ## add data lines
        gpl_lines += "$data << EOD\n"
        for l in range(len(self.xpm_datalines)):
            for i in range(
                0, self.xpm_width * self.xpm_char_per_pixel, self.xpm_char_per_pixel
            ):
                value = self.chars.index(
                    self.xpm_datalines[l][i : i + self.xpm_char_per_pixel]
                )
                gpl_lines += "{:.6f} {:.6f} {:.6f}\n".format(
                    self.xpm_xaxis[int(i / self.xpm_char_per_pixel)],
                    self.xpm_yaxis[l],
                    value,
                )
        gpl_lines += "EOD\n\n"
        ## add tail part of gpl file
        gpl_lines += "#set tmargin at screen 0.95\n"
        gpl_lines += "#set bmargin at screen 0.20\n"
        gpl_lines += "#set rmargin at screen 0.85\n"
        y_posi = 0.92
        for index, note in enumerate(self.notes):
            label_line = """#set label "{:10}" at screen 0.85,{:.2f} left textcolor rgb "{}"\n""".format(
                note, y_posi, self.colors[index]
            )
            y_posi -= 0.10
            gpl_lines += label_line
        gpl_lines += """set term pngcairo enhanced truecolor font "Arial,85" """
        gpl_lines += """fontscale 1 linewidth 20 pointscale 5 size 10000,6000\n"""
        gpl_lines += "set tics out nomirror;\n"
        gpl_lines += "set key out reverse Left spacing 2 samplen 1/2\n"
        gpl_lines += """set title "{}"\n""".format(self.xpm_title)
        gpl_lines += """set xlabel "{}"; set ylabel "{}";\n""".format(
            self.xpm_xlabel, self.xpm_ylabel
        )
        gpl_lines += """plot [{:.2f}:{:.2f}] [{:.2f}:{:.2f}] $data u 1:2:3 w imag notit, \\\n""".format(
            math.floor(min(self.xpm_xaxis) * 10.0) / 10.0 - 0.1,
            math.ceil(max(self.xpm_xaxis) * 10.0) / 10.0 + 0.1,
            math.floor(min(self.xpm_yaxis) * 10.0) / 10.0 - 0.1,
            math.ceil(max(self.xpm_yaxis) * 10.0) / 10.0 + 0.1,
        )
        for index, note in enumerate(self.notes):
            gpl_lines += """{} w p ps 3 pt 5 lc rgb "{}" t"{}", \\\n""".format(
                math.floor(min(self.xpm_yaxis)) - 1, self.colors[index], note
            )
        gpl_lines = gpl_lines.strip("\n").strip("\\").strip().strip(",")

        ## write gpl files
        with open(outgpl, "w") as fo:
            fo.write(gpl_lines + "\n")

        print(
            "Info -> write gnuplot scripts {} from {} successfully".format(
                outgpl, self.xpmfile
            )
        )

    def draw_origin(
        self, IP: bool = False, outputpng: str = None, noshow: bool = False
    ) -> None:
        """draw xpm figure by plt.imshow
        IP : whether to interpolation
        outputpng: the name for figure output
        noshow: whether not to show figure, useful for PC without gui
        """

        ## check parameters
        if outputpng != None and os.path.exists(outputpng):
            print("ERROR -> {} already in current directory".format(outputpng))
            exit()

        # visualization of xpm
        if IP == False:
            img = []
            for line in self.xpm_datalines:
                rgb_line = []
                for i in range(
                    0, self.xpm_width * self.xpm_char_per_pixel, self.xpm_char_per_pixel
                ):
                    rgb_line.append(
                        self.colors_rgb[
                            self.chars.index(line[i : i + self.xpm_char_per_pixel])
                        ]
                    )
                img.append(rgb_line)

            plt.imshow(img, aspect="auto")
            
            if self.xpm_type != "Continuous":
                legend_patches = []
                for ind, note in enumerate(self.notes):
                    leg_patch = patches.Patch(color=self.colors[ind], label=note)
                    legend_patches.append(leg_patch)
                plt.legend(handles=legend_patches, bbox_to_anchor=(1.02,  1.00), 
                        loc="upper left", borderaxespad=0)
                plt.tight_layout()


        if IP == True:
            if self.xpm_type != "Continuous":
                print("ERROR -> Only Continuous type xpm file can interpolation")
                exit()
            ## show figure with interpolation
            imgIP = []
            for line in self.xpm_datalines:
                value_line = []
                for i in range(
                    0, self.xpm_width * self.xpm_char_per_pixel, self.xpm_char_per_pixel
                ):
                    value_line.append(
                        float(
                            self.notes[
                                self.chars.index(line[i : i + self.xpm_char_per_pixel])
                            ]
                        )
                    )
                imgIP.append(value_line)

            im = plt.imshow(imgIP, cmap="jet", interpolation="bilinear", aspect="auto")
            plt.colorbar(im, label=self.xpm_legend)

        ## TODO: find a better way to solve problem of ticks
        ## set the ticks
        x_tick, y_tick = 3, 3
        xpm_xticks = ["{:.1f}".format(x) for x in self.xpm_xaxis]
        xpm_yticks = ["{:.1f}".format(y) for y in self.xpm_yaxis]
        if self.xpm_width < 100:
            x_tick = int(self.xpm_width / 3)
        elif self.xpm_width >= 100 and self.xpm_width < 1000:
            x_tick = int(self.xpm_width / 5)
        elif self.xpm_width > 500:
            x_tick = int(self.xpm_width / 10)
        if self.xpm_height < 100:
            y_tick = int(self.xpm_height / 3)
        elif self.xpm_height >= 100 and self.xpm_height < 1000:
            y_tick = int(self.xpm_height / 5)
        elif self.xpm_height > 500:
            y_tick = int(self.xpm_height / 10)
        if self.xpm_width / self.xpm_height > 10:
            y_tick = int(self.xpm_height / 2)
        if self.xpm_height / self.xpm_width > 10:
            x_tick = int(self.xpm_width / 2)
        plt.tick_params(axis="both", which="major")
        plt.xticks(
            [0]
            + [w for w in range(x_tick, self.xpm_width - int(x_tick / 2), x_tick)]
            + [self.xpm_width - 1],
            [xpm_xticks[0]]
            + [
                xpm_xticks[w]
                for w in range(x_tick, self.xpm_width - int(x_tick / 2), x_tick)
            ]
            + [xpm_xticks[-1]],
        )
        plt.yticks(
            [0]
            + [h for h in range(y_tick, self.xpm_height - int(y_tick / 2), y_tick)]
            + [self.xpm_height - 1],
            [xpm_yticks[0]]
            + [
                xpm_yticks[h]
                for h in range(y_tick, self.xpm_height - int(y_tick / 2), y_tick)
            ]
            + [xpm_yticks[-1]],
        )

        ## set other infos in the figure
        plt.title(self.xpm_title)
        plt.xlabel(self.xpm_xlabel)
        plt.ylabel(self.xpm_ylabel)
        print("Legend of this xpm figure -> ", self.xpm_legend)

        if outputpng != None:
            plt.savefig(outputpng, dpi=300)
        if noshow == False:
            plt.show()

    def draw_pcm(
        self, IP: bool = False, outputpng: str = None, noshow: bool = False
    ) -> None:
        """draw xpm figure by pcolormesh (with interpolation)
        IP : whether to interpolation
        outputpng: the name for figure output
        noshow: whether not to show figure, useful for PC without gui
        """

        ## check parameters
        if outputpng != None and os.path.exists(outputpng):
            print("ERROR -> {} already in current directory".format(outputpng))
            exit()

        if self.xpm_type != "Continuous":
            print("ERROR -> Only Continuous type xpm file can interpolation")
            exit()

        ## convert xpm_data to img (values)
        img = []
        for line in self.xpm_datalines:
            value_line = []
            for i in range(
                0, self.xpm_width * self.xpm_char_per_pixel, self.xpm_char_per_pixel
            ):
                value_line.append(
                    float(
                        self.notes[
                            self.chars.index(line[i : i + self.xpm_char_per_pixel])
                        ]
                    )
                )
            img.append(value_line)

        if IP == False:
            plt.pcolormesh(
                self.xpm_xaxis, self.xpm_yaxis, img, cmap="jet", shading="auto"
            )
        elif IP == True:
            ## interpolation
            ip_func = interp2d(self.xpm_xaxis, self.xpm_yaxis, img, kind="linear")
            x_new = np.linspace(
                np.min(self.xpm_xaxis), np.max(self.xpm_xaxis), 10 * len(self.xpm_xaxis)
            )
            y_new = np.linspace(
                np.min(self.xpm_yaxis), np.max(self.xpm_yaxis), 10 * len(self.xpm_yaxis)
            )
            value_new = ip_func(x_new, y_new)
            x_new, y_new = np.meshgrid(x_new, y_new)
            ## show figure
            plt.pcolormesh(x_new, y_new, value_new, cmap="jet", shading="auto")

        ## set ticks and other figure infos
        ax = plt.gca()
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        plt.colorbar(label=self.xpm_legend)
        plt.title(self.xpm_title)
        plt.xlabel(self.xpm_xlabel)
        plt.ylabel(self.xpm_ylabel)
        print("Legend of this xpm figure -> ", self.xpm_legend)

        if outputpng != None:
            plt.savefig(outputpng, dpi=300)
        if noshow == False:
            plt.show()

    def draw_3D(
        self, IP: bool = False, outputpng: str = None, noshow: bool = False
    ) -> None:
        """draw xpm 3D figure (with interpolation)
        IP : whether to interpolation
        outputpng: the name for figure output
        noshow: whether not to show figure, useful for PC without gui
        """

        ## check parameters
        if outputpng != None and os.path.exists(outputpng):
            print("ERROR -> {} already in current directory".format(outputpng))
            exit()

        if self.xpm_type != "Continuous":
            print("ERROR -> Only Continuous type xpm file can draw 3D figure")
            exit()

        ## convert xpm_data to values
        values = []
        for line in self.xpm_datalines:
            for i in range(
                0, self.xpm_width * self.xpm_char_per_pixel, self.xpm_char_per_pixel
            ):
                values.append(
                    float(
                        self.notes[
                            self.chars.index(line[i : i + self.xpm_char_per_pixel])
                        ]
                    )
                )
        xpm_xaxis = np.array(self.xpm_xaxis)
        xpm_yaxis = np.array(self.xpm_yaxis)
        img = np.array(values)

        ## draw 3d figure
        fig = plt.figure()
        ax = fig.gca(projection="3d")

        ## interpolation
        IP_value = 1
        if IP == False:
            IP_value = 1
        elif IP == True:
            IP_value = 12
        img = img.reshape(len(xpm_xaxis), len(xpm_yaxis))
        ip_func = interp2d(xpm_xaxis, xpm_yaxis, img, kind="linear")
        x_new = np.linspace(
            np.min(xpm_xaxis), np.max(xpm_xaxis), IP_value * len(xpm_xaxis)
        )
        y_new = np.linspace(
            np.min(xpm_yaxis), np.max(xpm_yaxis), IP_value * len(xpm_yaxis)
        )
        img_new = ip_func(x_new, y_new)
        x_new, y_new = np.meshgrid(x_new, y_new)
        img_new = img_new.reshape(len(x_new), len(y_new))

        ## show figure
        ax.plot_surface(
            x_new,
            y_new,
            img_new,
            alpha=0.9,
            cmap="coolwarm",
            linewidth=0,
            antialiased=False,
        )
        ## set the 2d surface location
        ax.contourf(
            x_new,
            y_new,
            img_new,
            zdir="z",
            offset=math.floor(min(values)) - math.floor(max(values) - min(values)) / 30,
            cmap="coolwarm",
        )

        ## set the axis ticks and other figure infos
        ax.zaxis.set_major_locator(AutoLocator())
        ax.zaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        # ax.set_zlim(0, )
        # plt.colorbar(surf, shrink=0.6, aspect=12, label=self.xpm_legend)
        plt.title(self.xpm_title)
        ax.set_xlabel(self.xpm_xlabel)
        ax.set_ylabel(self.xpm_ylabel)
        ax.set_zlabel(self.xpm_legend)
        print("Legend of this xpm figure -> ", self.xpm_legend)

        if outputpng != None:
            plt.savefig(outputpng, dpi=300)
        if noshow == False:
            plt.show()


def xpm_combine(
    xpm_files: list = [], outputpng: str = None, noshow: bool = False
) -> None:
    """Combination of xpm files, still in construction, not suggest to use it
    xpm_file_list : a list contains all xpm file names
    outputpng : the name for figure output
    noshow: whether not to show figure, useful for PC without gui
    """

    ###################### bolzmann
    #### G(x) = -kT*Ln(P(x)) + c
    ######################

    x_list, y_list = [], []
    xpm_title, xpm_legend, xpm_xlabel, xpm_ylabel = "", "", "", ""
    for file in xpm_files:
        xpm = XPM(file)
        xpm_title = xpm.xpm_title
        xpm_legend = xpm.xpm_legend
        xpm_xlabel = xpm.xpm_xlabel
        xpm_ylabel = xpm.xpm_ylabel
        if xpm.xpm_type != "Continuous":
            print("ERROR -> can not combine xpm whose type is not Continuous")
            exit()
        scatter_x, scatter_y, _, _, _ = xpm.get_scatter_data()
        x_list += scatter_x
        y_list += scatter_y

    ## combine xpm
    # plt.scatter(x_list, y_list)
    # plt.show()
    heatmap, xedges, yedges = np.histogram2d(x_list, y_list, bins=800)
    heatmap = gaussian_filter(heatmap, sigma=16)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # if you set origin="lower", no need to reverse yaxis any more
    plt.imshow(heatmap.T, origin="lower", extent=extent, cmap="jet_r")
    plt.xlim(extent[0], extent[1])
    plt.ylim(extent[2], extent[3])

    ## set ticks and other figure infos
    ax = plt.gca()
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    plt.title(xpm_title)
    plt.xlabel(xpm_xlabel)
    plt.ylabel(xpm_ylabel)
    print("Legend of this xpm figure -> ", xpm_legend)

    if outputpng != None and os.path.exists(outputpng):
        print("ERROR -> {} already in current directory".format(outputpng))
        exit()
    if outputpng != None:
        plt.savefig(outputpng, dpi=300)
    if noshow == False:
        plt.show()


def xpm_call_functions(arguments: list = None):
    """call functions of xpm module"""
    if arguments == None:
        arguments = [argv for argv in sys.argv]

    ## parse the command parameters
    parser = argparse.ArgumentParser(description="Process xpm files generated by GMX")
    parser.add_argument("-f", "--input", help="input your xpm file")
    parser.add_argument("-o", "--output", help="file name to output")
    parser.add_argument("-x", "--xlabel", type=str, help="the xlabel of figure")
    parser.add_argument("-y", "--ylabel", type=str, help="the ylabel of figure")
    parser.add_argument("-t", "--title", type=str, help="the title of figure")
    parser.add_argument(
        "-xs", "--xshrink", type=str, help="modify x-axis by multipling xshrink"
    )
    parser.add_argument(
        "-ip",
        "--interpolation",
        action="store_true",
        help="whether to apply interpolation (only support Continuous type xpm)",
    )
    parser.add_argument(
        "-pcm",
        "--pcolormesh",
        action="store_true",
        help="whether to apply pcolormesh function to draw",
    )
    parser.add_argument(
        "-3d",
        "--threeDimensions",
        action="store_true",
        help="whether to draw 3D figure",
    )
    parser.add_argument(
        "-ns",
        "--noshow",
        action="store_true",
        help="whether not to show picture, useful on computer without gui",
    )
    parser.add_argument(
        "-c",
        "--combine",
        nargs="+",
        help="specify some xpm files to combine into one figure",
    )

    if len(arguments) < 2:
        print("Error -> no input parameters, -h or --help for help messages")
        exit()

    method = arguments[1]
    # print(method)
    if method in ["-h", "--help"]:
        parser.parse_args(arguments[1:])
        exit()
    args = parser.parse_args(arguments[2:])
    # for key, value in vars(args).items():
    #     print(key, value)

    inputxpm = args.input
    output = args.output
    ip = args.interpolation
    noshow = args.noshow
    pcm = args.pcolormesh
    fig_3d = args.threeDimensions
    xpms2combine = args.combine
    xlabel = args.xlabel
    ylabel = args.ylabel
    title = args.title
    xshrink = args.xshrink

    ## call functions
    if method == "xpm_show":
        if inputxpm == None:
            print("Error -> no input file")
            exit()
        xpm = XPM(inputxpm, xlabel, ylabel, title, xshrink)
        if fig_3d == True:
            xpm.draw_3D(ip, output, noshow)
        if pcm == False and fig_3d == False:
            xpm.draw_origin(ip, output, noshow)
        elif pcm == True and fig_3d == False:
            xpm.draw_pcm(ip, output, noshow)
    elif method == "xpm_combine":
        if xpms2combine == None:
            print("Error -> no input xpm files for combination")
            exit()
        xpm_combine(xpms2combine, output, noshow)
    elif method == "xpm2csv":
        xpm = XPM(inputxpm, xlabel, ylabel, title, xshrink)
        xpm.xpm2csv(output)
    elif method == "xpm2gpl":
        xpm = XPM(inputxpm, xlabel, ylabel, title, xshrink)
        xpm.xpm2gpl(output)
    else:
        print("Error -> Wrong method you specified")
        exit()

    print("Info -> good day !")


def main():
    xpm_call_functions()


if __name__ == "__main__":
    main()
