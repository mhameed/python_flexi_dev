import threading
from struct import unpack
import time
import logging
import plumbum
from plumbum.cmd import xte

class Driver():


    def processMotionData(self):
        while True:
            c = self.f.read(1)
            b2 = self.f.read(1)
            b3 = self.f.read(1)
            tmpx = ord(b2)  # from char to int
            if tmpx > 128:
                tmpx -= 255
            self.x += tmpx

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
