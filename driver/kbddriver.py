from struct import unpack
from metadriver import MetaDriver
import logging

class KBDDriver(MetaDriver):

    def __init__(self, device='/dev/input/event10', methodprefix='kbd_', *args, **kwargs):
        super(KBDDriver, self).__init__(device=device, methodprefix=methodprefix, *args, **kwargs)
        self.logger = self.__logger = logging.getLogger('motion.KBDDriver')

    def dispatcher(self):
        etime = self.f.read(16)
        etype = unpack('H', self.f.read(2))[0]
        ecode = unpack('H', self.f.read(2))[0]
        evalue = unpack('I', self.f.read(4))[0]
        if etype != 1: return

        mname=self.methodprefix + 'btn%d' % ecode
        try:
            method = self.__getattribute__(mname)
        except AttributeError:
            self.defaultAction(mname, ecode, evalue)
            return
        method(evalue)

