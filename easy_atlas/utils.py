# python 2.7 uses ConfigParser, python 3 uses configparser

import os
from .EAGlobals import PythonVersion_Major

if PythonVersion_Major <= 2:
    import ConfigParser
else:
    import configparser as ConfigParser


class INIHandler:
    """INIHandler simplifies the load/save information on INI style files."""

    @staticmethod
    def load_info(configPath, option, debug=False):
        """
        Load info from config file.

        :param configPath: Filepath to config file
        :param option: field where the information will be read from
        :param bool debug: boolean for printing debug information in the script editor
        """
        configFilename = configPath.replace("\\\\", "/")

        config = ConfigParser.RawConfigParser()
        config.read(configFilename)
        info = ""
        try:
            info = config.get("ROOT", option)
        except:
            pass

        if debug:
            print(configFilename)

        return info

    @staticmethod
    def save_info(configPath, option, info, debug=False):
        """
        Save info into config file.

        :param configPath: Filepath to config file
        :param option: field where the information will be read from
        :param info: information that will be stored
        :param bool debug: boolean for printing debug information in the script editor
        """
        configFilename = os.path.abspath(configPath)
        configDirectory = os.path.dirname(configFilename)

        config = ConfigParser.RawConfigParser()
        config.read(configFilename)
        try:
            config.add_section('ROOT')
        except:
            pass
        config.set('ROOT', option, info)

        if not os.path.exists(configDirectory):
            os.makedirs(configDirectory)

        mode = "w"
        if PythonVersion_Major == 2:
            mode += "+b"

        with open(configFilename, mode) as configfile:
            config.write(configfile)

        if debug:
            print(configFilename)
