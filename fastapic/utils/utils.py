import base64
import configparser
import os


def get_config():
    config = configparser.ConfigParser()
    config.read(r"C:\Users\unc3rta1n\Desktop\work\hackaton\settings.ini")
    return config


