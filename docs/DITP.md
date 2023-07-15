# DuIvyTools v0.5 

## 模块切分

整个程序由四块内容组成：

**FileParser**：处理各种类型的文件，包括xvg,xpm,ndx,mdp,pdb,gro等。

**Visualization**：数据可视化模块，对各种数据进行可视化；可视化引擎包括Matplotlib, plotext, gnuplot, plotly。

**Help&Docs**：帮助信息与帮助文档等信息。

**Procedures**：包含各种相关的程序流，用于流程的自动化或高通量的处理；此部分为实验功能。

**用户层**：最外层设置用户层，用户参数需要统一设置，最外层封装中设置参数层以方便调用。


## 模块内容

### FileParser

#### xvgParser

#### xpmParser

#### ndxParser

#### mdpParser

#### pdbParser

#### groParser


### Visualization

#### matplotlib

#### plotly

#### plotext

#### gnuplot



### Help&Docs

#### Help

#### DOcs


### 用户层

#### parameters

```
-f, --input
        specify the input file
-o, --output
        specify the output file
-ns, --noshow
        not show figure
-c, --column_select
        select column indexs for visualization
-l, --legend_list
        legends for visualization
-b, --begin
        specify the index beginning
-e, --end 
        specify the index ending
-dt, --dt
        the index step
-x, --xlabel
        x-label
-y, --ylabel
        y-label
-z, --zlabel
        z-label
-t, --title
        figure title
--xlim
        tuple for x value range
--ylim
        tuple for y value range
--zlim
        tuple for z value range
--x_precision
        precision of x value
--y_precision
        precision of y value
--z_precision
        precision of z value
-xs, --xshrink
        factor for multiplication of x-axis
-ys, --yshrink
        factor for multiplication of y-axis
-zs, --zshrink
        factor for multiplication of z-axis
-xi, --x_index
        the index for x of scatter figure
-yi, --y_index
        the index for y of scatter figure
-zi, --z_index
        the index for z of scatter figure
-xt, --xtitles
        the names of x ticks in figure
-smv, --showMV
        show moving average
-ws, --windowsize
        windows size for moving average
-cf, --confidence
        confidence for moving average
--alpha
        alpha for figure transparency of moving average
--bin
        number of bins for calculating distribution
--ave2csv
        save the average data info csv
-ip, --interpolation
        interpolation
-pcm, --pcolormesh ???
        或许默认就是pcolormesh，这样就不用其它的了
-3d
        3D figure
-gl, --grouplist
        the group names
-int, --interactive
        interactive mode
-gn, --groupname
        group name for modification of group names
-on, --oldname ???
        old name of ndx
-nn, --newname ???
        new name of ndx
-a, --application
        for mdp generation
-n, --index
        index file
-vg
        get vector from index group
-vec
        get vector by command line
-select
        select the groups from command line ???
-aa, --allatoms
        find center of one group atoms in all atoms
-m, --map
        the hbond map file
-csv
        save data into csv
-hnf, --hbond_name_format
        hbond name format
-genscript
        gen script for distance and angle of hbonds calculation
-cda, --calc_distance_angle
        calculate distance and angle of hbonds from xvg files
--distancefile
        distance xvg of hbonds
--anglefile
        angle xvg files
-so, --set_operation
        AND or OR operation on hbonds
-cm, --colormap
        select colormap
```

#### commands

- xvg_show
- xvg_compare
- xvg_ave
- xvg_mvave
- xvg2csv
- xvg_rama
- xvg_show_distribution
- xvg_show_stack
- xvg_show_scatter
- xvg_energy_compute
- xvg_combine
- xvg_ave_bar
- xvg_box
- xvg_violin

- xpm_show
- xpm2csv
- xpm2dat
- xpm2gpl

- ndx_show
- ndx_rm_dup
- ndx_rm
- ndx_preserve
- ndx_add
- ndx_combine
- ndx_rename

- mdp_gen

- show_style

- find_center
- pipi_dist_ang
- hbond
- dccm_ascii
- dssp




### Procedures

#### dock


#### GROMACS Analysis


