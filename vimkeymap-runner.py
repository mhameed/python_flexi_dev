import time
import logging
from vimkeymap import VimKeymap

logger = logging.getLogger('motion')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('motion.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

d = VimKeymap()
d.start()
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    d.stop()
    d.join()
