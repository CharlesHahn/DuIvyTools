""" NDX module is part of DuIvyTools library, which is a tool for analysis and visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to process and deal with ndx (GMX index) file. 

This NDX module contains:
    - NDX class

This file is provided to you by GPLv2 license."""


import os
import sys


class NDX(object):
    """
    NDX class is designed to read and process .ndx (GROMACS index) file

    :attributes:
    

    :method:

    """

    def __init__(self, ndxfile:str):
        """ read ndx file and extract data """

        self.ndx_filename = None
        self.group_dick = {}
        self.group_number = 0
        
    def remove_duplicate(self, outndx:str):
        pass

    def remove_group(self, outndx:str, group_list:list):
        pass

    def choose_group(self, outndx:str, group_list:list):
        pass

    def combine_group(self, outndx:str, group_list:list):
        pass

    def add_group(self, outndx:str, groupname:str, start:int, end:int, step:int):
        pass

    def change_groupname(self, outndx:str, old_name:str, new_name:str):
        pass



def ndx_remove_duplicate(ndxfile:str, outndx:str):
    pass

def ndx_remove_group(ndxfile:str, outndx:str, group_list:list):
    pass

def ndx_choose_group(ndxfile:str, outndx:str, group_list:list):
    pass

def ndx_combine_group(ndxfile:str, outndx:str, group_list:list):
    pass

def ndx_add_group(ndxfile:str, groupname:str, start:int, end:int, step:int, outndx:str):
    pass

def ndx_change_groupname(ndxfile:str, outndx:str, old_name:str, new_name:str):
        pass


def ndx_call_functions(arguments):
    pass

def main():
    arguments = [ argv for argv in sys.argv ]
    ndx_call_functions(arguments)

if __name__ == "__main__":
    main()


