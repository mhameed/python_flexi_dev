import threading
from struct import unpack
import time
import logging
import plumbum
from plumbum.cmd import xte

# possible types: taken from joystick.h
JS_EVENT_BUTTON = 0x01    # button pressed/released
JS_EVENT_AXIS = 0x02    # joystick moved
JS_EVENT_INIT = 0x80    # initial state of device

class Driver():


    def processMotionData(self):
        while True:
            etime = unpack('I', self.f.read(4))[0]
            evalue = unpack('h', self.f.read(2))[0]
            etype = unpack('B', self.f.read(1))[0]
            enumber = unpack('B', self.f.read(1))[0]

            if etype & JS_EVENT_INIT: continue
            if etype & JS_EVENT_BUTTON:
                print("btn%x, v=%i" % (enumber,evalue))
            if etype & JS_EVENT_AXIS:
                print("axis%x, v=%i" % (enumber,evalue))
            time.sleep(0)

    def __init__(self, keymap, device, boundary=50, keyDelay=0.35, logfile='motion.log', loglevel=logging.WARNING):
        self.f = None
        self.x=0
        self.b1state=0
        self.b2state=0
        self.b3state=0
        self.keyDelay = keyDelay
        self.boundary = boundary
        self.device = device
        self.keymap = keymap
        logging.basicConfig(filename=logfile,
            level=loglevel,
            format='%(asctime)s - %(levelname)s - %(message)s')

    def start(self):
        logging.info("motion driver: starting.")
        self.f = open(self.device, 'rb')

        t1 = threading.Thread(target=self.processMotionData)
        t1.daemon = True
        t1.start()
        try:
            while True:
                time.sleep(self.keyDelay)
                if abs(self.x) < self.boundary: continue
                try:
                    keys1, keys2 = self.keymap[self.b1state, self.b2state, self.b3state] 
                except KeyError, ValueError:
                    logging.warning("No such state defined.")
                    continue

                if self.x>0:
                    logging.debug("Rightward motion detected, submitting xte keys")
                    xte[tuple(keys1)]()
                else:
                    logging.debug("Leftward motion detected, submitting xte keys")
                    xte[tuple(keys2)]()
                self.x = 0
        except KeyboardInterrupt:
            pass
        except Exception as err:
            raise 
        self.f.close()
        logging.info("motion driver: shutting down.")
