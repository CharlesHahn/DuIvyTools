"""
Commands module is part of DuIvyTools providing basic Commands class.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class Command(log):
    def __init__(self) -> None:
        pass

    def sel_parm(self, *args) -> None:

        if len(args) < 1:
            self.critical("wrong length of parameters selcetion")
        for item in args:
            if item != None:
                return item
        else:
            return args[0]

    def get_parm(self, key: str) -> None:
        value = self.parm.__dict__.get(key, None)
        if value != None:
            return value
        value = self.file.__dict__.get(key, None)
        if value != None:
            return value
        return None

    def deal_latex(self, ori: str, with_dollar: bool = True) -> None:
        ## deal with subscripts or superscripts
        res = ori[:]
        if "\\s" in res and "\\N" in res:
            res = res.replace("\\s", "_{")
            res = res.replace("\\N", "}")
        if "\\S" in res and "\\N" in res:
            res = res.replace("\\s", "^{")
            res = res.replace("\\N", "}")
        if with_dollar:
            res = f"${res}$"
        return res

    def remove_latex(self) -> None:
        if self.parm.engine in ["matplotlib", "plotly"]:
            self.file.data_heads = [self.deal_latex(h) for h in self.file.data_heads]
            self.file.xlabel = self.deal_latex(self.file.xlabel)
            self.file.ylabel = self.deal_latex(self.file.ylabel)
        elif self.parm.engine == "gnuplot":
            self.file.data_heads = [
                self.deal_latex(h, with_dollar=False) for h in self.file.data_heads
            ]
            self.file.xlabel = self.deal_latex(self.file.xlabel, with_dollar=False)
            self.file.ylabel = self.deal_latex(self.file.ylabel, with_dollar=False)
