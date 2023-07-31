"""
DIT module is part of DuIvyTools. This module provides log parent class.

Written by DuIvy and provided to you by GPLv3 license.
"""


from Commands.xvgCommands import *
from utils import Parameters, log


class DIT(log):
    def __init__(self) -> None:
        self.cmds = {
            "xvg_show":xvg_show,
            "xvg_compare":xvg_compare,
            "xvg_ave":xvg_ave,
            "xvg_rama":xvg_rama,
            "xvg_show_distribution":xvg_show_distribution,
            "xvg_show_stack":xvg_show_stack,
            "xvg_show_scatter":xvg_show_scatter,
            "xvg_energy_compute":xvg_energy_compute,
            "xvg_combine":xvg_combine,
            "xvg_ave_bar":xvg_ave_bar,
            "xvg_box":xvg_box,
            "xvg_violin":xvg_violin,
        }

    def run(self) -> None:
        ## try to run DIT
        parm = Parameters()
        cmd = self.cmds.get(parm.cmd, None)
        if cmd == None:
            self.error("Wrong selection of command, type 'dit help' to see all possible commands")
        cmd = cmd(parm)
        cmd()



if __name__ == "__main__":
    dit = DIT()
    dit.run()
    dit.info("May you good day !")
