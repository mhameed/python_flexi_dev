from struct import unpack
import time
import threading
import logging
import plumbum
from plumbum.cmd import xte

# possible types: taken from joystick.h
JS_EVENT_BUTTON = 0x01    # button pressed/released
JS_EVENT_AXIS = 0x02    # joystick moved
JS_EVENT_INIT = 0x80    # initial state of device

class Driver(threading.Thread):

    def __init__(self, device='/dev/input/js0', methodprefix='js_', logfile='motion.log', loglevel=logging.WARNING, *args, **kwargs):
        super(Driver, self).__init__(*args, **kwargs)
        self.device = device
        self.methodprefix = methodprefix
        self._stop = threading.Event()
        logging.basicConfig(filename=logfile,
            level=loglevel,
            format='%(asctime)s - %(levelname)s - %(message)s')

    def stop(self):
        self._stop.set()

    def run(self):
        logging.info("motion driver: starting.")
        self.f = open(self.device, 'rb')
        while not self._stop.isSet():

            etime = unpack('I', self.f.read(4))[0]
            evalue = unpack('h', self.f.read(2))[0]
            etype = unpack('B', self.f.read(1))[0]
            enumber = unpack('B', self.f.read(1))[0]

            mname = ''
            if etype & JS_EVENT_INIT: continue
            if etype & JS_EVENT_BUTTON:
                mname = 'btn%d' 
            if etype & JS_EVENT_AXIS:
                mname = 'axis%d'
            if not mname: continue
            mname=self.methodprefix + mname % enumber
            try:
                method = self.__getattribute__(mname)
            except AttributeError:
                logging.warning('method for %s not implemented.'%mname)
                continue
            method(evalue)
            time.sleep(0)

        self.f.close()
        logging.info("motion driver: shutting down.")
