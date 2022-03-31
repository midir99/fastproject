"""Application configuration module.

Here the configuration from file ".env" gets loaded into a Python
configparser.ConfigParser object.
"""

import configparser
import pathlib

settings = configparser.ConfigParser()
settings.read(pathlib.Path(__file__).resolve().parent / ".env")
