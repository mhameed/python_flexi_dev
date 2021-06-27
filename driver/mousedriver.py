from struct import unpack
from metadriver import MetaDriver
import logging

MOUSE_EVENT_LEFT_BUTTON = 0x1
MOUSE_EVENT_RIGHT_BUTTON = 0x2
MOUSE_EVENT_THIRD_BUTTON = 0x4
MOUSE_EVENT_FOURTH_BUTTON = 0x8
MOUSE_EVENT_LEFT = 0x10
MOUSE_EVENT_DOWN = 0x20
MOUSE_EVENT_SEVEN_BUTTON = 0x40
MOUSE_EVENT_EIGHTH_BUTTON = 0x80

class MouseDriver(MetaDriver):

    def __init__(self, device='/dev/input/mouse2', methodprefix='ms_', *args, **kwargs):
        super(MouseDriver, self).__init__(device=device, methodprefix=methodprefix, *args, **kwargs)
        self.logger = self.__logger = logging.getLogger('motion.MouseDriver')

    async def readFromDevice(self):
        n = unpack('B', await self.f.read(1))[0]
        x = unpack('b', await self.f.read(1))[0]
        y = unpack('b', await self.f.read(1))[0]

        mname = self.methodprefix +'btn%d' %n
        return (mname, {'n':n, 'x':x, 'y':y})
