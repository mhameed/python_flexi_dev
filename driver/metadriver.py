import trio
import logging

class MetaDriver():

    def __init__(self, device=None, methodprefix=None, logfile='motion.log', loglevel=logging.WARNING, *args, **kwargs):
        super(MetaDriver, self).__init__(*args, **kwargs)
        self.device = device
        self.methodprefix = methodprefix
        self.logger = self.__logger = logging.getLogger('motion.MetaDriver')
        self.stop = False

    async def defaultAction(self, **kwargs):
        s = " ".join([f"'{k}':'{v}'" for k, v in kwargs.items()])
        self.logger.debug(f'defaultAction: {s}')

    async def run(self):
        self.__logger.info("Starting to listen to %s ..." % self.device)
        self.f = await trio.open_file(self.device, 'rb')
        while not self.stop:
            mname, kwargs = await self.readFromDevice()
            try:
                method = self.__getattribute__(mname)
            except AttributeError:
                await self.defaultAction(mname=mname, **kwargs)
                continue
            await method(**kwargs)
        await self.f.close()
        self.__logger.info("Shutting down.")
