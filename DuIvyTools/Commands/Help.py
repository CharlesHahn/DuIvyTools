"""
Help module is part of DuIvyTools providing help infomation.

Written by DuIvy and provided to you by GPLv3 license.
"""


from Commands.Commands import Command

class Help(Command):
    def __init__(self) -> None:
        self.cmd_parms = {
            "xvg_show": ["input", "begin", "end", "dt", "xshrink", "yshrink", "legends", "xmin", "xmax", "ymin", "ymax", "xlabel", "ylabel", "title", "x_precision", "y_precision", "engine", "output", "noshow"],
            "xvg_show": ["input", "columns", "showMV", "windowsize", "confidence", "alpha", "csv", "begin", "end", "dt", "xshrink", "yshrink", "legends", "xmin", "xmax", "ymin", "ymax", "xlabel", "ylabel", "title", "x_precision", "y_precision", "engine", "output", "noshow"],
            "xvg_ave":["begin", "end", "dt", "input", "output"],
        }

        ## TODO: through read the commands original code to parse the used parm?

