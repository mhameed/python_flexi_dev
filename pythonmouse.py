from struct import unpack
import time
running = 1
f = open('/dev/input/mice', 'rb')
try:
    oldx = 0
    oldy = 0
    x = 0
    y = 0
    while running:
        c = f.read(1)
        b2 = f.read(1)
        b3 = f.read(1)
        tmpx = ord(b2)  # from char to int
        tmpy = ord(b3)

        if tmpx > 128:
                tmpx -= 255
        if tmpy > 128:
                tmpy -= 255
        x += tmpx
        y += tmpy
        print "X=%d, Y=%d" % (x, y)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nBye.")
