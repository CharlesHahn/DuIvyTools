"""
HELP module is part of DuIvyTools library, which is a tool for analysis and 
visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to provide help messages. 

This HELP module contains:
    - HELP class
    - help_call_functions

This file is provided to you by GPLv3 license.
"""

import sys
import logging


class HELP(object):
    """HELP class provides help infos about all method in DuIvyTools"""

    def __init__(self) -> None:
        """init all help messages"""

        self.help_infos = {
            "xvg_show": """
xvg_show: draw xvg data into line figures.

:examples: 
    dit xvg_show -f test.xvg
    dit xvg_show -f test.xvg --subplot
    dit xvg_show -f test.xvg -o test.png -ns

:parameters:
    -f, --input
            specify the xvg file for input.
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
    -subplot, --subplot (optional)
            whether to draw different data in subplots.
""",
            "xvg_compare": """
xvg_compare: comparison of xvg files, draw different data columns you selected
             into line figure.

:examples:
    dit xvg_compare -f f1.xvg f2.xvg -c 1,2 2,3,4 -l l1 l2 l3 l4 l5
    dit xvg_compare -f f1.xvg f2.xvg -c 1 1 -l l1 l2 -x Time(ns) -y ylabel 
    dit xvg_compare -f f1.xvg f2.xvg -c 1,2 2 -l l1 l2 l3 -s 100 -e 500 -t test
    dit xvg_compare -f f1.xvg f2.xvg -c 1,2 2,3,4 -o test.png -ns

:parameters:
    -f, --input
            specify the xvg files for input. accept one or one more input file
            names seperated by space.
    -c, --column_select
            specify the index of columns you want to use. index starts from 0. 
            one xvg file in -f should be paired with one column index group 
            seperated by space, and in each column index group, indexs should 
            be seperated by comma. 
            In first example, 1,2 is paired with f1.xvg, 2,3,4 is paird with 
            f2.xvg. This means selecting the column 1 and 2 in f1.xvg, column 
            2, 3 and 4 in f2.xvg to compare. 
    -l, --legend_list (optional) 
            specify the legends to show in figure. The number of legends should
            be equal to the number of indexs you sepecified in -c. if you want 
            space in one legend, like "hh gg"; use "~~" for instead, 
            like "hh~~gg", ~~ will be turn into space and shown in figure.
    -s, --start (optional)
            specify row index of column data which you want to start to plot.
    -e, --end (optional)
            specify row index of column data which you want to stop plotting.
    -x, --xlabel (optional)
            specify the x-label you want to show in figure.
    -y, --ylabel (optional)
            specify the y-label you want to show in figure.
    -t, --title (optional)
            specify the title you want to show in figure.
    -smv, --showMV  (optional)
            if you specified this parameter, moving average and confidence 
            interval will be calculated and shown in figure. 
    -ws, --windowsize (optional)
            specify the windows size for moving average calculation. 
            default == 50, only valid when -smv specified. 
    -cf, --confidence (optional)
            specify the confidence for confidence interval calculation. 
            default == 0.90, only valid when -smv specified. 
    -a, --alpha (optional)
            specify the transparency for plotting confidence interval. 
            default == 0.4, only valid when -smv specified. 
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xvg
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
            I advise you'd better to use -tu in gmx commands for convertion of 
            unit of x-axis.
""",
            "xvg_ave": """
xvg_ave: calculate the average of each column in xvg file.

:examples:
    dit xvg_ave -f f1.xvg
    dit xvg_ave -f f1.xvg -s 1000 -e 2000

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -s, --start (optional)
            specify the row index of column data which you want to start to 
            calculation.
    -e, --end (optional)
            specify the row index of column data which you want to stop 
            calculation.
""",
            "xvg_mvave": """
xvg_mvave: calculate the moving average of each column in xvg file and save 
           results to csv file.

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
            specify the windows size for moving average calculation. 
            default == 50
    -cf, --confidence (optional)
            specify the confidence for confidence interval calculation. 
            default == 0.90
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
    dit xvg_rama -f rama.xvg -o test.png -ns

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
""",
            "xvg_show_distribution": """
xvg_show_distribution: calculate distribution of each data column in xvg file 
                       and show.

:examples:
    dit xvg_show_distribution -f f1.xvg
    dit xvg_show_distribution -f f1.xvg -bin 100
    dit xvg_show_distribution -f f1.xvg -o test.png -ns

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -bin, --bin (optional)
            specify the number of bins of calculating distribution. 
            default == 100
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
""",
            "xvg_show_stack": """
xvg_show_stack: draw stack figure of column data.

:examples:
    dit xvg_show_stack -f f1.xvg -c 2 3 4 5 6
    dit xvg_show_stack -f f1.xvg -c 2 3 4 5 6 -l A B C D E -s 500 -e 1000
    dit xvg_show_stack -f f1.xvg -c 2 3 4 5 6 -o test.png -ns

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -c, --column_select
            specify the column indexs you want to stack,  seperated by space.
    -l, --legend_list (optional)
            Normally, legends could be assigned automatically, but you can 
            specify them by -l. The number of legends should be equal to the 
            number of column indexs. if you want space in one legend, like 
            "hh gg", use "~~" for instead, like "hh~~gg". ~~ will be turn into 
            space and shown in figure.
    -s, --start (optional)
            specify the row index of column data which you want to start to 
            calculation.
    -e, --end (optional)
            specify the row index of column data which you want to stop 
            calculation.
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xvg
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
            I advise you'd better to use -tu in gmx commands for convertion of 
            unit of x-axis.
    -x, --xlabel (optional)
            specify the x-label you want to show in figure.
    -y, --ylabel (optional)
            specify the y-label you want to show in figure.
""",
            "xvg_show_scatter": """
xvg_show_scatter: draw scatter figure.

:examples:
    dit xvg_show_scatter -f f1.xvg -xi 0 -yi 1
    dit xvg_show_scatter -f f1.xvg -xi 1 -yi 2 -c 0
    dit xvg_show_scatter -f f1.xvg -xi 0 -yi 1 -o test.png -ns

:parameters:
    -f, --input
            specify the xvg file for input. 
            Only the first file is valid, others will be dropped.
    -xi, --x_index (optional)
            specify the index of column which you want to use as x data. 
            default == 0
    -yi, --y_index (optional)
            specify the index of column which you want to use as y data. 
            default == 1
    -c, --column_select (optional)
            specify the index of column which you want to use as color 
            mapping, select only one index
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
""",
            "xvg_energy_compute": """
xvg_energy_compute: calculate the interaction energy between two items.

:examples:
    dit xvg_energy_compute -f prolig.xvg pro.xvg lig.xvg -o energy_results.xvg

:parameters:
    -f, --input
            specify three xvg files to calculate (complex energy file, 
            component A energy file and component B energy file). Each should 
            contain and ONLY contain five columns 
            (Time, LJ(SR), Disper.corr., Coulomb(SR), Coul.recip.).
    -o, --output
            specify a xvg file to save results. 
""",
            "xvg_combine": """
xvg_combine: combine data columns selected and save results into one xvg file. 

:examples:
    dit xvg_combine -f f1.xvg -c 1,2 -o res.xvg
    dit xvg_combine -f f1.xvg f2.xvg -c 1,2 2,3 -o res.xvg

:parameters:
    -f, --input
            specify the xvg files for input. accept one or one more input file
            names seperated by space.
    -c, --column_select
            specify the index of columns you want to use. index starts from 0. 
            one xvg file in -f should be paired with one column index group 
            seperated by space. And in each column index group, indexs should
            be seperated by comma. 
            In second example, 1,2 is paired with f1.xvg, 2,3 is paird with 
            f2.xvg. This means selecting the column 1 and 2 in f1.xvg, column 2
            and 2 in f2.xvg to combine, and saving results to res.xvg. 
    -o, --output
            specify a xvg file to save results of combination.
""",
            "xvg_ave_bar": """
xvg_ave_bar: First, the average of each data column you select by -c will be
             calculated.
             Second, the average and standard error of corresponding column 
             averages in xvg file groups will be calculated.
             Third, the averages and standard errors will be drawn into bar 
             figure.

:examples:
    dit xvg_ave_bar -f f1_1.xvg,f1_2.xvg,f1_3.xvg f2_1.xvg,f2_2.xvg,f2_3.xvg -c 1 2 3
    dit xvg_ave_bar -f f1.xvg f2.xvg -c 1 2 -l L1 L2 -s 100 -e 1000 
    dit xvg_ave_bar -f f1.xvg f2.xvg -c 1 2 -x xlabel -y ylabel -t test
    dit xvg_ave_bar -f f1.xvg f2.xvg f3.xvg -c 1 2 -l L1 L2 L3 -xt xt1 xt2
    dit xvg_ave_bar -f f1.xvg f2.xvg -c 1 2 -l L1 L2 -ac average.csv
    dit xvg_ave_bar -f f1.xvg f2.xvg -c 1 2 -l L1 L2 -o test.png -ns

:parameters:
    -f, --input
            specify the xvg files for input. accept one or one more file names
            or file name groups. 
            Several file names seperated by comma is called a file name group. 
            In first example, f1_1.xvg,f1_2.xvg,f1_3.xvg is the first file name
            group, and f2_1.xvg,f2_2.xvg,f2_3.xvg is second file name group.
            This method will calculate averages of columns you select in each
            xvg file. Then calculate the average and standard error of column
            averages in each file group. Finally, convert the averages and 
            standard errors into bar plot.
    -c, --column_select
            specify the index of columns you want to calculate. Index starts 
            from 0. The column indexs you select will be applied to EVERY xvg
            file in -f.
    -l, --legend_list (optional) 
            specify the legends to show in figure. The number of legends should
            be equal to the number of files or file groups you specified in -f.
            If you want space in legend, like "hh gg"; use "~~" for instead, 
            like "hh~~gg", ~~ will be turn into space and shown in figure.
    -xt, --xtitles (optional)
            specity the names of x ticks in figure. The number of xtitles 
            should be equal to the number of indexs in column_select (-c).
    -s, --start (optional)
            specify the row index of column data which you want to start to 
            calculation.
    -e, --end (optional)
            specify the row index of column data which you want to stop 
            calculation.
    -x, --xlabel (optional)
            specify the x-label you want to show in figure.
    -y, --ylabel (optional)
            specify the y-label you want to show in figure.
    -t, --title (optional)
            specify the title you want to show in figure.
    -ac, --ave2csv (optional)
            the csv file name for saving data of averages into csv file.
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
""",
            "xvg_box": """
xvg_box: draw the data of columns you select into box figure.

:examples:
    dit xvg_box -f f1.xvg f2.xvg f3.xvg -c 1 2 -xt xt1 xt2 -s 100 -e 1000
    dit xvg_box -f f1.xvg f2.xvg -c 1 2 3 -xt xt1 xt2 xt3 -x xlabel -y ylabel
    dit xvg_box -f f1.xvg f2.xvg f3.xvg -c 1 2 -o test.png -ns -t title

:parameters:
    -f, --input
            accept one or more than one files as input.
    -c, --column_select
            specify the column indexs you want to plot. The indexs you 
            specified will be applied to each file you select in -f.
    -xt, --xtitles (optional)
            specity the names of x ticks in figure. The number of xtitles 
            should be equal to the number of indexs in column_select (-c).
    -s, --start (optional)
            specify the row index of column data which you want to start to 
            calculation.
    -e, --end (optional)
            specify the row index of column data which you want to stop 
            calculation.
    -x, --xlabel (optional)
            specify the x-label you want to show in figure.
    -y, --ylabel (optional)
            specify the y-label you want to show in figure.
    -t, --title (optional)
            specify the title you want to show in figure.
    -o, --output (optional)
            specify the output figure name. Figure will be saved in 300 dpi.
    -ns, --noshow (optional)
            if -ns is specified, figure won't be shown on screen. Usually work
            with -o to save figure directly.
""",
            "xpm_show": """
xpm_show: vasualize the xpm file.

:examples:
    dit xpm_show -f f1.xpm 
    dit xpm_show -f f1.xpm -ip 
    dit xpm_show -f f1.xpm -pcm 
    dit xpm_show -f f1.xpm -3d
    dit xpm_show -f f1.xpm -o test.png -ns 
    dit xpm_show -f 31.xpm -x xlabel -y ylabel -t title
    dit xpm_show -f 31.xpm -x xlabel -xs 0.001


:parameters:
    -f, --input
            specify the xpm file for input. 
    -o, --output (optional)
            specify the output figure name. 
    -ip, --interpolation (optional)
            whether to perform interpolation which will make your figure looks 
            smoother.
    -pcm, --pcolormesh (optional)
            whether to use pcolormesh function to vasualize your xpm figure.
    -3d, --threeDimensions (optional)
            whether to draw a 3D figure. Useful for free energy landscape plot.
    -ns, --noshow (optional)
            whether not to show figure in GUI, useful when working without GUI.
    -x, --xlabel (optional)
            specify the x-label you want to show in figure.
    -y, --ylabel (optional)
            specify the y-label you want to show in figure.
    -t, --title (optional)
            specify the title you want to show in figure.
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xpm
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
            I advise you'd better to use -tu in gmx commands for convertion of 
            unit of x-axis.
""",
            "xpm2csv": """
xpm2csv: convert xpm file into csv data file. 
         when number of x-axis (or y-axis) is 1 more than width (or height) of
         figure, the intermediate value of two adjacent values of x-axis (or
         y-axis) will be calculated to suit the width (or height).

:examples:
    dit xpm2csv -f f1.xpm -o test.csv
    dit xpm2csv -f f1.xpm -o test.csv -x xlabel -y ylabel
    dit xpm2csv -f f1.xpm -o test.csv -x xlabel -xs 0.001

:parameters:
    -f, --input
            specify the xpm file for input. 
    -o, --output
            specify the output csv file name.
    -x, --xlabel (optional)
            specify the x-label you want to write to csv file.
    -y, --ylabel (optional)
            specify the y-label you want to write to csv file.
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xpm
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
            I advise you'd better to use -tu in gmx commands for convertion of 
            unit of x-axis.
""",
            "xpm2dat": """
xpm2dat: convert xpm file into N*N data file. 
         when number of x-axis (or y-axis) is 1 more than width (or height) of
         figure, the intermediate value of two adjacent values of x-axis (or
         y-axis) will be calculated to suit the width (or height).

:examples:
    dit xpm2dat -f f1.xpm -o test.dat
    dit xpm2dat -f f1.xpm -o test.dat -x xlabel -y ylabel
    dit xpm2dat -f f1.xpm -o test.dat -x xlabel -xs 0.001

:parameters:
    -f, --input
            specify the xpm file for input. 
    -o, --output
            specify the output dat file name.
    -x, --xlabel (optional)
            specify the x-label you want to write to csv file.
    -y, --ylabel (optional)
            specify the y-label you want to write to csv file.
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xpm
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
            I advise you'd better to use -tu in gmx commands for convertion of 
            unit of x-axis.
""",
            "xpm2gpl": """
xpm2gpl: convert xpm file into gnuplot script.

:examples:
    dit xpm2gpl -f f1.xpm -o test.gpl
    dit xpm2gpl -f f1.xpm -o test.gpl -x xlabel -y ylabel -t title
    dit xpm2gpl -f f1.xpm -o test.gpl -x xlabel -xs 0.001

:parameters:
    -f, --input
            specify the xpm file for input. 
    -o, --output
            specify the output gnuplot script file name.
    -x, --xlabel (optional)
            specify the x-label you want to show in figure.
    -y, --ylabel (optional)
            specify the y-label you want to show in figure.
    -t, --title (optional)
            specify the title you want to show in figure.
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xpm
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
            I advise you'd better to use -tu in gmx commands for convertion of 
            unit of x-axis.
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
ndx_preserve: preserve index groups according to names you specified, and 
              remove others.

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
ndx_add: add one index group to ndx file by specified group name(-gn), 
         start(-s), end(-e), step(-t).

:examples:
    dit ndx_add -f f1.ndx -o res.ndx -gn test -s 1 -e 10 -t 2

:parameters:
    -f, --input (optional)
            specify ndx file for input. -f could be ignored if you want a new
            ndx file with the index group added.
    -o, --output
            specify the ndx file name for saving the results.
    -gn, --groupname
            specify the name of index group you want to add.
    -s, --start
            specify the start index of the group you want to add.
    -e, --end
            specify the end index of the group you want to add.
    -t, --step (optional)
            specify the step of indexs of the group you want to add. 
            default == 1. In the example, -s 1 -e 10 -t 2 means to generate a
            group contains index: 1 3 5 7 9 
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
mdp_gen: generate a template mdp file by application you specified. The mdp 
         file generated may NOT be appropriate for your system. 
         CHECK IT YOURSELF !

:examples:
    dit mdp_gen -o em.mdp -a em
    dit mdp_gen -o npt.mdp -a npt

:parameters:
    -o, --output
            specify an output mdp file to save the results.
    -a, --application
            specify the applications you want to use mdp file for. You can 
            select from: ions, em, nvt, npt, md, blank
""",
            "pipi_dist_ang": """
pipi_dist_ang: to calculate the distance and angles between two rings or between 
               one ring and one vector defined by atom group or command line.

:examples:
    dit pipi_dist_ang -f test.gro -n test.ndx 
    dit pipi_dist_ang -f test.gro -n test.ndx -select ring1 ring2
    dit pipi_dist_ang -f test.gro -n test.ndx -select ring1 -vg
    dit pipi_dist_ang -f test.gro -n test.ndx -select ring1 -vec 6 6 6 

:parameters:
    -f, --input
            the gro file which contains frames of molecule coordinates
    -n, --index
            the index file which contains atom index groups of rings or 
            vector groups
    -b (optional)
            the frame number to start calculation, default=0
    -dt (optional)
            the frame interval, default=1
    -o, --output
            the output filename to save results
    -vg (optional)
            whether to get vector from index group, default=False
    -vec (optional)
            specify the vector by command line, eg. -vec 6 6 6 
    -select (optional)
            select the groups from command line
""",
            "find_center": """
find_center: to find the atom which is nearest to center of atom group. 

:examples:
    dit find_center -f test.gro
    dit find_center -f test.gro -n index.ndx
    dit find_center -f test.gro -n index.ndx -aa

:parameters:
    -f, --input
            the gro file which contains one frame of molecule coordinates
    -n, --index (optional)
            the index file which you could select group from
    -aa, --AllAtoms (optional)
            if to find center of one group atoms in all atoms
""",
            "hbond": """
hbond: A useful method to process hbond related files generated by `gmx hbond`,
        you can get hbond occupancy figure and table infos from `dit hbond`. 
        note: the hbond names will show on figure only when number of hbonds 
              less than 10. 

:examples:
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm 
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -c 5 7 
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -c 5 7 0-3
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -o test.png -csv test.csv -ns
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -hnf d_resname(d_resnum)@d_atomname(d_atomnum)->h_atomname(h_atomnum)...a_resname(a_resnum)@a_atomname(a_atomnum) 
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -hnf "d_resname@d_atomname -> h_atomname ... a_resname@a_atomname" 
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -hnf "d_atomname@h_atomname -> a_atomname" 
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -hnf "number" 
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -hnf id -so AND0,2,5-7
    dit hbond -f md.gro -n hbond.ndx -m hbmap.xpm -hnf id -so OR0,2,5-7

:parameters:
    -f, --input
            the gro file which contains one frame of molecule coordinates, 
            used to get atom names.
    -n, --index
            the index file generated by `gmx hbond`
    -m, --map
            the hbond map file (hbmap.xpm) generated by `gmx hbond`
    -c, --select (optional)
            select the hbond id to only show the selected hbonds
    -o, --output (optional)
            the figure name you want to save
    -csv, --csv (optional)
            save the table infos into a csv whose name is specified here
    -ns, --noshow (optional)
            whether not to show figure, useful on computer without gui
    -hnf, --hbond_name_format (optional)
            define the hbond name format by user! 
            Each atom has four features: resname, resnum, atomname, atomnum. 
            Distinguish donor, hydrogen, acceptor by adding one prefix to each
            feature, like: d_resname, a_resnum, h_atomname. So you may able to
            define hbond name style by: 
            'd_resname(d_resnum)@d_atomname(d_atomnum)->h_atomname(h_atomnum)...a_resname(a_resnum)@a_atomname(a_atomnum)' 
            which is the default style, or also you could specify 
            'd_atomname@h_atomname...a_atomname' 
            or some format you would like.
            Or you could just set hnf to be 'number' or 'id' to show hbond id on figure
    -genscript, --genscript (optional)
            whether to generate scripts for calculating distance and angle of hbonds
    )
    -cda, --calc_distance_angle (optional)
            whether to calculate distance and angle of hbonds from distance xvg file and angle xvg file
    -distancefile, --distancefile (optional)
            distance file of hbonds for input
    -anglefile, --anglefile (optional)
            angle file of hbonds for input
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xvg
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
    -x, --xlabel (optional)
            specify the xlabel of figures
    -so, --set_operation (optional)
            use AND or OR to perform set operation on hbonds, eg. `AND1,2,5-6`  
            or `OR0,2-4,7`. The AND set or OR set of hbonds whose ids were after
            key words will be calculated and shown in occupancy figure.  
""",
            "mol_map": """
mol_map:  map the coordinates of coor_file to atoms in name_file. The molecules
          in two pdb file need to share exactly same conformation.
          **YOU ARE NOT SUPPOSED TO USE THIS COMMAND!**

:examples:
    dit mol_map -n good.gro -c coor.pdb -o output.pdb

:parameters:
    -n, --name
            the pdb file which contains infos with coordinates you don't want
    -c, --coor
            the pdb file with coordinates and the conformation of molecule is 
            the same with the molecule in -n
    -o, --output
            the pdb file to write output
""",
            "dccm_ascii": """
dccm_ascii: generate dynamic cross correlation matrix (DCCM) from dat file 
            generated by `gmx covar`.

:examples:
    dit dccm_ascii -f covapic.dat 
    dit dccm_ascii -f covapic.dat -m gaussian -o res.png -noshow
    dit dccm_ascii -f covapic.dat -x Res -y Res -t DCCM

:parameters:
    -f, --input 
            the dat file generated by `gmx covar` which stored the covarience
            matrix information
    -o, --output (optional)
            specify the output figure name
    -m, --mode (optional)
            specify the figure style, "origin", "gaussian", "bio3d"(default)
    -ns, --noshow (optional)
            whether not to show figure
    -x, --xlabel (optional)
            specify the xlabel of figure
    -y, --ylabel (optional)
            specify the ylabel of figure
    -t, --title (optional)
            specify the title of figure
""",
            "show_style": """
show_style: generate matplotlib style template. 

:examples:
    dit show_style
""",
            "dssp": """
dssp: read in one xpm of secondary structure file, output the DSSP plot, 
      residue occupancy vs time figure, time occupancy vs residue figure. 

:examples:
    dit dssp -f dssp.xpm 
    dit dssp -f dssp.xpm -xs 0.001 -x Time(ns)

:parameters:
    -f, --input 
            input xpm of secondary structure
    -x, --xlabel (optional)
            specify the xlabel of xpm
    -y, --ylabel (optional)
            specify the ylabel of xpm
    -t, --title (optional)
            specify the title of xpm
    -xs, --xshrink (optional)
            specify a factor for multiplication of x-axis. default == 1.0
            For instance, if "-xs 0.001" is specified, all x-axis value of xvg
            will multiply this value. x-axis 1000 will be shown as 1. 
            Useful for converting the unit (ps) of time into (ns). Don't forget
            to change xlabel too after specifing -xs.
""",
        }

    def print_help_infos(self, method: str) -> None:
        """print help messages"""

        if method in self.help_infos.keys():
            print(self.help_infos[method])
        else:
            logging.error(
                "unknown command {}, type `dit help` for more infos.".format(method)
            )
            sys.exit()


def print_help_msg(method: str) -> None:
    """print help messages"""

    help_class = HELP()
    help_class.print_help_infos(method)


def get_welcome_msg() -> str:
    """return welcome messages"""

    welcome_info = """
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

DuIvyTools provides about 30 commands for visualization and processing of GMX
result files like .xvg or .xpm. 

All commands are shown below:
    XVG:
        xvg_show, xvg_compare, xvg_ave, xvg_mvave, xvg2csv, xvg_rama
        xvg_show_distribution, xvg_show_stack, xvg_show_scatter
        xvg_energy_compute, xvg_combine, xvg_ave_bar, xvg_box
    XPM:
        xpm_show, xpm2csv, xpm2dat, xpm2gpl
    NDX:
        ndx_show, ndx_rm_dup, ndx_rm, ndx_preserve
        ndx_add, ndx_combine, ndx_rename
    MDP:
        mdp_gen
    Others:
        find_center, pipi_dist_ang, hbond, mol_map, dccm_ascii, dssp
    Matplotlib Style:
        show_style

You can type `dit help <command>` or `dit <command> -h` for more help messages 
about each command, like: `dit help xvg_show` or `dit xvg_show -h`. 

And you can also modify the style of figures by adding (only) one mplstyle file
to your working directory. DIT will apply it to custom figures. You could 
modify mplstyle file based on the template generated by "dit show_style", or 
select one from style folder of DuIvyTools github repo 
(https://github.com/CharlesHahn/DuIvyTools). 

Have a good day !
"""
    return welcome_info


def help_call_functions(arguments: list = None) -> None:
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]
    description = get_welcome_msg()

    if len(arguments) < 2:
        DIT_infos = get_welcome_msg()
        print(DIT_infos)
        sys.exit()
    elif len(arguments) == 2:
        if arguments[1] in ["help", "-h", "--help"]:
            print(description)
        else:
            logging.error(
                "unknown method {}, type `dit help` for more infos.".format(
                    arguments[1]
                )
            )
            sys.exit()
    else:
        if arguments[1] != "help":
            logging.error("unknown command {}".format(arguments[1]))
            sys.exit()
        else:
            methods = arguments[2:]
            for method in methods:
                print_help_msg(method)


def main():
    help_call_functions()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s -> %(message)s")
    logger = logging.getLogger(__name__)
    main()
