import time
from vimkeymap import VimKeymap

d = VimKeymap()
d.start()
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    d.stop()
    d.join()
