import sys

from utils.TerminalColors import TerminalColors

plugins = dict()


def cli(_func=None, *, desc=""):
    def decorator_cli(func):
        plugins[func.__name__] = {
            "func": func,
            "description": desc
        }

    if _func is None:
        return decorator_cli
    else:
        return decorator_cli(_func)


def run(plug: dict):
    args = sys.argv
    print(len(args))
    if len(args) >= 2:
        get = plug[args[1]]
        fun = get["func"]
        fun()
    else:
        print(TerminalColors.BOLD + "[Commends]" + TerminalColors.ENDC)
        print("--------------------")
        for key, val in plug.items():
            des = val["description"]
            if not des:
                des = None
            print("  ", key, ":", des)
        print("--------------------")
