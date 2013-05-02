import threading
from struct import unpack
import time
import logging
import plumbum
from plumbum.cmd import xte

class Driver():


    def processMotionData(self):
        while True:
            n = unpack('B', self.f.read(1))[0]
            self.x += unpack('b', self.f.read(1))[0]
            y = unpack('b', self.f.read(1))[0]

            # process button states:
            leftbutton = n & 0x1
            rightbutton = n & 0x2
            threeb = n & 0x4
            fourb = n & 0x8
            left = n & 0x10
            down = n & 0x20 
            sevenb = n & 0x40
            eightb = n & 0x80
            if leftbutton > 0:
                self.b1state = not self.b1state
                logging.info("b1 pressed, new b1state=%d" % self.b1state)
            if rightbutton > 0:
                self.b3state = not self.b3state
                logging.info("b3 pressed, new b3state=%d" % self.b3state)
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
