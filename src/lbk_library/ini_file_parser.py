"""
A Wrapper around configparser for ini files.

File:       ini_file_parser.py
Author:     Lorn B Kerr
Copyright:  (c) 2022 Lorn B Kerr
License:    see License
"""

import configparser
import os
import sys
from typing import Any


class IniFileParser:
    """
    Exposes the stored configuation file (*.ini) as a standard dict.

    This uses the python 'configparser' object to provide 2 simple
    methods to read and write the full ini file. It initializes the
    config file directories and reads and writes ini files to and from
    the designated directories. For other needs, the full capabilities
    of the 'configparser' should be used.

    By default, it uses the standard Linux (Fedora) or Windows
    configuration locations.
    """

    def __init__(
        self, filename: str, program_config_subdir: str = "", config_dir: str = ""
    ) -> None:
        """
        Initialize the configuration file parser.

        This sets the configuration file location in the standard config
        directory, either '{HOME}/.config/lbk_software' for linux or
        '{HOME}/AppData/lbk_software' for Windows

        The resulting path to the config file is created if it does not
        already exist.

        Parameters:
            filename: (str) the config ini filename to be used.
            program_config_subdir: (str) (optional) the program specific
                config directory location for this config file. If not
                given, defaults to filename minus the suffix.
            config_dir: (str) Used if the standard, platform dependent,
                config directory location is not desired for some
                reason. (testing primarily)
        """
        home_dir = os.path.expanduser("~")

        self.config_file: str = ""
        """The full path to the ini file """

        # set the program config sub-dirirectory if not present
        if not program_config_subdir:
            program_config_subdir = os.path.splitext(filename)[0]

        # set the full path to the program config file directiory
        if not config_dir:
            if sys.platform.startswith("linux"):
                config_dir = os.path.join(
                    home_dir, ".config", "lbk_software", program_config_subdir
                )
            elif sys.platform.startswith("win"):
                config_dir = os.path.join(
                    home_dir, "AppData", "Local", "lbk_software", program_config_subdir
                )

        else:
            config_dir = os.path.join(config_dir, program_config_subdir)

        # if no path to config file, create path
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, 0o744)

            # build the absolute file name.
        self.config_file = os.path.join(config_dir, filename)

    def read_config(self) -> dict[str, Any]:
        """
        Read the configuration file.

        Everything is treated as a string, so any numbers or booleans
        will need to be converted separately.

        Returns:
            (dict) The saved configuration settings. If the config file
            does not exist, returns an empty dict object
        """
        config: dict[str, Any] = {}
        config_parser = configparser.ConfigParser(allow_no_value=True)

        # read the file
        if os.path.exists(self.config_file):
            config_parser.read_file(open(self.config_file, "r"))
            for section in config_parser.sections():
                config[section] = {}
                for key in config_parser[section]:
                    config[section][key] = config_parser[section].get(key)
        return config

    # end get_config()

    def write_config(self, new_config: dict[str, Any]) -> None:
        """
        Save the config values to the file.

        Parameters:
            new_config: (dict) The new configuration settings to save.
        """
        config_parser = configparser.ConfigParser(allow_no_value=True)
        config_parser.read_dict(new_config)
        config_parser.write(open(self.config_file, "w"))

    # end write_config()

    def config_path(self) -> str:
        """
        Provide the absolute path to the config file.

        Returns:
            (str) The absolute path to the config file.
        """
        return self.config_file

    # end config_path()


# end class IniFileParser
