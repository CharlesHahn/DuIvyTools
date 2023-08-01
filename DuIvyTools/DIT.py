"""
DIT module is part of DuIvyTools. This module provides log parent class.

Written by DuIvy and provided to you by GPLv3 license.
"""


from Commands.xvgCommands import *
from utils import Parameters, log
import inspect


class DIT(log):
    def __init__(self) -> None:
        self.cmds = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass))

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
