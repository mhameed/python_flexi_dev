#!/usr/bin/env python3
import logging
import math
import sys
import trio
import flexi_dev.mousedriver as msd

compass_brackets = [
    "North", "North East", "East",
    "South East", "South", "South West",
    "West", "North West", "North"
]

class CompassDirections(msd.MouseDriver):
    def __init__(self, device, *args, **kwargs):
        super(CompassDirections, self).__init__(device=device, *args, **kwargs)
        self.absX = 0
        self.absY = 0
        self.prevAbsX = 0
        self.prevAbsY = 0
        self.triggerDistance = 300

    async def defaultAction(self, *args, **kwargs):
        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)
        self.absX += x
        self.absY += y
        xdelta = self.absX - self.prevAbsX
        ydelta = self.absY - self.prevAbsY
        # pythagoras
        distance = math.sqrt(xdelta**2 + ydelta**2)
        if distance >= self.triggerDistance:
            self.prevAbsX = self.absX
            self.prevAbsY = self.absY
            degrees = math.atan2(xdelta, ydelta)/math.pi*180
            if degrees < 0:
                degrees += 360
            print(compass_brackets[round(degrees / 45)])

    async def ms_btn9(self, **kwargs):
        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)
        if x==0 and y==0:
            print("left button pressed, quitting...")
            self.stop = True

logger = logging.getLogger('flexi_dev')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('flexi_dev.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

m = CompassDirections('/dev/input/mouse2')
trio.run(m.run)
