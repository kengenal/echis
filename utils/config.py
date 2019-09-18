import configparser
import sys
import os
import logging


def config():
    try:
        cnf = configparser.ConfigParser()
        cnf.read('config.ini')
        cnf.sections()
    except Exception as error:
        print(error)
    if cnf:
        return cnf
    else:
        print("File doesn't exists")


def log():
    return logging.basicConfig(
        filename='/data/logs/nieaktywne_hosty.log',
        level=logging.WARNING, format='%(asctime)s %(message)s'
    )
