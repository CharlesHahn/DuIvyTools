"""
Commands module is part of DuIvyTools providing basic Commands class.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union, Any

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class Command(log):
    def __init__(self) -> None:
        pass

    def sel_parm(self, *args) -> Any:
        """select the first parameters which is not None from *args, return the first item if all None

        Returns:
            Any: the first not None parm, or the first item if all None
        """
        if len(args) < 1:
            self.critical("wrong length of parameters selcetion")
        for item in args:
            if item != None:
                return item
        else:
            return args[0]

    def get_parm(self, key: str) -> Any:
        """get parm from user input (self.parm) or data file (self.file), user input with higher priority

        Args:
            key (str): properties of class

        Returns:
            Any: value of class properties
        """
        value = self.parm.__dict__.get(key, None)
        if value != None:
            return value
        value = self.file.__dict__.get(key, None)
        if value != None:
            return value
        return None

    def deal_latex(
        self, ori: str, with_dollar: bool = True, ignore_slash: bool = False
    ) -> str:
        """deal with subscripts or superscripts inside strings

        Args:
            ori (str): the string to process
            with_dollar (bool, optional): add $ around result. Defaults to True.
            ignore_slash (bool, optional): ture \\ into / to avoid errors. Defaults to False.

        Returns:
            str: result string
        """
        ## deal with subscripts or superscripts
        latex_found_flag:bool = False
        res = ori[:]
        if "\\s" in res and "\\N" in res:
            res = res.replace("\\s", "_{")
            res = res.replace("\\N", "}")
            latex_found_flag = True
        if "\\S" in res and "\\N" in res:
            res = res.replace("\\s", "^{")
            res = res.replace("\\N", "}")
            latex_found_flag = True
        if "^" in res:
            latex_found_flag = True
        if with_dollar and res and latex_found_flag:
            res = f"${res}$"
        if ignore_slash:
            res = res.replace("\\", "/")
        return res

    def remove_latex(self) -> None:
        """remove the super-/sub-scripts in data_heads, xlabel, and ylabel of data files"""
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

    def remove_latex_msgs(self, msgs: List[str]) -> List[str]:
        """for a list, deal with super-/sub-scripts of each item

        Args:
            msgs (List[str]): the strings to process

        Returns:
            List[str]: the results
        """
        if self.parm.engine in ["matplotlib", "plotly"]:
            msgs = [self.deal_latex(m, True, True) for m in msgs]
        elif self.parm.engine == "gnuplot":
            msgs = [self.deal_latex(m, False, True) for m in msgs]
        return msgs

    def check_output_exist(self, output:str) -> str:
        """check if the output file exists in current working directory. If true, add time stamp to its name

        Args:
            output (str): the output file name

        Returns:
            str: the fine output file name
        """
        if os.path.exists(output):
            time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())
            new_output = f'{".".join(output.split(".")[:-1])}_{time_info}.{output.split(".")[-1]}'
            self.warn(
                f"{output} is already in current directory, save to {new_output} for instead."
            )
            output = new_output
        return output
    