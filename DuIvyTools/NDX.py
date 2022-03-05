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
        ndx_filename: th name of input ndx file name
        group_number: the total number of groups
        group_name_list: a list to store all groups' names
        group_index_list: a list to store all groups' index numbers

    :method:
        remove_duplicate: remove the duplicate groups
        remove_group: remove some specified groups
        preserve_group: preserve some specified groups
        combine_group: combine some groups into one group
        add_group: add one group by specified groupname and index parameters
        rename_group: rename the group
    """

    def __init__(self, ndxfile:str) -> None:
        """ read ndx file and extract data """

        self.ndx_filename = ndxfile
        self.group_number = 0
        self.group_name_list = []
        self.group_index_list = []

        ## check file 
        if len(ndxfile) <= 4 or ndxfile[-4:] != ".ndx":
            print("Error -> please specify a index file with suffix .ndx")
            exit()
        if not os.path.exists(ndxfile):
            print("Error -> no {} in current directory".format(ndxfile))
            exit()

        ## parse the content of ndxfile
        with open(ndxfile, 'r') as fo:
            lines = [ line.strip() for line in fo.readlines() ]
        for line_id, line in enumerate(lines):
            if line == "":
                continue
            elif line[0] == "[" and line[-1] == "]":
                self.group_name_list.append(line[1:-1].strip())
                self.group_number += 1
            elif (not "[" in line) and (not "]" in line):
                if len(self.group_name_list) -1 == len(self.group_index_list):
                    self.group_index_list.append([int(i) for i in line.split()])
                elif len(self.group_name_list) == len(self.group_index_list):
                    self.group_index_list[-1] += [int(i) for i in line.split()]
                else:
                    print("Error -> check your index file, one group", end="")
                    print("name should be followed by some index number")
                    exit()
            else:
                print("Error -> a weired line appears at line {}".format(line_id))
                exit()
        if not (self.group_number == len(self.group_name_list) == len(
                self.group_index_list)):
            print("Error -> length of group name and group index are not equal")
            exit()

        print("Info -> read {} groups from {} successfully".format(
            self.group_number, self.ndx_filename))
        

    def write_ndx(self, outndx:str) -> None:
        """ write data to new ndx file """

        ## check file 
        if len(outndx) <=4 or outndx[-4:] != ".ndx":
            print("Error -> please specify a output file with suffix .ndx")
            exit()
        if os.path.exists(outndx):
            print("Error -> {} is already in current directory".format(outndx))
            exit()

        ## write results
        if len(self.group_name_list) != len(self.group_index_list):
            print("Error -> shit happens sometimes, oops")
            exit()
        with open(outndx, 'w') as fo:
            for i in range(len(self.group_name_list)):
                fo.write("[ {} ]\n".format(self.group_name_list[i]))
                sentence, count = "", 0
                for index in self.group_index_list[i]:
                    count += 1
                    sentence += "{:>4d} ".format(index)
                    if count == 15:
                        sentence += "\n"
                        count = 0
                fo.write(sentence.strip() + "\n")
        print("Info -> save index data to {} successfully".format(outndx))


    def remove_duplicate(self, outndx:str) -> None:
        """ remove the duplicate groups in ndx file """

        ## remove duplicate
        out_name_list, out_index_list = [], []
        for index_id, index in enumerate(self.group_index_list):
            if index not in out_index_list or (
                self.group_name_list[index_id] not in out_name_list):
                out_index_list.append(index)
                if self.group_name_list[index_id] in out_name_list:
                    print("Warning -> two groups with the same name", end="")
                    print(" ({}) but index numbers are different? check it".format(
                        self.group_name_list[index_id]))
                out_name_list.append(self.group_name_list[index_id])
            else:
                print("Info -> removed the group {}".format(
                    self.group_name_list[index_id]))

        self.group_name_list = out_name_list
        self.group_index_list = out_index_list
        self.write_ndx(outndx)


    def remove_group(self, outndx:str, group_list:list) -> None:
        pass


    def preserve_group(self, outndx:str, group_list:list) -> None:
        pass


    def combine_group(self, outndx:str, groupname:str, group_list:list) -> None:
        pass


    def add_group(self, outndx:str, groupname:str, start:int, end:int, step:int) -> None:
        pass


    def rename_group(self, outndx:str, old_name:str, new_name:str) -> None:
        pass



def ndx_remove_duplicate(ndxfile:str, outndx:str) -> None:
    pass

def ndx_remove_group(ndxfile:str, outndx:str, group_list:list) -> None:
    pass

def ndx_preserve_group(ndxfile:str, outndx:str, group_list:list) -> None:
    pass

def ndx_combine_group(ndxfile:str, outndx:str, groupname:str, group_list:list) -> None:
    pass

def ndx_add_group(ndxfile:str, outndx:str, groupname:str, start:int, end:int, step:int) -> None:
    pass

def ndx_rename_group(ndxfile:str, outndx:str, old_name:str, new_name:str) -> None:
        pass





def ndx_call_functions(arguments):
    pass





def main():
    # arguments = [ argv for argv in sys.argv ]
    # ndx_call_functions(arguments)
    ndx = NDX(sys.argv[1])
    ndx.remove_duplicate("test.ndx")





if __name__ == "__main__":
    main()
