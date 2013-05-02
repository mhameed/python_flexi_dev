import threading
from struct import unpack
import time
import plumbum
from plumbum.cmd import xte

running = 1
f = open('/dev/input/mice', 'rb')

x=0
y=0

def processMouse():
    global x
    global y
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
        time.sleep(0)

t1 = threading.Thread(target=processMouse)
t1.daemon = True
t1.start()
i=0
try:
    while i<1000:
        time.sleep(0.5)
        i+=1
        #print "i=%d, X=%d, Y=%d" % (i, x, y)
        if x == y:
            #print "nothing to do."
            continue
        if abs(x) > abs(y):
            if x>0:
                #print "moved to the right"
                xte['key Right']()
            else:
                print "moved to the left."
                xte['key Left']()
        else:
            if y>0:
                print "moved up."
                xte['key Up']()
            else:
                print "moved down."
                xte['key Down']()
        x = 0
        y = 0
except KeyboardInterrupt:
    pass
except Exception as err:
   raise 
#running=False
#t1.join()
print "shutting down."
