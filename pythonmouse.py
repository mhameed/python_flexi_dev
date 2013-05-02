import threading
from struct import unpack
import time
import plumbum
from plumbum.cmd import xte

running = 1
f = open('/dev/input/mouse1', 'rb')

boundary=50
x=0
#y=0

b1state=0
b2state=0
b3state=0


# dict of which keys to send at what event.
mykeys = {}

# verticalMotion, if 1 send left/right, else send up/down
mykeys[0,0,0]=('Down', 'Up')
mykeys[1,0,0]=('Right', 'Left')

# vimMode, send hjkl instead of arrow keys.
mykeys[0,0,1]=('j', 'k')
mykeys[1,0,1]=('l', 'h')

def processMouse():
    global x
    #global y
    global b1state
    global b2state
    global b3state
    while running:
        c = f.read(1)
        b2 = f.read(1)
        b3 = f.read(1)
        tmpx = ord(b2)  # from char to int
        #tmpy = ord(b3)
        if tmpx > 128:
                tmpx -= 255
        #if tmpy > 128:
        #        tmpy -= 255
        x += tmpx
        #y += tmpy

        # process button states:
        n = ord(c)
        button_state = [n & (1 << i) for i in xrange(8)]
        i = iter(button_state)
        leftbutton = i.next()
        rightbutton = i.next()
        threeb = i.next()
        fourb = i.next()
        left = i.next()
        down = i.next()
        sevenb = i.next()
        eightb = i.next()
        if leftbutton > 0:
                print "LEFTBUTTON"
                b1state = not b1state
        if rightbutton > 0:
                print "RIGHTBUTTON"
                b3state = not b3state

        time.sleep(0)


t1 = threading.Thread(target=processMouse)
t1.daemon = True
t1.start()
i=0
try:
    while i<1000:
        time.sleep(0.35)
        i+=1
        if x == 0:
            continue

        if abs(x)<boundary: continue
        key1, key2 = mykeys[b1state, b2state, b3state] 
        if x>0:
            #print "moved to the right"
            xte['key %s' %key1]()
        else:
            print "moved to the left."
            xte['key %s'%key2]()
        x = 0
        #y = 0
except KeyboardInterrupt:
    pass
except Exception as err:
   raise 
#running=False
#t1.join()
print "shutting down."
