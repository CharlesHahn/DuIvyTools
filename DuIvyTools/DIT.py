"""This module is part of DuIvyTools library. Written by CharlesHahn.

DIT module provide some simple API and CLI commands for you to use conveniently. 

This file is provided to you under GPLv2 License"""


import sys
from DuIvyTools.XPM import xpm_call_functions
from DuIvyTools.XVG import xvg_call_functions
from DuIvyTools.NDX import ndx_call_functions
from DuIvyTools.MDP import mdp_call_functions
from DuIvyTools.HELP import help_call_functions


def main():
    arguments = [argv for argv in sys.argv]
    if len(sys.argv) < 2:
        print("DuIvyTools is a simple analysis and visualization tool ", end="")
        print("for GROMACS result files.")
        print("Info -> type `dit help` for more messages")
        exit()
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["help", "-h", "--help"]:
            help_call_functions(arguments)
        else:
            print("Error -> unknown command, type `dit help` for more information")
            exit()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "help":
            help_call_functions(arguments)
        elif sys.argv[2] in ["-h", "--help", "help"]:
            help_call_functions(["dit", "help", sys.argv[1]])
        else:
            print("Error -> unknown command, type `dit help` for more information")
            exit()
    elif len(sys.argv) > 3:
        method = sys.argv[1]
        if method.startswith("xvg"):
            xvg_call_functions(arguments)
        elif method.startswith("xpm"):
            xpm_call_functions(arguments)
        elif method.startswith("ndx"):
            ndx_call_functions(arguments)
        elif method.startswith("mdp"):
            mdp_call_functions(arguments)
        elif method.startswith("help"):
            help_call_functions(arguments)
        else:
            print("Error -> unknown method {}".format(method))


if __name__ == "__main__":
    main()
