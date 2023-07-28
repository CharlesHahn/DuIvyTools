"""
xpmParser module is part of DuIvyTools for parsing the xpm file generated by GROMACS.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import math
import numpy as np
from typing import Dict, List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class XPM(log):
    def __init__(self, xpmfile: str, is_file: bool = True) -> None:
        if is_file:
            self.xpmfile: str = xpmfile
            with open(xpmfile, "r") as fo:
                content = fo.read()
        else:
            content = xpmfile

        self.title: str = ""
        self.legend: str = ""
        self.type: str = ""
        self.xlabel: str = ""
        self.ylabel: str = ""
        self.width: int = 0
        self.height: int = 0
        self.color_num: int = 0
        self.char_per_pixel: int = 0
        self.chars: list[str] = []
        self.colors: list[str] = []
        self.notes: list[str] = []
        self.xaxis: list[float] = []
        self.yaxis: list[float] = []
        self.datalines: list[str] = []
        self.dot_matrix: list[list[str]] = []
        self.value_matrix: list[list[float]] = []

        lines = [l.strip() for l in content.split("\n")]
        flag_4_code: int = 0
        for line in lines:
            if flag_4_code == 1:
                flag_4_code = 2
                code4 = [int(c) for c in line.strip(' ,"').split()]
                self.width = code4[0]
                self.height = code4[1]
                self.color_num = code4[2]
                self.char_per_pixel = code4[3]
                continue
            elif (flag_4_code == 0) and line.startswith("static char"):
                flag_4_code = 1
                continue
            ## parsing comments and axis parts
            if line.startswith("/* x-axis"):
                self.xaxis += [float(n) for n in line.strip().split()[2:-1]]
                continue
            elif line.startswith("/* y-axis"):
                self.yaxis += [float(n) for n in line.strip().split()[2:-1]]
                continue
            elif line.startswith("/* title"):
                self.title = line.strip().split('"')[1]
                continue
            elif line.startswith("/* legend"):
                self.legend = line.strip().split('"')[1]
                continue
            elif line.startswith("/* x-label"):
                self.xlabel = line.strip().split('"')[1]
                continue
            elif line.startswith("/* y-label"):
                self.ylabel = line.strip().split('"')[1]
                continue
            elif line.startswith("/* type"):
                self.type = line.strip().split('"')[1]
                continue

            items = line.strip().split()
            ## for char-color-note part
            if len(items) == 7 and items[1] == "c":
                self.colors.append(items[2])
                self.notes.append(items[5].strip('"'))
                if len(items[0].strip('"')) == self.char_per_pixel:
                    self.chars.append(items[0].strip('"'))
                ## deal with blank char
                if len(items[0].strip('"')) < self.char_per_pixel:
                    char_item = line.strip('"')[: self.char_per_pixel]
                    self.chars.append(char_item)
                continue

            ## for figure content part
            if line.strip().startswith('"') and (
                len(line.strip().strip(",").strip('"'))
                == self.width * self.char_per_pixel
            ):
                self.datalines.append(line.strip().strip(",").strip('"'))

        ## check infos
        if self.color_num != len(self.chars):
            self.error(f"length of chars != color_num")
        if self.color_num != len(self.colors):
            self.error(f"length of colors != color_num")
        if self.color_num != len(self.notes):
            self.error(f"length of notes != color_num")
        if len(self.xaxis) != self.width and len(self.xaxis) != self.width + 1:
            self.error(
                f"length of xaxis ({len(self.xaxis)}) != xpm width ({self.width}) or xpm width +1"
            )
        if len(self.yaxis) != self.height and len(self.yaxis) != self.height + 1:
            self.error(
                f"length of yaxis ({len(self.yaxis)}) != xpm height ({self.height}) or xpm height +1"
            )
        if len(self.datalines) != self.height:
            self.error(
                f"rows of data ({len(self.datalines)}) is not equal to xpm height ({self.height}), check it!"
            )

        ## convert data
        if len(self.xaxis) == self.width + 1:
            self.xaxis = [
                (self.xaxis[i - 1] + self.xaxis[i]) / 2.0
                for i in range(1, len(self.xaxis))
            ]
            self.warn(
                "length of x-axis is 1 more than xpm width, use intermediate value for instead. "
            )
        if len(self.yaxis) == self.height + 1:
            self.yaxis = [
                (self.yaxis[i - 1] + self.yaxis[i]) / 2.0
                for i in range(1, len(self.yaxis))
            ]
            self.warn(
                "length of y-axis is 1 more than xpm height, use intermediate value for instead. "
            )
        if self.type == "Continuous":
            self.notes = [float(n) for n in self.notes]

        self.yaxis.reverse()  # IMPORTANT! from high to low now

        for dataline in self.datalines:
            dot_list: List[str] = []
            value_list: List[float] = []
            for i in range(0, self.width * self.char_per_pixel, self.char_per_pixel):
                dot = dataline[i : i + self.char_per_pixel]
                dot_list.append(dot)
                if self.type == "Continuous":
                    value = self.notes[self.chars.index(dot)]
                else:
                    # for Discrete, value store the index of chars|notes|colors
                    value = self.chars.index(dot)
                value_list.append(value)
                self.dot_matrix.append(dot_list)
                self.value_matrix.append(value_list)

        if is_file:
            self.info(f"parsing data from {xpmfile} successfully !")
    
    def __sub__(self, other:XPM) -> XPM: # diff_map
        pass


class XPMS(log):
    def __init__(self, xpmfile: str) -> None:
        self.xpmfile: str = xpmfile
        self.frames: list[XPM] = []

        with open(xpmfile, "r") as fo:
            contents = fo.read()
        contents = contents.split("/* XPM */")
        contents = [f"/* XPM */\n{c}" for c in contents if c.strip() != ""]
        for content in contents:
            xpm = XPM(content, is_file=False)
            self.frames.append(xpm)
        self.info(f"parsing multi-frames data from {xpmfile} successfully !")

    def __len__(self) -> int:
        return len(self.frames)

    def __getitem__(self, index: int) -> XPM:
        return self.frames[index]

    def get_time_series(self) -> List[float]:

        times: float = []
        for xpm in self:
            if xpm.title.startswith("t="):
                times.append(int(xpm.title[2:-2]))
            else:
                self.error(f"cannot parse time info from xpm title {xpm.title}")
        return times


def main():
    xpm = XPM("../../test/dm.xpm")
    print(xpm.title)
    print(xpm.legend)
    print(xpm.type)
    print(xpm.xlabel)
    print(xpm.ylabel)
    print(xpm.width)
    print(xpm.height)
    print(xpm.color_num)
    print(xpm.char_per_pixel)
    print(xpm.chars)
    print(xpm.colors)
    print(xpm.notes)
    # print(xpm.xaxis)
    # print(xpm.yaxis)
    # print(xpm.datalines)
    # print(xpm.dot_matrix)
    # print(xpm.value_matrix)

    xpms = XPMS("../../test/dmf.xpm")
    for xpm in xpms:
        print(xpm.title)
        print(xpm.legend)
        print(xpm.type)
        print(xpm.xlabel)
        print(xpm.ylabel)
        print(xpm.width)
        print(xpm.height)
        print(xpm.color_num)
        print(xpm.char_per_pixel)
        print(xpm.chars)
        print(xpm.colors)
        print(xpm.notes)
        # print(xpm.xaxis)
        # print(xpm.yaxis)
    print(xpms.get_time_series())

    xpm2 = XPM("../../test/hbond.xpm")
    print(xpm2.title)
    print(xpm2.legend)
    print(xpm2.type)
    print(xpm2.xlabel)
    print(xpm2.ylabel)
    print(xpm2.width)
    print(xpm2.height)
    print(xpm2.color_num)
    print(xpm2.char_per_pixel)
    print(xpm2.chars)
    print(xpm2.colors)
    print(xpm2.notes)
    # print(xpm2.xaxis)
    # print(xpm2.yaxis)
