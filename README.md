DuIvyTools

[![PyPI version](https://badge.fury.io/py/DuIvyTools.svg)](https://badge.fury.io/py/DuIvyTools)
![PyPI - Downloads](https://img.shields.io/pypi/dm/DuIvyTools)
![PyPI - License](https://img.shields.io/pypi/l/DuIvyTools)
[![Documentation Status](https://readthedocs.org/projects/duivytools/badge/?version=latest)](https://duivytools.readthedocs.io/zh_CN/latest/?badge=latest)
[![commits-since](https://img.shields.io/github/commits-since/CharlesHahn/DuIvyTools/v0.4.8.svg)](https://github.com/CharlesHahn/DuIvyTools/compare/v0.4.8...master)
[![Python Version](https://img.shields.io/pypi/pyversions/DuIvyTools.svg)](https://pypi.org/project/DuIvyTools)
[![Documentation Status](https://readthedocs.org/projects/duivytools/badge/?version=latest)](https://duivytools.readthedocs.io/en/latest/?badge=latest)

```
  *******           **                  **********               **
 /**////**         /**          **   **/////**///               /**
 /**    /** **   **/** **    **//** **     /**  ******   ****** /**  ******
 /**    /**/**  /**/**/**   /** //***      /** **////** **////**/** **//// 
 /**    /**/**  /**/**//** /**   /**       /**/**   /**/**   /**/**//***** 
 /**    ** /**  /**/** //****    **        /**/**   /**/**   /**/** /////**
 /*******  //******/**  //**    **         /**//****** //****** *** ****** 
 ///////    ////// //    //    //          //  //////   ////// /// //////
```

DuIvyTools (DIT) is a simple analysis and visualization tool for GROMACS result
files (.xvg, .xpm, .ndx, .mdp). 

This tool can perform data visualization and convertion, and may be able to 
cover daily simple tasks when analyzing results of molecular dynamics 
simulations by GROMACS. 

## Intro

The usage of DIT is similar to GMX, type `dit` and followed by commands and 
parameters, like:

```bash
dit xvg_show -f test.xvg
dit xpm_show -f test.xpm -ip
```

Type `dit help` for more messages.

visit https://github.com/CharlesHahn/DuIvy/tree/master/Articles/20220310-DIT 
for more introductions in Chinese.


## Install

This tool is a python3 library which you can install it by `pip`.

```bash
pip install DuIvyTools
```

## Commands

This tool contains quite a lot commands.

```
For XVG files:
    xvg_show, xvg_compare, xvg_ave, xvg_mvave, xvg2csv, xvg_rama
    xvg_show_distribution, xvg_show_stack, xvg_show_scatter
    xvg_energy_compute, xvg_combine, xvg_ave_bar, xvg_box
For XPM files:
    xpm_show, xpm2csv, xpm2dat, xpm2gpl
For NDX files:
    ndx_show, ndx_rm_dup, ndx_rm, ndx_preserve
    ndx_add, ndx_combine, ndx_rename
For MDP files:
    mdp_gen
Others:
    find_center, pipi_dist_ang, hbond, mol_map, dccm_ascii, dssp
Matplotlib Style:
    show_style

You can type `dit help <command>` or `dit <command> -h` for more help messages 
about each command, like: `dit help xvg_show` or `dit xvg_show -h`. 
```


## Cite 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6339993.svg)](https://doi.org/10.5281/zenodo.6339993)


# To fix

- [ ] hbond -g hbond.log : hbond atom names in it
- [ ] xpm x and y precision(after dot)

## further features in v0.5.0

- [ ] ! the parsing of files should be isolated from figure plotting
- [ ] ! re-design all arguments parsing part
- [ ] ! plotting engines: matplotlib, plotext, gnuplot
- [ ] ! Procedures
- [ ] ! tidy help info and documentation
- [ ] mdmat dmf.xpm
- [ ] Discrete xpm to csv, convert notes to numbers
- [ ] Control over the number of digits after the decimal point
- [ ] better output (color, error ... ),绘图质量参考desmond
- [ ] use plotext to create plot in terminal !
- [ ] python test
- [ ] latex or format parser for matplotlib
- [ ] volume occupancy of ligand during MD
- [ ] build a GUI maybe (webapp?)
