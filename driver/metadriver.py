import trio
import logging

class MetaDriver():

    def __init__(self, device=None, methodprefix=None, logfile='motion.log', loglevel=logging.WARNING, *args, **kwargs):
        super(MetaDriver, self).__init__(*args, **kwargs)
        self.device = device
        self.methodprefix = methodprefix
        self.logger = self.__logger = logging.getLogger('motion.MetaDriver')
        self.stop = False

    async def dispatcher(self):
        pass

    def defaultAction(self, mname, label, value):
            self.logger.warning('%s not implemented (%s, %s).' % (mname, label, value))

    async def run(self):
        self.__logger.info("Starting to listen to %s ..." % self.device)
        self.f = await trio.open_file(self.device, 'rb')
        while not self.stop:
            await self.dispatcher()
        await self.f.close()
        self.__logger.info("Shutting down.")
