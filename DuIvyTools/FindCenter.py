"""
FindCenter module is part of DuIvyTools library, which is a tool for analysis and 
visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to provide some useful funcitons.

This module contains:
    - find_center function

This file is provided to you by GPLv2 license."""


import os
import sys
import argparse


def find_center(gro_file: str = "") -> None:
    """
    find_center: a function to figure out one atom coordinates which
    is the closest one to group center, useful for adjusting PBC
    This function will read one gro file and return the center of coordinates
    and the atom number which is close to it.

    :parameters:
        gro_file: the gro file which saved coordinates

    :return:
        None
    """

    if not os.path.exists(gro_file):
        print("Error -> no {} in current dirrectory. ".format(gro_file))
        exit()
    if gro_file[-4:] != ".gro":
        print("Error -> find_center only accept gro file with suffix .gro")
        exit()

    with open(gro_file, "r") as fo:
        lines = fo.readlines()
    atom_count = int(lines[1].strip())
    print("Info -> {:d} atoms in {}".format(atom_count, gro_file))
    atom_lines = lines[2 : atom_count + 2]

    ## calculate the center point
    center_x, center_y, center_z = 0, 0, 0
    for line in atom_lines:
        center_x += float(line[20:28])
        center_y += float(line[28:36])
        center_z += float(line[36:44])
    center_x = center_x / atom_count
    center_y = center_y / atom_count
    center_z = center_z / atom_count
    print(
        "Info -> the center point is ({:.3f}, {:.3f}, {:.3f})".format(
            center_x, center_y, center_z
        )
    )

    ## find the closed atom
    atom_info = ""
    dist = 5  # nm, find closed atom in sphere of 5nm
    for line in atom_lines:
        x = float(line[20:28])
        y = float(line[28:36])
        z = float(line[36:44])
        atom_center_dist = (
            (x - center_x) ** 2 + (y - center_y) ** 2 + (z - center_z) ** 2
        ) ** 0.5
        if atom_center_dist < dist:
            dist = atom_center_dist
            atom_info = line
    if atom_info == "":
        print("Error -> no atom detected in 5 nm sphere of center point. ")
        exit()
    else:
        print("--------------------------------------------")
        print("ResID Name Atom  Num       X       Y       Z")
        print("--------------------------------------------")
        print(atom_info, end="")
        print("--------------------------------------------")


def others_call_functions(arguments: list = []):
    """call functions according to arguments"""

    if len(arguments) == 0:
        arguments = [argv for argv in sys.argv]

    ## parse the command parameters
    parser = argparse.ArgumentParser(description="Find the center of a group of atoms")
    parser.add_argument("-f", "--input", help="file name for input")

    if len(arguments) < 2:
        print("Error -> no input parameters, -h or --help for help messages")
        exit()

    method = arguments[1]
    # print(method)
    if method in ["-h", "--help"]:
        parser.parse_args(arguments[1:])
        exit()

    if len(arguments) == 2:
        print("Error -> no parameters, type 'dit <command> -h' for more infos.")
        exit()
    args = parser.parse_args(arguments[2:])
    if method == "find_center":
        find_center(args.input)
    else:
        print("Error -> unknown method {}".format(method))
        exit()

    print("Info -> good day !")


def main():
    others_call_functions()


if __name__ == "__main__":
    main()
