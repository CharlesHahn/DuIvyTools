# DuIvyTools
[![PyPI version](https://badge.fury.io/py/DuIvyTools.svg)](https://badge.fury.io/py/DuIvyTools)
![PyPI - Downloads](https://img.shields.io/pypi/dm/DuIvyTools)
![PyPI - License](https://img.shields.io/pypi/l/DuIvyTools)
[![Documentation Status](https://readthedocs.org/projects/duivytools/badge/?version=latest)](https://duivytools.readthedocs.io/zh_CN/latest/?badge=latest)
      


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
    xpm_show, xpm2csv, xpm2gpl
For NDX files:
    ndx_show, ndx_rm_dup, ndx_rm, ndx_preserve
    ndx_add, ndx_combine, ndx_rename
For MDP files:
    mdp_gen
Others:
    find_center, pipi_dist_ang, hbond, mol_map, dccm_ascii
Matplotlib Style:
    show_style
```


## Cite 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7261532.svg)](https://doi.org/10.5281/zenodo.7261532)

## still working 

- [ ] readthedocs content
- [ ] dit command to get help
- [ ] xtick of xvg shrink
- [ ] xvg_show one plot mode
- [ ] xpm2dat(N by N)
- [ ] mdmat dm.xpm
- [ ] latex or format parser for matplotlib
- [ ] Discrete xpm to csv, convert notes to numbers
- [ ] python test
- [ ] better output (color, error ... )
- [ ] build a GUI maybe

