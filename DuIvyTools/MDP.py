""" MDP module is part of DuIvyTools library, which is a tool for analysis and visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to generate .mdp file templates. 

This MDP module contains:
    - MDP class

This file is provided to you by GPLv2 license."""


import os
import sys
import argparse


class MDP(object):
    """
    """

    def __init__(self) -> None:
        pass

    def gen_em(self, outmdp:str) -> None:
        pass

    def gen_nvt(self, outmdp:str) -> None:
        pass

    def gen_npt(self, outmdp:str) -> None:
        pass

    def gen_md(self, outmdp:str) -> None:
        pass


def mdp_gen_em(outmdp:str) -> None:
    pass

def mdp_gen_nvt(outmdp:str) -> None:
    pass

def mdp_gen_npt(outmdp:str) -> None:
    pass

def mdp_gen_md(outmdp:str) -> None:
    pass



def mdp_call_functions(arguments: list = None):
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]

    ## parse the command parameters
    parser = argparse.ArgumentParser(description="generate mdp file templates")
    parser.add_argument("-o", "--outputfile", help="file name to output")
    if len(arguments) < 2:
        print("Error -> no input parameters, -h or --help for help messages")
        exit()
    method = arguments[1]
    # print(method)
    if method in ["-h", "--help"]:
        parser.parse_args(arguments[1:])
        exit()
    args = parser.parse_args(arguments[2:])

    if method == "ndx_show":
        pass
    elif method == "ndx_rm_dup":
        pass
    else:
        print("Error -> unknown method {}".format(method))
        exit()

    print("Info -> good day !")


def main():
    mdp_call_functions()


if __name__ == "__main__":
    main()
