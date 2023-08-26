# DuIvyTools v0.5 

## 模块切分

整个程序由四块内容组成：

**FileParser**：处理各种类型的文件，包括xvg,xpm,ndx,mdp,pdb,gro等。

**Visualization**：数据可视化模块，对各种数据进行可视化；可视化引擎包括Matplotlib, plotext, gnuplot, plotly。

**Help&Docs**：帮助信息与帮助文档等信息。

**Procedures**：包含各种相关的程序流，用于流程的自动化或高通量的处理；此部分为实验功能。

**用户层**：最外层设置用户层，用户参数需要统一设置，最外层封装中设置参数层以方便调用。还需要设置log系统用于输出log。


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
DuIvyTools: A Simple MD Analysis Tool

positional arguments:
  cmd                   command of DIT to run

optional arguments:
  -h, --help            
        show this help message and exit
  -f INPUT [INPUT ...], --input INPUT [INPUT ...]
        specify the input file or files
  -o OUTPUT, --output OUTPUT
        specify the output file
  -ns, --noshow         
        not to show figure
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
        select the column indexs for visualization or calculation, or input numerical list
  -l LEGENDS [LEGENDS ...], --legends LEGENDS [LEGENDS ...]
        specify the legends of figure or data
  -b BEGIN, --begin BEGIN
        specify the index for beginning (include)
  -e END, --end END     
        specify the index for ending (not include)
  -dt DT, --dt DT       
        specify the index step, default to 1
  -x XLABEL, --xlabel XLABEL
        specify the xlabel of figure or data
  -y YLABEL, --ylabel YLABEL
        specify the ylabel of figure or data
  -z ZLABEL, --zlabel ZLABEL
        specify the zlabel of figure or data
  -t TITLE, --title TITLE
        specify the title of figure or data
  -xmin XMIN, --xmin XMIN
        specify the X value limitation, x_min
  -xmax XMAX, --xmax XMAX
        specify the X value limitation, x_max
  -ymin YMIN, --ymin YMIN
        specify the Y value limitation, y_min
  -ymax YMAX, --ymax YMAX
        specify the Y value limitation, y_max
  -zmin ZMIN, --zmin ZMIN
        specify the Z value limitation, z_min
  -zmax ZMAX, --zmax ZMAX
        specify the Z value limitation, z_max
  --x_precision X_PRECISION
        specify the precision of X values for visualization
  --y_precision Y_PRECISION
        specify the precision of Y values for visualization
  --z_precision Z_PRECISION
        specify the precision of Z values for visualization
  -xs XSHRINK, --xshrink XSHRINK
        modify X values by multipling xshrink, default to 1.0
  -ys YSHRINK, --yshrink YSHRINK
        modify Y values by multipling yshrink, default to 1.0
  -zs ZSHRINK, --zshrink ZSHRINK
        modify Z values by multipling zshrink, default to 1.0
  -smv, --showMV        
        whether to show moving averages of data
  -ws WINDOWSIZE, --windowsize WINDOWSIZE
        window size for moving average calculation, default to 50
  -cf CONFIDENCE, --confidence CONFIDENCE
        confidence for confidence interval calculation, default to 0.95
  --alpha ALPHA         
        the alpha of figure items
  -csv CSV, --csv CSV   
        store data into csv file
  -eg {matplotlib,plotext,plotly,gnuplot}, --engine {matplotlib,plotext,plotly,gnuplot}
        specify the engine for plotting: 'matplotlib', 'plotext', 'plotly', 'gnuplot'
  -cmap COLORMAP, --colormap COLORMAP
        specify the colormap applied for figures, available for 'matplotlib' and 'plotly' engine
  --colorbar_location {None,left,top,bottom,right}
        the location of colorbar, also determining the orientation of colorbar, ['left', 'top', 'bottom', 'right'], available for 'matplotlib'
  --legend_location {inside,outside}
        the location of legend box, ['inside', 'outside'], available for 'matplotlib' and 'gnuplot'
  -m {None,withoutScatter,pcolormesh,3d,contour,AllAtoms}, --mode {None,withoutScatter,pcolormesh,3d,contour,AllAtoms}
        additional parameter: 'withoutScatter' will NOT show scatter plot for 'xvg_box_compare'; 'imshow', 'pcolormesh', '3d', 'contour' were used for 'xpm_show' command; 'AllAtoms' were used for 'find_center' command
  -al ADDITIONAL_LIST [ADDITIONAL_LIST ...], --additional_list ADDITIONAL_LIST [ADDITIONAL_LIST ...]
        additional parameters. Used to set xtitles for 'xvg_ave_bar'
  -ip INTERPOLATION, --interpolation INTERPOLATION
        specify the interpolation method, default to None
  -ipf INTERPOLATION_FOLD, --interpolation_fold INTERPOLATION_FOLD
        specify the interpolation fold, default to 10
  -bin BIN, --bin BIN   
        the bin number for distribution calculation
```


#### commands

- xvg_show
- xvg_compare
- xvg_ave
- xvg_show_distribution
- xvg_show_stack
- xvg_show_scatter
- xvg_energy_compute
- xvg_box_compare
- xvg_combine
- xvg_ave_bar
- xvg_rama

- xpm_show
- xpm2csv
- xpm2dat
- xpm_diff
- xpm_merge

- mdp_gen
- show_style
- find_center
- dccm_ascii
- dssp
- ndx_add   ## add a new group
- ndx_split ## ndx group split into several group


** style setting **

gnuplot style : User could define by themselves, set the DIT style


**DOC**

**TODO**

-[ ] angle vs time, circle plot
-[ ] reconstruction of gnuplot engine
-[ ] seaborn engine 


### Procedures

** move to procedure **

- pipi_dist_ang
- hbond

#### dock


#### GROMACS Analysis


