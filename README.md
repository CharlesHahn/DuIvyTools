# DuIvyTools

DuIvyTools (DIT): A simple tool for analysis of GROMACS result files(.xvg, .xpm, .ndx, .mdp). 

This tool can perform data visualization and convertion, and is able to cover daily tasks when analyzing results of molecular dynamics simulations by GROMACS. 

## Intro

The usage of DIT is similar to GMX, type `dit` and followed by commands and parameters, like:

```bash
dit xvg_show -f test.xvg
```

## Install

This tool is a python library which you can install it by `pip`.

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
    - still working on these

For .mdp file:
    - still working on these

## Cite 

pass
