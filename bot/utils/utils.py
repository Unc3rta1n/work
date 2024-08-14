import base64
import configparser
import os


def get_config():
    config = configparser.ConfigParser()
    config.read(r"settings.ini")
    return config


def generate_base64_id(length=11):
    random_bytes = os.urandom(length)
    base64_id = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return base64_id.rstrip('=')
