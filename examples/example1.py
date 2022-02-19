#!/usr/bin/env python3
import logging
import sys
import trio
from flexi_dev.MouseDriver import MouseDriver

class MickeyMouse(MouseDriver):
    def __init__(self, device, *args, **kwargs):
        super(MickeyMouse, self).__init__(device=device, *args, **kwargs)

    async def ms_btn9(self, **kwargs):
        print("left button pressed")

    async def ms_btn10(self, **kwargs):
        print("right button pressed, quitting...")
        sys.exit() 

logger = logging.getLogger('flexi_dev')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('flexi_dev.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

m = MickeyMouse('/dev/input/by-id/usb-17ef_Lenovo_Ultraslim_Plus_Wireless_Keyboard___Mouse-if01-mouse')
trio.run(m.run)
