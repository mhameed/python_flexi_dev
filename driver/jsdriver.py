from struct import unpack
import plumbum
from plumbum.cmd import xte
from metadriver import MetaDriver
import logging

# possible types: taken from joystick.h
JS_EVENT_BUTTON = 0x01    # button pressed/released
JS_EVENT_AXIS = 0x02    # joystick moved
JS_EVENT_INIT = 0x80    # initial state of device

class JSDriver(MetaDriver):

    def __init__(self, device='/dev/input/js0', methodprefix='js_', *args, **kwargs):
        super(JSDriver, self).__init__(device=device, methodprefix=methodprefix, *args, **kwargs)
        self.__logger = logging.getLogger('motion.JSDriver')

    def dispatcher(self):
        etime = unpack('I', self.f.read(4))[0]
        evalue = unpack('h', self.f.read(2))[0]
        etype = unpack('B', self.f.read(1))[0]
        enumber = unpack('B', self.f.read(1))[0]

        mname = ''
        if etype & JS_EVENT_INIT: return
        if etype & JS_EVENT_BUTTON:
            mname = 'btn%d' 
        if etype & JS_EVENT_AXIS:
            mname = 'axis%d'
        if not mname: return
        mname=self.methodprefix + mname % enumber
        try:
            method = self.__getattribute__(mname)
        except AttributeError:
            self.__logger.warning('method for %s not implemented.'%mname)
            return
        method(evalue)

