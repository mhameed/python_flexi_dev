import threading
from struct import unpack
import time
import logging
import plumbum
from plumbum.cmd import xte

### Start configuration area:

# dict of which keys to send at what event.
mykeys = {}

# verticalMotion, if 1 send left/right, else send up/down
mykeys[0,0,0]=(['key Down'], ['key Up'])
mykeys[1,0,0]=(['key Right'], ['key Left'])

# vimMode, send hjkl instead of arrow keys.
mykeys[0,0,1]=(['key j'], ['key k'])
mykeys[1,0,1]=(['key l'], ['key h'])


# Minimum time that should pass before sending consecutive keys
keyDelay=0.35

# If new pointer location within boundary of x after keyDelay, then dont act, consider it as noise.
boundary=50

# Which input device should be used.
device = '/dev/input/mouse1'

logfile='motion.log'
loglevel=logging.INFO
### end of configuration area

logging.basicConfig(filename=logfile,
    level=loglevel,
    format='%(asctime)s - %(levelname)s - %(message)s')

x=0
b1state=0
b2state=0
b3state=0
logging.info("motion driver: starting.")
f = open(device, 'rb')

def processMotionData():
    global x
    global b1state
    global b2state
    global b3state
    while True:
        c = f.read(1)
        b2 = f.read(1)
        b3 = f.read(1)
        tmpx = ord(b2)  # from char to int
        if tmpx > 128:
                tmpx -= 255
        x += tmpx

        # process button states:
        n = ord(c)
        button_state = [n & (1 << i) for i in xrange(8)]
        i = iter(button_state)
        leftbutton = i.next()
        rightbutton = i.next()
        threeb = i.next()
        fourb = i.next()
        left = i.next()
        down = i.next()
        sevenb = i.next()
        eightb = i.next()
        if leftbutton > 0:
                b1state = not b1state
                logging.info("b1 pressed, new b1state=%d" % b1state)
        if rightbutton > 0:
                b3state = not b3state
                logging.info("b3 pressed, new b3state=%d" % b3state)
        time.sleep(0)


t1 = threading.Thread(target=processMotionData)
t1.daemon = True
t1.start()
try:
    while True:
        time.sleep(keyDelay)
        if abs(x) < boundary: continue
        try:
            keys1, keys2 = mykeys[b1state, b2state, b3state] 
        except KeyError, ValueError:
            logging.warning("No such state defined.")
            continue

        if x>0:
            logging.debug("Rightward motion detected, submitting xte keys")
            xte[tuple(keys1)]()
        else:
            logging.debug("Leftward motion detected, submitting xte keys")
            xte[tuple(keys2)]()
        x = 0
except KeyboardInterrupt:
    pass
except Exception as err:
   raise 
logging.info("motion driver: shutting down.")
