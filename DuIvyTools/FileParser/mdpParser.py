"""
mdpParser module is part of DuIvyTools for parsing the mdp file of GROMACS.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


## totally re-construction may needed
class MDP(log):
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

        self.info(
            "MDP module could init some mdp templates for you. Specify application (-a) to generate a mdp file. "
        )
        self.info("Applications to choose: ions, em, nvt, npt, md, blank")
        self.warning(
            "the generated mdp file may be not appropriate for your system, CHECK IT YOURSELF !"
        )

    def gen_mdp(self, outmdp: str, application: str) -> None:
        """gen mdp template by specified application"""

        ## check parameters
        if outmdp == None or len(outmdp) <= 4 or outmdp[-4:] != ".mdp":
            self.error("output file name should be with suffix .mdp")
        if os.path.exists(outmdp):
            self.error("{} is already in current directory".format(outmdp))
        if application == None or application not in self.application_loc.keys():
            self.info(
                "application available:\n         {}".format(
                    " ".join(self.application_loc.keys())
                )
            )
            self.error("no application {} found".format(application))

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

        self.info(
            "generate {}.mdp for {} application successfully".format(
                outmdp, application
            )
        )


def mdp_gen(outmdp: str, application: str) -> None:
    """gen mdp templates"""

    mdp = MDP()
    mdp.gen_mdp(outmdp, application)
