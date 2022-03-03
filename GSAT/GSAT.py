"""This module is part of GMX_Simple_Analysis_Tool library. Written by CharlesHahn.

GSAT module provide some simple API and CLI commands for you to use conveniently. 

This module requires argparse. 

This file is provided to you under GPLv2 License"""


import sys
from XPM import xpm_call_functions
from XVG import xvg_call_functions



def main():
    method = sys.argv[1]
    arguments = [ argv for argv in sys.argv ]
    if method.startswith("xvg"):
        xvg_call_functions(arguments)
    elif method.startswith("xpm"):
        xpm_call_functions(arguments)
    else:
        print("Error -> unknown method {}".format(method))



if __name__ == "__main__":
    main()

