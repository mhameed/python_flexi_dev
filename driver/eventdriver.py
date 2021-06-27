from struct import unpack
from metadriver import MetaDriver
import logging

class EventDriver(MetaDriver):

    def __init__(self, device='/dev/input/event10', methodprefix='kbd_', *args, **kwargs):
        super(EventDriver, self).__init__(device=device, methodprefix=methodprefix, *args, **kwargs)
        self.logger = self.__logger = logging.getLogger('motion.EventDriver')

    async def readFromDevice(self):
        etime = await self.f.read(16)
        etype = unpack('H', await self.f.read(2))[0]
        ecode = unpack('H', await self.f.read(2))[0]
        evalue = unpack('I', await self.f.read(4))[0]
        if etype not in [1,2,3]:
            return ('', {'etype':etype, 'ecode':ecode, 'evalue':evalue})

        mname = self.methodprefix + 'btn%d' % ecode
        return (mname, {'etype':etype, 'ecode':ecode, 'evalue':evalue})

