import sys
import time
import logging
import importlib

if len(sys.argv) != 2:
    print "usage."
    sys.exit(1)

mod = importlib.import_module(sys.argv[1])
logname = sys.argv[1].split('.')[-1]

logger = logging.getLogger('motion')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('%s.log' %logname)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

d = mod.Mapping()
d.start()
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    d.stop()
    d.join()