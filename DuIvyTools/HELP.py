""" HELP module is part of DuIvyTools library, which is a tool for analysis and visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to provide help messages. 

This HELP module contains:
    - HELP class

This file is provided to you by GPLv2 license."""


import sys


class HELP(object):
    """ HELP class provides help infos about all method in DuIvyTools """
    
    def __init__(self) -> None:
        """ init all help messages """

        self.help_infos = {
            "xvg_show": """
xvg_show: draw xvg data into line figures.

:examples: dit xvg_show -f test.xvg

:parameters:
    -f, --input
            specify the xvg file for input
""",
            "xvg_compare": """

""",
            "xvg_ave": """

""",
            "xvg_mvave": """

""",
            "xvg2csv": """

""",
            "xvg_rama": """

""",
            "xvg_show_distribution": """

""",
            "xvg_show_stack": """

""",
            "xvg_show_scatter": """

""",
            "xvg_energy_compute": """

""",
            "xvg_combine": """

""",
            "xvg_ave_bar": """

""",
            "xvg_box": """

""",
            "xpm_show": """

""",
            "xpm2csv": """

""",
            "xpm2gpl": """

""",
            "xpm_combine": """

""",
            "ndx_show": """

""",
            "ndx_rm_dup": """

""",
            "ndx_rm": """

""",
            "ndx_preserve": """

""",
            "ndx_add": """

""",
            "ndx_combine": """

""",
            "ndx_rename": """

""",
            "mdp_gen": """

""",
        }

    def print_help_infos(self, method:str) -> None:
        """ print help messages """

        if method in self.help_infos.keys():
            print(self.help_infos[method])
        else:
            print("Error -> unknown method {}, type `dit help`".format(method))
            exit()


def print_help_msg(method:str) -> None:
    """ print help messages """

    help_class = HELP()
    help_class.print_help_infos(method)


def help_call_functions(arguments: list = None) -> None:
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]

    description = "\nHELP method provides help messages about all methods in DuIvyTools\n"
    description += "Type any methods below to find help messages:\n"
    description += "    XVG:\n"
    description += "        xvg_show, xvg_compare, xvg_ave, xvg_mvave, xvg2csv, xvg_rama\n"
    description += "        xvg_show_distribution, xvg_show_stack, xvg_show_scatter\n"
    description += "        xvg_energy_compute, xvg_combine, xvg_ave_bar, xvg_box\n"
    description += "    XPM:\n"
    description += "        xpm_show, xpm2csv, xpm2gpl, xpm_combine\n"
    description += "    NDX:\n"
    description += "        ndx_show, ndx_rm_dup, ndx_rm, ndx_preserve\n"
    description += "        ndx_add, ndx_combine, ndx_rename\n"
    description += "    MDP:\n"
    description += "        mdp_gen\n"

    if len(arguments) < 2:
        print("Error -> no input parameters, `dit help` for help messages")
        exit()
    elif len(arguments) == 2:
        if arguments[1] == "help":
            print(description)
        else:
            print("Error -> unknown command {}, `help` for help messages".format(
                arguments[1]))
    else:
        if arguments[1] != "help":
            print("Error -> unknown command {}".format(arguments[1]))
            exit()
        else:
            methods = arguments[2:]
            for method in methods:
                print_help_msg(method)


def main():
    help_call_functions()


if __name__ == "__main__":
    main()
