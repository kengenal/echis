import configparser
import sys
import os
#sys.path.insert(0, os.path.abspath('..'))

def config(dev=None):
    cnf = configparser.ConfigParser()
    filename = 'config'
    if dev is not None:
        filename = 'config.dev.ini'
    cnf.read(filename)
    cnf.sections()
    if cnf:
        return cnf
    else:
        print("File doesn't exists")
       
