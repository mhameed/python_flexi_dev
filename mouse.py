import logging
from driver import Driver

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
d = Driver(mykeys,device)
d.start()

