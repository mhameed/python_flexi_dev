import time
import threading
import logging

class MetaDriver(threading.Thread):

    def __init__(self, device=None, methodprefix=None, logfile='motion.log', loglevel=logging.WARNING, *args, **kwargs):
        super(MetaDriver, self).__init__(*args, **kwargs)
        self.device = device
        self.methodprefix = methodprefix
        self._stop = threading.Event()
        self.__logger = logging.getLogger('motion.MetaDriver')

    def stop(self):
        self.__logger.info('Setting stop flag.')
        self._stop.set()

    def dispatcher(self):
        pass

    def run(self):
        self.__logger.info("Starting...")
        self.f = open(self.device, 'rb')
        while not self._stop.isSet():
            self.dispatcher()
            time.sleep(0)
        self.f.close()
        self.__logger.info("Shutting down.")
