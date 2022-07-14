"""
This DIT module is part of DuIvyTools library. Written by CharlesHahn.

DIT module provides simple API and CLI commands for you to use conveniently. 

This file is provided to you under GPLv2 License.
"""


import sys
import logging
from DuIvyTools.XPM import xpm_call_functions
from DuIvyTools.XVG import xvg_call_functions
from DuIvyTools.NDX import ndx_call_functions
from DuIvyTools.MDP import mdp_call_functions
from DuIvyTools.HELP import help_call_functions
from DuIvyTools.PipiDistAng import pipi_dist_ang_call_functions
from DuIvyTools.FindCenter import find_center_call_functions
from DuIvyTools.HydrogenBond import hbond_call_functions
from DuIvyTools.MolMap import mol_map_call_functions

logging.basicConfig(level=logging.INFO, format="%(levelname)s -> %(message)s")
logger = logging.getLogger(__name__)


def main():
    arguments = [argv for argv in sys.argv]
    if len(sys.argv) < 2:
        DIT_infos = """

 *******           **                  **********               **        
/**////**         /**          **   **/////**///               /**        
/**    /** **   **/** **    **//** **     /**  ******   ****** /**  ******
/**    /**/**  /**/**/**   /** //***      /** **////** **////**/** **//// 
/**    /**/**  /**/**//** /**   /**       /**/**   /**/**   /**/**//***** 
/**    ** /**  /**/** //****    **        /**/**   /**/**   /**/** /////**
/*******  //******/**  //**    **         /**//****** //****** *** ****** 
///////    ////// //    //    //          //  //////   ////// /// //////  

DuIvyTools is a simple analysis and visualization tool for GROMACS result files
written by CharlesHahn (https://github.com/CharlesHahn/DuIvyTools). 

> Type `dit help` for more informations. 

"""

        print(DIT_infos)
        sys.exit()
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["help", "-h", "--help"]:
            help_call_functions(arguments)
        else:
            logging.error("unknown command {}, ".format(sys.argv[1]))
            logging.info("type `dit help` for more information")
            sys.exit()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "help":
            help_call_functions(arguments)
        elif sys.argv[2] in ["-h", "--help", "help"]:
            help_call_functions(["dit", "help", sys.argv[1]])
        else:
            logging.error("wrong command, type `dit help` for more information")
            sys.exit()
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
        elif method == "pipi_dist_ang":
            pipi_dist_ang_call_functions(arguments)
        elif method == "find_center":
            find_center_call_functions(arguments)
        elif method == "hbond":
            hbond_call_functions(arguments)
        elif method == "mol_map":
            mol_map_call_functions(arguments)
        else:
            logging.error("unknown command {}".format(method))


if __name__ == "__main__":
    main()
