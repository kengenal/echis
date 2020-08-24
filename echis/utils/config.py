import configparser
import sys
import os
import logging


def config():
    try:
        cnf = configparser.ConfigParser()
        cnf.read('helper.ini')
        cnf.sections()
    except Exception:
        return "command not found"
    if cnf:
        return cnf

