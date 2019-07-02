import configparser
import sys
import os
sys.path.insert(0, os.path.abspath('../'))

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
       
