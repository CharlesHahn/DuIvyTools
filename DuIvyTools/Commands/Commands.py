"""
Commands module is part of DuIvyTools providing basic Commands class.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
import sys
import time
from typing import List, Union

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils import log


class Command(log):
    def __init__(self) -> None:
        pass

    def sel_parm(self, *args) -> None:

        if len(args) < 1:
            self.critical("wrong length of parameters selcetion")
        for item in args:
            if item != None:
                return item
        else:
            return args[0]

    def get_parm(self, key: str) -> None:
        value = self.parm.__dict__.get(key, None)
        if value != None:
            return value
        value = self.file.__dict__.get(key, None)
        if value != None:
            return value
        return None
