import os
from pyLib.clock import clock
from pyLib.screen import screen

if __name__ == "__main__":
    try:
        clock().start()
        screen.run(log="textual.log", log_verbosity=2, title="PatinhOS :duck:")
        clock().stop()
    except:
        clock().stop()
        os._exit(0)
