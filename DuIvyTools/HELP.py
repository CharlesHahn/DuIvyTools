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

:examples: 
    dit xvg_show -f test.xvg

:parameters:
    -f, --input
            specify the xvg file for input
""",
            "xvg_compare": """
xvg_compare: comparison of xvg files, draw different data columns into line figure.

:examples:
    dit xvg_compare -f f1.xvg f2.xvg -c 1,2 2,3,4 -l l1 l2 l3 l4 l5
    dit xvg_compare -f f1.xvg f2.xvg -c 1 1 -l l1 l2 -x Time(ns) -y ylabel -t tile
    dit xvg_compare -f f1.xvg f2.xvg -c 1,2 2 -l l1 l2 l3 -s 100 -e 1000

:parameters:
    -f, --input
            specify the xvg files for input. accept more than input file names seperated
            by space
    -c, --column_select
            specify the index of columns you want to use. index starts from 0. 
            one xvg file in -f should be paired with one column index group seperated by
            space, and in each column index group, indexs should be seperated by comma. 
            In first example, 1,2 is paired with f1.xvg, 2,3,4 is paird with f2.xvg; 
            this means selecting the column 1 and 2 in f1.xvg, column 2, 3 and 4 in 
            f2.xvg to compare. 
    -l, --legend_list
            specify the legends to show in figure. The number of legends should be equal
            to the number of indexs you sepecified in -c. 
    -s, --start
            specify the row index of column data which you want to start to plot.
    -e, --end
            specify the row index of column data which you want to stop plotting.
    -x, --xlabel
            sepecify the x-label you want to show in figure
    -y, --ylabel
            sepecify the y-label you want to show in figure
    -t, --title
            sepecify the title you want to show in figure
    -smv, --showMV  
            if you specified this parameter, moving average and confidence interval 
            will be calculated and shown in figure. 
    -ws, --windowsize
            specify the windows size for moving average calculation. default == 50
            only valid when -smv specified. 
    -cf, --confidence
            specify the confidence for confidence interval calculation. default == 0.90
            only valid when -smv specified. 
    -a, --alpha
            specify the transparency for plotting confidence interval. default == 0.4
            only valid when -smv specified. 
""",
            "xvg_ave": """
xvg_ave: calculate the average of each column in xvg file

:examples:
    dit xvg_ave -f f1.xvg
    dit xvg_ave -f f1.xvg -s 1000 -e 2000

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -s, --start
            specify the row index of column data which you want to start to calculation.
    -e, --end
            specify the row index of column data which you want to stop calculation.
""",
            "xvg_mvave": """
xvg_mvave: calculate the moving average of each column in xvg file and save results to csv file.

:examples:
    dit xvg_mvave -f f1.xvg -o res.csv 
    dit xvg_mvave -f f1.xvg -o res.csv -ws 20 -cf 0.95

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -o, --output
            specify the csv file to save results.
    -ws, --windowsize
            specify the windows size for moving average calculation. default == 50
    -cf, --confidence
            specify the confidence for confidence interval calculation. default == 0.90
""",
            "xvg2csv": """
xvg2csv: convert xvg file into csv file.

:examples:
    dit xvg2csv -f f1.xvg -o res.csv

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -o, --output
            specify the csv file to save results.
""",
            "xvg_rama": """
xvg_rama: draw ramachandran figure from a rama data xvg file.

:examples:
    dit xvg_rama -f rama.xvg

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
""",
            "xvg_show_distribution": """
xvg_show_distribution: calculate distribution of each column in xvg file and show.

:examples:
    dit xvg_show_distribution -f f1.xvg
    dit xvg_show_distribution -f f1.xvg -bin 100

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -bin, --bin
            specify the number of bins of calculating distribution. default == 100
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
