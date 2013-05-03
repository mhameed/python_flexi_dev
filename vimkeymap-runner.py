import time
from vimkeymap import VimKeymap

d = VimKeymap()
try:
    d.start()
    time.sleep(120)
except KeyboardInterrupt:
    pass
d.stop()
d.join()
