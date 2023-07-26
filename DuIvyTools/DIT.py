"""
DIT module is part of DuIvyTools. This module provides log parent class.

Written by DuIvy and provided to you by GPLv3 license.
"""

import sys
import logging
import argparse
from colorama import Fore, Back, Style


from Commands.xvgCommands import xvgShow
from utils import Parameters


class DIT(object):
    pass


## try to run DIT
parm = Parameters()
cmd = xvgShow(parm)
cmd()
