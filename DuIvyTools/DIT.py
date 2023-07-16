"""
DIT module is part of DuIvyTools. This module provides log parent class.

Written by DuIvy and provided to you by GPLv3 license.
"""

import logging
from colorama import Fore, Back, Style


class log(object):
    """log class, a logging system parent class, provied five functions for 
    output debug, info, warning, error, and critical messages.
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s[line:%(lineno)d]\n%(message)s",
    )
    logger = logging.getLogger(__name__)

    def debug(self, msg):
        self.logger.debug(Fore.CYAN + Back.WHITE + f"Debug -> {msg}" + Style.RESET_ALL)

    def info(self, msg):
        self.logger.info(Fore.GREEN + f"Info -> {msg}" + Style.RESET_ALL)

    def warn(self, msg):
        self.logger.warning(Fore.YELLOW + f"Warning -> {msg}" + Style.RESET_ALL)

    def error(self, msg):
        self.logger.error(Fore.WHITE + Back.RED + f"Error -> {msg}" + Style.RESET_ALL)

    def critical(self, msg):
        self.logger.critical(
            Fore.WHITE + Back.RED + f"CRITICAL -> {msg}" + Style.RESET_ALL
        )


class DIT(object):
    pass