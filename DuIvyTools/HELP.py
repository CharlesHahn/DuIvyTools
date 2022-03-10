""" HELP module is part of DuIvyTools library, which is a tool for analysis and visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to provide help messages. 

This HELP module contains:
    - HELP class

This file is provided to you by GPLv2 license."""


import sys


class HELP(object):
    """HELP class provides help infos about all method in DuIvyTools"""

    def __init__(self) -> None:
        """init all help messages"""

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
            specify the xvg files for input. accept one or one more input file names 
            seperated by space
    -c, --column_select
            specify the index of columns you want to use. index starts from 0. 
            one xvg file in -f should be paired with one column index group seperated by
            space, and in each column index group, indexs should be seperated by comma. 
            In first example, 1,2 is paired with f1.xvg, 2,3,4 is paird with f2.xvg; 
            this means selecting the column 1 and 2 in f1.xvg, column 2, 3 and 4 in 
            f2.xvg to compare. 
    -l, --legend_list (optional)
            specify the legends to show in figure. The number of legends should be equal
            to the number of indexs you sepecified in -c. 
    -s, --start (optional)
            specify the row index of column data which you want to start to plot.
    -e, --end (optional)
            specify the row index of column data which you want to stop plotting.
    -x, --xlabel (optional)
            sepecify the x-label you want to show in figure
    -y, --ylabel (optional)
            sepecify the y-label you want to show in figure
    -t, --title (optional)
            sepecify the title you want to show in figure
    -smv, --showMV  (optional)
            if you specified this parameter, moving average and confidence interval 
            will be calculated and shown in figure. 
    -ws, --windowsize (optional)
            specify the windows size for moving average calculation. default == 50
            only valid when -smv specified. 
    -cf, --confidence (optional)
            specify the confidence for confidence interval calculation. default == 0.90
            only valid when -smv specified. 
    -a, --alpha (optional)
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
    -s, --start (optional)
            specify the row index of column data which you want to start to calculation.
    -e, --end (optional)
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
    -ws, --windowsize (optional)
            specify the windows size for moving average calculation. default == 50
    -cf, --confidence (optional)
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
    -bin, --bin (optional)
            specify the number of bins of calculating distribution. default == 100
""",
            "xvg_show_stack": """
xvg_show_stack: draw stack figure of column data.

:examples:
    dit xvg_show_stack -f f1.xvg
    dit xvg_show_stack -f f1.xvg -cis 2 -cie 4

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -cis, --column_index2start (optional)
            specify the index of column you want to start to stack. default == 1
    -cie, --column_index2end (optional)
            specify the index of column you want to stop stacking. 
""",
            "xvg_show_scatter": """
xvg_show_scatter: draw scatter figure

:examples:
    dit xvg_show_scatter -f f1.xvg -xi 0 -yi 1

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -xi, --x_index (optional)
            specify the index of column which you want to use as x data. default == 0
    -yi, --y_index (optional)
            specify the index of column which you want to use as y data. default == 1
""",
            "xvg_energy_compute": """
xvg_energy_compute: calculate the interaction energy between two items.

:examples:
    dit xvg_energy_compute -f prolig.xvg pro.xvg lig.xvg -o energy_results.xvg

:parameters:
    -f, --input
            specify three xvg files to calculate (complex energy file, component A 
            energy file and component B energy file). Each should contain and ONLY 
            contain five columns (Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip.)
    -o, --output
            specify a xvg file to save results. 
""",
            "xvg_combine": """
xvg_combine: select columns from xvg files and conbine data columns into one xvg file. 

:examples:
    dit xvg_combine -f f1.xvg -c 1,2 -o res.xvg
    dit xvg_combine -f f1.xvg f2.xvg -c 1,2 2,3 -o res.xvg

:parameters:
    -f, --input
            specify the xvg files for input. accept one or one more input file names 
            seperated by space
    -c, --column_select
            specify the index of columns you want to use. index starts from 0. 
            one xvg file in -f should be paired with one column index group seperated by
            space. And in each column index group, indexs should be seperated by comma. 
            In second example, 1,2 is paired with f1.xvg, 2,3 is paird with f2.xvg; 
            this means selecting the column 1 and 2 in f1.xvg, column 2 and 2 in 
            f2.xvg to combine, and saving results to res.xvg. 
    -o, --output
            specify a xvg file to save results of combination.
""",
            "xvg_ave_bar": """
xvg_ave_bar: First, the average of each data column you select by -c will be calculated.
             Second, the average and standard error of corresponding column averages in 
             xvg file groups will be calculated.
             Third, the averages and standard errors will be draw into bar figure.

:examples:
    dit xvg_ave_bar -f f1_1.xvg,f1_2.xvg,f1_3.xvg f2_1.xvg,f2_2.xvg,f2_3.xvg -c 1 2 
    dit xvg_ave_bar -f f1.xvg f2.xvg -c 1 2 -l l1 l2 -s 100 -e 1000 
    dit xvg_ave_bar -f f1.xvg f2.xvg -c 1 2 -l l1 l2 -x xlabel -y ylabel -t title
    dit xvg_ave_bar -f f1.xvg f2.xvg f3.xvg -c 1 2 -l l1 l2 l3 -xt xt1 xt2
    dit xvg_ave_bar -f f1.xvg f2.xvg -c 1 2 -l l1 l2 -ac -o average.csv

:parameters:
    -f, --input
            specify the xvg files for input. accept one or one more file names or file 
            name groups. Several file names seperated by comma is called a file name 
            group. In first example, f1_1.xvg,f1_2.xvg,f1_3.xvg is the first file name 
            group, and f2_1.xvg,f2_2.xvg,f2_3.xvg is the second file name group. 
            This method will calculate averages of columns you select in each xvg file.
            Then calculate the average and standard error of column averages in each 
            file group. Finally, convert the averages and standard errors into bar plot.
    -c, --column_select
            specify the index of columns you want to calculate. Index starts from 0. 
            The column indexs you select will be applied to EVERY xvg file in -f.
    -l, --legend_list (optional)
            specify the legends to show in figure. The number of legends should be equal
            to the number of files or file groups you specified in -f. 
    -xt, --xtitles (optional)
            specity the names of x ticks in figure. The number of xtitles should be 
            equal to the number of indexs in column_select (-c).
    -s, --start (optional)
            specify the row index of column data which you want to start to calculation.
    -e, --end (optional)
            specify the row index of column data which you want to stop calculation.
    -x, --xlabel (optional)
            sepecify the x-label you want to show in figure
    -y, --ylabel (optional)
            sepecify the y-label you want to show in figure
    -t, --title (optional)
            sepecify the title you want to show in figure
    -ac, --ave2csv (optional)
            whether save data of averages into csv file. default == False
    -o, --output (optional)
            if you specified -ac, -o should be used to specify the csv file name.
""",
            "xvg_box": """
xvg_box: draw the data of columns you select into box figure.

:examples:
    dit xvg_box -f f1.xvg f2.xvg f3.xvg -c 1 2 -xt xt1 xt2 -s 100 -e 1000
    dit xvg_box -f f1.xvg f2.xvg -c 1 2 3 -xt xt1 xt2 xt3 -x xlabel -y ylabel -t title

:parameters:
    -f, --input
            accept one or more than one files as input.
    -c, --column_select
            specify the column indexs you want to plot. The indexs you specified will
            be applied to each file you select in -f.
    -xt, --xtitles (optional)
            specity the names of x ticks in figure. The number of xtitles should be 
            equal to the number of indexs in column_select (-c).
    -s, --start (optional)
            specify the row index of column data which you want to start to calculation.
    -e, --end (optional)
            specify the row index of column data which you want to stop calculation.
    -x, --xlabel (optional)
            sepecify the x-label you want to show in figure
    -y, --ylabel (optional)
            sepecify the y-label you want to show in figure
    -t, --title (optional)
            sepecify the title you want to show in figure
""",
            "xpm_show": """
xpm_show: vasualize the xpm file.

:examples:
    dit xpm_show -f f1.xpm 
    dit xpm_show -f f1.xpm -ip 
    dit xpm_show -f f1.xpm -pcm 
    dit xpm_show -f f1.xpm -3d
    dit xpm_show -f f1.xpm -o test.png -ns 

:parameters:
    -f, --input
            specify the xpm file for input. 
    -o, --output (optional)
            specify the output figure name. 
    -ip, --interpolation (optional)
            whether to perform interpolation which will make your figure looks better.
    -pcm, --pcolormesh (optional)
            whether to use pcolormesh function to vasualize your xpm figure.
    -3d, --threeDimensions (optional)
            whether to draw a 3D figure. Useful for free energy landscape figure.
    -ns, --noshow (optional)
            whether not to show figure in GUI, useful when working without GUI.
""",
            "xpm2csv": """
xpm2csv: convert xpm file into csv data file. 
         when number of x-axis (or y-axis) is 1 more than width (or height) of figure, 
         the intermediate value of two adjacent values of x-axis (or y-axis) will be 
         calculated to suit the width (or height).

:examples:
    dit xpm2csv -f f1.xpm -o test.csv

:parameters:
    -f, --input
            specify the xpm file for input. 
    -o, --output
            specify the output csv file name.
""",
            "xpm2gpl": """
xpm2csv: convert xpm file into gnuplot script.

:examples:
    dit xpm2csv -f f1.xpm -o test.gpl

:parameters:
    -f, --input
            specify the xpm file for input. 
    -o, --output
            specify the output gnuplot script file name.
""",
            "xpm_combine": """
xpm_combine: combine several xpm files into one figure. 
             STILL WORKING ON IT. NOT RECOMMAND TO USE IT !!!

:examples:
    dit xpm_combine -c f1.xpm f2.xpm
    dit xpm_combine -c f1.xpm f2.xpm -o test.png -ns

:parameters:
    -c, --combine
            specify several xpm files for input. 
    -o, --output
            specify the output figure name. 
    -ns, --noshow (optional)
            whether not to show figure in GUI, useful when working without GUI.
""",
            "ndx_show": """
ndx_show: print all group names in ndx file you specified.

:examples:
    dit ndx_show -f f1.ndx

:parameters:
    -f, --input
            specify the ndx file for input. 
""",
            "ndx_rm_dup": """
ndx_rm_dup: remove all duplicated groups in ndx file.

:examples:
    dit ndx_rm_dup -f f1.ndx -o res.ndx

:parameters:
    -f, --input
            specify the ndx file for input. 
    -o, --output
            specify the ndx file name for saving the results of romiving.
""",
            "ndx_rm": """
ndx_rm: remove index groups according to names you specified.

:examples:
    dit ndx_rm -f f1.ndx -o res.ndx -gl Protein SOL System
    dit ndx_rm -f f1.ndx -o res.ndx -int

:parameters:
    -f, --input
            specify the ndx file for input. 
    -o, --output
            specify the ndx file name for saving the results.
    -gl, --grouplist (optional)
            specify the group names you want to remove. Seperated by space.
    -int, --interactive (optional)
            specify the group names you want to remove by interactive mode.
""",
            "ndx_preserve": """
ndx_preserve: preserve index groups according to names you specified, and remove others.

:examples:
    dit ndx_preserve -f f1.ndx -o res.ndx -gl Protein SOL System
    dit ndx_preserve -f f1.ndx -o res.ndx -int

:parameters:
    -f, --input
            specify the ndx file for input. 
    -o, --output
            specify the ndx file name for saving the results.
    -gl, --grouplist (optional)
            specify the group names you want to preserve. Seperated by space.
    -int, --interactive (optional)
            specify the group names you want to preserve by interactive mode.
""",
            "ndx_add": """
ndx_add: add one index group to ndx file by specified group name, start, end, step.

:examples:
    dit ndx_add -f f1.ndx -o res.ndx -gn test -s 1 -e 10 -t 2

:parameters:
    -f, --input (optional)
            specify ndx file for input. -f could be ignored if you want a new ndx file.
    -o, --output
            specify the ndx file name for saving the results.
    -gn, --groupname
            specify the name of index group you want to add.
    -s, --start
            specify the start index of the group you want to add.
    -e, --end
            specify the end index of the group you want to add.
    -t, --step (optional)
            specify the step of indexs of the group you want to add. default == 1
            In the example, -s 1 -e 10 -t 2 means to generate a group contains index:
            1 3 5 7 9 
""",
            "ndx_combine": """
ndx_combine: combine groups into one group by the group names you specified.
             I recommand you to use gmx make_ndx command to do this.

:example:
    dit ndx_combine -f f1.ndx -o res.ndx -gn combined_group -gl Protein Ligand

:parameters:
    -f, --input
            specify the ndx file for input. 
    -o, --output
            specify the ndx file name for saving the results.
    -gn, --groupname
            specify the name of combined index group.
    -gl, --grouplist
            specify the group names you want to combine. Seperated by space.
""",
            "ndx_rename": """
ndx_rename: rename groups in ndx file.

:examples:
    dit ndx_rename -f f1.ndx -o res.ndx -on Protein -nn test
    dit ndx_rename -f f1.ndx -o res.ndx -int

:parameters:
    -f, --input
            specify the ndx file for input. 
    -o, --output
            specify the ndx file name for saving the results.
    -on, --oldname (optional)
            specify the old name of group you want to rename.
    -nn, --newname (optional)
            specify a new name for the group you renamed.
    -int, --interactive (optional)
            rename groups in interactive mode.
""",
            "mdp_gen": """
mdp_gen: generate a template mdp file by application you specified. The mdp file 
         generated may NOT be appropriate for your system, CHECK IT YOURSELF.

:examples:
    dit mdp_gen -o em.mdp -a em
    dit mdp_gen -o npt.mdp -a npt

:parameters:
    -o, --output
            specify an output mdp file to save the results.
    -a, --application
            specify the applications you want to use mdp file for. You can select from:
            ions, em, nvt, npt, md, blank
""",
        }

    def print_help_infos(self, method: str) -> None:
        """print help messages"""

        if method in self.help_infos.keys():
            print(self.help_infos[method])
        else:
            print(
                "Error -> unknown method {}, type `dit help` for more infos.".format(
                    method
                )
            )
            exit()


def print_help_msg(method: str) -> None:
    """print help messages"""

    help_class = HELP()
    help_class.print_help_infos(method)


def help_call_functions(arguments: list = None) -> None:
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]

    description = "HELP method provides help infos about all methods in DuIvyTools\n"
    description += "Type any methods below to show help messages:\n"
    description += "like: `dit help xvg_show` or `dit xvg_show -h`\n"
    description += "    XVG:\n"
    description += "        xvg_show, xvg_compare, xvg_ave, xvg_mvave, "
    description += "xvg2csv, xvg_rama\n"
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
        print("DuIvyTools is a simple analysis and visualization tool ", end="")
        print("for GROMACS result files.")
        print("Info -> type `dit help` for more messages")
        exit()
    elif len(arguments) == 2:
        if arguments[1] in ["help", "-h", "--help"]:
            print(description)
        else:
            print("Error -> unknown command, type `dit help` for more information")
            exit()
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
