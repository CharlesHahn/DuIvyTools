"""
NDX module is part of DuIvyTools library, which is a tool for analysis and 
visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to process and deal with ndx (GMX index) file. 

This NDX module contains:
    - NDX class

This file is provided to you by GPLv2 license."""


import os
import sys
import argparse


class NDX(object):
    """
    NDX class is designed to read and process .ndx (GROMACS index) file

    :attributes:
        ndx_filename: th name of input ndx file name
        group_number: the total number of groups
        group_name_list: a list to store all groups' names
        group_index_list: a list to store all groups' index numbers

    :method:
        show_ndx: print all group names
        writ_ndx: write ndx data to ndx file
        remove_duplicate: remove the duplicate groups
        remove_group: remove some specified groups
        preserve_group: preserve some specified groups
        combine_group: combine some groups into one group
        add_group: add one group by specified groupname and index parameters
        rename_group: rename the group
    """

    def __init__(self, ndxfile: str) -> None:
        """read ndx file and extract data"""

        self.ndx_filename = ndxfile
        self.group_number = 0
        self.group_name_list = []
        self.group_index_list = []

        ## to init without input ndx file
        if ndxfile == None:
            self.ndx_filename = ""
            return

        ## check file
        if len(ndxfile) <= 4 or ndxfile[-4:] != ".ndx":
            print("Error -> please specify a index file with suffix .ndx")
            exit()
        if not os.path.exists(ndxfile):
            print("Error -> no {} in current directory".format(ndxfile))
            exit()

        ## parse the content of ndxfile
        with open(ndxfile, "r") as fo:
            lines = [line.strip() for line in fo.readlines()]
        for line_id, line in enumerate(lines):
            if line == "":
                continue
            elif line[0] == "[" and line[-1] == "]":
                self.group_name_list.append(line[1:-1].strip())
                self.group_number += 1
            elif (not "[" in line) and (not "]" in line):
                if len(self.group_name_list) - 1 == len(self.group_index_list):
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
        if not (
            self.group_number == len(self.group_name_list) == len(self.group_index_list)
        ):
            print("Error -> length of group name and group index are not equal")
            exit()

        print(
            "Info -> read {} groups from {} successfully".format(
                self.group_number, self.ndx_filename
            )
        )

    def show_ndx(self) -> None:
        """print all group names"""
        for name_id, name in enumerate(self.group_name_list):
            print("  {:>2} -> {}".format(name_id, name))

    def write_ndx(self, outndx: str) -> None:
        """write data to new ndx file"""

        ## check file
        if outndx == None:
            print("Error -> please specify the output ndx file name")
            exit()
        if len(outndx) <= 4 or outndx[-4:] != ".ndx":
            print("Error -> please specify a output file with suffix .ndx")
            exit()
        if os.path.exists(outndx):
            print("Error -> {} is already in current directory".format(outndx))
            exit()

        ## write results
        if len(self.group_name_list) != len(self.group_index_list):
            print("Error -> shit happens sometimes, oops")
            exit()
        with open(outndx, "w") as fo:
            for i in range(len(self.group_name_list)):
                fo.write("[ {} ]\n".format(self.group_name_list[i]))
                sentence, count = "", 0
                for index in self.group_index_list[i]:
                    count += 1
                    sentence += "{:>4d} ".format(index)
                    if count == 15:
                        sentence += "\n"
                        count = 0
                fo.write(sentence.strip("\n") + "\n")
        print("Info -> save index data to {} successfully".format(outndx))

    def remove_duplicate(self, outndx: str) -> None:
        """remove the duplicate groups in ndx file"""

        ## remove duplicate
        out_name_list, out_index_list = [], []
        for index_id, index in enumerate(self.group_index_list):
            if index not in out_index_list or (
                self.group_name_list[index_id] not in out_name_list
            ):
                out_index_list.append(index)
                if self.group_name_list[index_id] in out_name_list:
                    print("Warning -> two groups with the same name", end="")
                    print(
                        " ({}) but index numbers are different? check it".format(
                            self.group_name_list[index_id]
                        )
                    )
                out_name_list.append(self.group_name_list[index_id])
            else:
                print(
                    "Info -> removed the group {}".format(
                        self.group_name_list[index_id]
                    )
                )

        self.group_name_list = out_name_list
        self.group_index_list = out_index_list
        self.write_ndx(outndx)

    def remove_group(
        self, outndx: str, group_list: list, interactive: bool = False
    ) -> None:
        """remove the groups you specify"""

        ## check parameters
        if interactive == False and group_list == []:
            print("Error -> please specify the names of groups you wanna remove")
            exit()
        ## remove the groups specified in group_list
        out_name_list, out_index_list = [], []
        if interactive == False:
            for index_id, name in enumerate(self.group_name_list):
                if name not in group_list:
                    out_name_list.append(name)
                    out_index_list.append(self.group_index_list[index_id])
                else:
                    print("Info -> removed the group {}".format(name))
        else:
            for index_id, name in enumerate(self.group_name_list):
                resp = input("\n  -> remove group [ {} ] ? y/N : ".format(name)).strip()
                if resp.lower() == "n" or resp == "" or resp.lower() == "no":
                    out_name_list.append(name)
                    out_index_list.append(self.group_index_list[index_id])
                elif resp.lower() == "y" or resp.lower() == "yes":
                    print("Info -> removed the group {}".format(name))
                else:
                    print("Error -> unknown response {}".format(resp))
                    exit()

        self.group_name_list = out_name_list
        self.group_index_list = out_index_list
        self.write_ndx(outndx)

    def preserve_group(
        self, outndx: str, group_list: list, interactive: bool = False
    ) -> None:
        """preserve the groups you specify and remove all others"""

        ## check parameters
        if interactive == False and group_list == []:
            print("Error -> please specify the names of groups you wanna preserve")
            exit()
        ## remove the groups specified in group_list
        out_name_list, out_index_list = [], []
        if interactive == False:
            for index_id, name in enumerate(self.group_name_list):
                if name in group_list:
                    out_name_list.append(name)
                    out_index_list.append(self.group_index_list[index_id])
                else:
                    print("Info -> removed the group {}".format(name))
        else:
            for index_id, name in enumerate(self.group_name_list):
                resp = input(
                    "\n  -> preserve group [ {} ] ? y/N : ".format(name)
                ).strip()
                if resp.lower() == "n" or resp == "" or resp.lower() == "no":
                    print("Info -> removed the group {}".format(name))
                elif resp.lower() == "y" or resp.lower() == "yes":
                    out_name_list.append(name)
                    out_index_list.append(self.group_index_list[index_id])
                else:
                    print("Error -> unknown response {}".format(resp))
                    exit()

        self.group_name_list = out_name_list
        self.group_index_list = out_index_list
        self.write_ndx(outndx)

    def combine_group(self, outndx: str, groupname: str, group_list: list) -> None:
        """combine the groups specified into one group"""

        if groupname == None:
            print("Error -> please specify the group name")
            exit()
        ## combine the groups specified in group_list into one group
        out_name_list, out_index_list = [], []
        for index_id, name in enumerate(self.group_name_list):
            if name in group_list:
                if len(out_name_list) == 0:
                    out_name_list.append(name)
                    out_index_list.append(self.group_index_list[index_id])
                elif len(out_name_list) == 1:
                    out_name_list[0] += "_" + name
                    out_index_list[0] += self.group_index_list[index_id]
                else:
                    print("Error -> shit happens when combination")
                    exit()
        self.group_name_list += [groupname]
        self.group_index_list += out_index_list
        print("Info -> combined {} into {}".format(out_name_list[0], groupname))
        self.write_ndx(outndx)

    def add_group(
        self, outndx: str, groupname: str, start: int, end: int, step: int
    ) -> None:
        """add one index group by parameters specified"""

        ## add one group
        if groupname == None:
            print("Error -> please specify the group name")
            exit()
        if step == None:
            step = 1
        if start == None or end == None:
            print("Error -> start and end must be integer > 0")
            exit()
        if start <= 0 or end <= start:
            print("Error -> start should > 0 and end should > start")
            exit()
        if groupname in self.group_name_list:
            print(
                "Warning -> already a group {} in {}, add to the end".format(
                    groupname, self.ndx_filename
                )
            )
        out_index = [i for i in range(start, end, step)]
        self.group_name_list.append(groupname)
        self.group_index_list.append(out_index)
        print("Info -> add group {} successfully".format(groupname))
        self.write_ndx(outndx)

    def rename_group(
        self, outndx: str, old_name: str, new_name: str, interactive: bool = False
    ) -> None:
        """rename the group name"""

        ## check parameters
        if interactive == False:
            if old_name == None or old_name == "":
                print("Error -> please specify the old name you wanna change")
                exit()
            if new_name == None or new_name == "":
                print("Error -> please specify the new name you wanna apply")
                exit()

        out_name_list = []
        if interactive == False:
            for name in self.group_name_list:
                if name == old_name:
                    out_name_list.append(new_name)
                    print("Info -> changed {} to {}".format(name, new_name))
                else:
                    out_name_list.append(name)
        else:
            print("Info -> change group names in interactive mode, type enter to pass")
            for name in self.group_name_list:
                name_input = input(" -> change {} to : ".format(name)).strip()
                if name_input == "":
                    out_name_list.append(name)
                else:
                    out_name_list.append(name_input)
                    print("Info -> changed {} to {}".format(name, name_input))
        self.group_name_list = out_name_list
        self.write_ndx(outndx)


def ndx_show_name(ndxfile: str) -> None:
    """print the name of all groups"""
    ndx = NDX(ndxfile)
    ndx.show_ndx()


def ndx_remove_duplicate(ndxfile: str, outndx: str) -> None:
    """remove all duplicate groups"""
    ndx = NDX(ndxfile)
    ndx.remove_duplicate(outndx)


def ndx_remove_group(
    ndxfile: str, outndx: str, group_list: list, interactive: bool = False
) -> None:
    """remove the groups specified"""
    ndx = NDX(ndxfile)
    ndx.remove_group(outndx, group_list, interactive)


def ndx_preserve_group(
    ndxfile: str, outndx: str, group_list: list, interactive: bool = False
) -> None:
    """preserve the groups specified and remove all others"""
    ndx = NDX(ndxfile)
    ndx.preserve_group(outndx, group_list, interactive)


def ndx_combine_group(
    ndxfile: str, outndx: str, groupname: str, group_list: list
) -> None:
    """combine the groups specified"""
    ndx = NDX(ndxfile)
    ndx.combine_group(outndx, groupname, group_list)


def ndx_add_group(
    ndxfile: str, outndx: str, groupname: str, start: int, end: int, step: int
) -> None:
    """add one group by specified parameters"""
    ndx = NDX(ndxfile)
    ndx.add_group(outndx, groupname, start, end, step)


def ndx_rename_group(
    ndxfile: str, outndx: str, old_name: str, new_name: str, interactive: bool = False
) -> None:
    """rename groups"""
    ndx = NDX(ndxfile)
    ndx.rename_group(outndx, old_name, new_name, interactive)


def ndx_call_functions(arguments: list = None) -> None:
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]

    ## parse the command parameters
    parser = argparse.ArgumentParser(description="Process ndx files generated by GMX")
    parser.add_argument("-f", "--input", help="input your ndx file")
    parser.add_argument("-o", "--output", help="file name to output")
    parser.add_argument(
        "-int",
        "--interactive",
        action="store_true",
        help="whether to initiate interactive mode",
    )
    parser.add_argument(
        "-gl", "--grouplist", nargs="+", help="specify a list of group names"
    )
    parser.add_argument("-gn", "--groupname", type=str, help="specify the group name")
    parser.add_argument("-on", "--oldname", type=str, help="specify the old group name")
    parser.add_argument("-nn", "--newname", type=str, help="specify the new group name")
    parser.add_argument(
        "-s", "--start", type=int, help="specify the start index number"
    )
    parser.add_argument("-e", "--end", type=int, help="specify the end index number")
    parser.add_argument(
        "-t", "--step", type=int, help="specify the step for generate index numbers"
    )

    if len(arguments) < 2:
        print("Error -> no input parameters, -h or --help for help messages")
        exit()
    method = arguments[1]
    # print(method)
    if method in ["-h", "--help"]:
        parser.parse_args(arguments[1:])
        exit()
    args = parser.parse_args(arguments[2:])

    if method == "ndx_show":
        ndx_show_name(args.input)
    elif method == "ndx_rm_dup":
        ndx_remove_duplicate(args.input, args.output)
    elif method == "ndx_rm":
        ndx_remove_group(args.input, args.output, args.grouplist, args.interactive)
    elif method == "ndx_preserve":
        ndx_preserve_group(args.input, args.output, args.grouplist, args.interactive)
    elif method == "ndx_add":
        ndx_add_group(
            args.input,
            args.output,
            args.groupname,
            args.start,
            args.end,
            args.step,
        )
    elif method == "ndx_combine":
        ndx_combine_group(args.input, args.output, args.groupname, args.grouplist)
    elif method == "ndx_rename":
        ndx_rename_group(
            args.input,
            args.output,
            args.oldname,
            args.newname,
            args.interactive,
        )
    else:
        print("Error -> unknown method {}".format(method))
        exit()

    print("Info -> good day !")


def main():
    ndx_call_functions()


if __name__ == "__main__":
    main()
