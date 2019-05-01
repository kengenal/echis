import configparser
import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

def config(name=None):
    cnf = configparser.ConfigParser()
    cnf.read('config.ini')
    cnf.sections()
    if name is not None:
        if cnf[name]:
            return cnf[name]
        else:
            return "This variable does not exists"
    else:
        return cnf
