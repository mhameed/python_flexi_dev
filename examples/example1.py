#!/usr/bin/env python3
import logging
import sys
import trio
import flexi_dev.mousedriver as msd

class MickeyMouse(msd.MouseDriver):
    def __init__(self, device, *args, **kwargs):
        super(MickeyMouse, self).__init__(device=device, *args, **kwargs)

    async def defaultAction(self, **kwargs):
        await super().defaultAction(**kwargs)
        n = kwargs.get('n')
        if n & msd.MOUSE_EVENT_LEFT_BUTTON:
            print("left button pressed")
        if n & msd.MOUSE_EVENT_RIGHT_BUTTON:
            print("right button pressed")
        if n & msd.MOUSE_EVENT_THIRD_BUTTON:
            print("middle button pressed, quitting.")
            self.stop = True

logger = logging.getLogger('flexi_dev')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('flexi_dev.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

m = MickeyMouse('/dev/input/by-id/usb-17ef_Lenovo_Ultraslim_Plus_Wireless_Keyboard___Mouse-if01-mouse')
trio.run(m.run)
