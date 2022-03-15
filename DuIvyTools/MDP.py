"""
MDP module is part of DuIvyTools library, which is a tool for analysis and 
visualization of GROMACS result files. This module is written by CharlesHahn.

This module is designed to generate .mdp file templates. 

This MDP module contains:
    - MDP class

This file is provided to you by GPLv2 license."""


import os
import sys
import argparse


class MDP(object):
    """
    class MDP are designed to generate kinds of mdp files

    """

    def __init__(self) -> None:
        """init the MDP class"""

        self.application_loc = {
            "ions": os.path.join("data", "ions.mdp"),
            "em": os.path.join("data", "em.mdp"),
            "nvt": os.path.join("data", "nvt.mdp"),
            "npt": os.path.join("data", "npt.mdp"),
            "md": os.path.join("data", "md.mdp"),
            "blank": os.path.join("data", "blank.mdp"),
        }

        print("Info -> MDP module could init some mdp templates for you.")
        print("        Specify application (-a) to generate a mdp file. ")
        print("Info -> applications to choose: ions, em, nvt, npt, md, blank")
        print("\nWARNING -> the generated mdp file may be not appropriate")
        print("            for your system, CHECK IT YOURSELF !\n")

    def gen_mdp(self, outmdp: str, application: str) -> None:
        """gen mdp template by specified application"""

        ## check parameters
        if outmdp == None or len(outmdp) <= 4 or outmdp[-4:] != ".mdp":
            print("Error -> output file name should be with suffix .mdp")
            exit()
        if os.path.exists(outmdp):
            print("Error -> {} is already in current directory".format(outmdp))
            exit()
        if application == None or application not in self.application_loc.keys():
            print(
                "Info -> application available:\n         {}".format(
                    " ".join(self.application_loc.keys())
                )
            )
            print("Error -> no application {} found".format(application))
            exit()

        ## gen mdp
        data_file_path = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        with open(
            os.path.join(data_file_path, self.application_loc[application]), "r"
        ) as fo:
            content = fo.read()
        with open(outmdp, "w") as fo:
            fo.write(content)

        print(
            "Info -> generate {}.mdp for {} application successfully".format(
                outmdp, application
            )
        )


def mdp_gen(outmdp: str, application: str) -> None:
    """gen mdp templates"""

    mdp = MDP()
    mdp.gen_mdp(outmdp, application)


def mdp_call_functions(arguments: list = None):
    """call functions according to arguments"""

    if arguments == None:
        arguments = [argv for argv in sys.argv]

    ## parse the command parameters
    parser = argparse.ArgumentParser(description="generate mdp file templates")
    parser.add_argument("-o", "--output", help="file name to output")
    parser.add_argument(
        "-a",
        "--application",
        choices=["ions", "em", "nvt", "npt", "md", "blank"],
        help="specify the application of mdp, choices: ions, em, nvt, npt, md, blank",
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
    if method == "mdp_gen":
        mdp_gen(args.output, args.application)
    else:
        print("Error -> unknown method {}".format(method))
        exit()

    print("Info -> good day !")


def main():
    mdp_call_functions()


if __name__ == "__main__":
    main()
