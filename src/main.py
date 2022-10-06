import os
from pyLib.screen import screen

if __name__ == "__main__":
    try:
        screen.run(log="textual.log", log_verbosity=2, title="PatinhOS :duck:")
    except SystemExit:
        os._exit(0)
