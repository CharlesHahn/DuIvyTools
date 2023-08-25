"""
mdpParser module is part of DuIvyTools for parsing the mdp file of GROMACS.

Written by DuIvy and provided to you by GPLv3 license.
"""

import os
from typing import List, Dict, Union

from utils import log


class MDP(log):
    """class MDP are designed to parse key and values of mdp file"""

    def __init__(
        self, mdpfile: str, is_file: bool = True, new_file: bool = False
    ) -> None:
        self.mdps: Dict[str, str]
        if new_file:
            self.mdpfile = mdpfile
        else:
            if is_file:
                self.mdpfile = mdpfile
                if not os.path.exists(mdpfile):
                    self.error(f"No {mdpfile} detected ! check it !")
                if mdpfile[-4:] != ".mdp":
                    self.error(
                        f"you must specify a file with suffix .mdp instead of {mdpfile}"
                    )
                with open(mdpfile, "r") as fo:
                    content = fo.read()
            else:
                content = mdpfile
            lines = [l.strip() for l in content.strip().split("\n")]
            self.parse_mdp(lines)
            if is_file:
                self.info(f"parsing data from {mdpfile} successfully !")

    def parse_mdp(self, lines: List[str]) -> None:
        """parse mdp file into MDP"""
        for line in lines:
            key_value = line.split(";")[0].strip().split("=")
            if len(key_value) == 1:
                key = key_value[0].strip()
                key = key.replace("_", "-")
                self[key] = ""
            elif len(key_value) == 2:
                key = key_value[0].strip()
                key = key.replace("_", "-")
                value = key_value[1].strip()
                self[key] = value
            else:
                self.error(
                    f"Error occured when paring {self.mdpfile} at line: \n {line}"
                )

    def __setitem__(self, key: str, value: str) -> None:
        """set key and value in mdps, key and value must be string"""
        if not isinstance(key, str) or not isinstance(value, str):
            self.error(
                f"Error in setitem, key {key} and value {value} must be string type"
            )
        self.mdps[key] = value

    def __getitem__(self, key: str) -> Union[str, None]:
        """return value of specified key, or return None if no key in mdps"""
        if not isinstance(key, str):
            self.error(f"key {key} must be string type")
        if key in self.mdps.keys():
            return self.mdps[key]
        else:
            return None

    def __len__(self) -> int:
        """return the number of key value pairs in mdps"""
        return len(self.mdps.keys())

    def __delitem__(self, key: str) -> None:
        """delete key value pair by key"""
        if not isinstance(key, str):
            self.error(f"key {key} must be string type")
        if key in self.mdps.keys():
            del self.mdps[key]

    def __str__(self) -> str:
        """return all keys in self.mdps"""
        output: str = ""
        for key, value in self.mdps.items():
            output += f"{key:<25} = {value:<20} \n"
        return output

    def save(self, mdpfile: str) -> None:
        """dump MDP to mdp file"""
        with open(mdpfile, "w") as fo:
            fo.write(str(self))
