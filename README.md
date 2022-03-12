# DuIvyTools
[![PyPI version](https://badge.fury.io/py/DuIvyTools.svg)](https://badge.fury.io/py/DuIvyTools)
![PyPI - Downloads](https://img.shields.io/pypi/dm/DuIvyTools)
![PyPI - License](https://img.shields.io/pypi/l/DuIvyTools)

DuIvyTools (DIT): A simple tool for analysis of GROMACS result files(.xvg, .xpm, .ndx, .mdp). 

This tool can perform data visualization and convertion, and may be able to cover daily tasks when analyzing results of molecular dynamics simulations by GROMACS. 

## Intro

The usage of DIT is similar to GMX, type `dit` and followed by commands and parameters, like:

```bash
dit xvg_show -f test.xvg
```

Type `dit help` for more messages.

visit https://github.com/CharlesHahn/DuIvy/tree/master/Articles/20220310-DIT for more introductions.


## Install

This tool is a python3 library which you can install it by `pip`.

```bash
pip install DuIvyTools
```

## Commands

This tool contains quite a lot commands.

For .xvg file:
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

For .xpm file:
- xpm_show
- xpm2csv
- xpm2gpl
- xpm_combine (not recommand to use it)

For .ndx file:
- ndx_show
- ndx_rm_dup
- ndx_rm
- ndx_preserve
- ndx_add
- ndx_combine
- ndx_rename

For .mdp file:
- mdp_gen

For help messages:
- help


## Cite 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6340263.svg)](https://doi.org/10.5281/zenodo.6340263)


## still working 

- [x] support space in the legends
- [x] column_select in xvg_show_stack
- [ ] xlabel and ylabel in xpm_show
- [ ] plot control parameters
- [ ] one item in column_select in xvg_ave_bar
- [ ] make the calculation of moving averages faster
- [ ] the location of ticks in xpm figure procesion
- [ ] support of modification of x-values in XPM and XVG
- [ ] savefig() and noshow in XVG
- [ ] add function of prolig trjconv and center calculation
- [ ] build a GUI maybe

