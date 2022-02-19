import configparser
from pathlib import Path

settings = configparser.ConfigParser()
settings.read(Path(__file__).resolve().parent / ".env")
