from struct import unpack
import time
running = 1
f = open('/dev/input/mice', 'rb')
while running:
        c = f.read(1)
        b2 = f.read(1)
        b3 = f.read(1)
        n = ord(c)
        n2 = ord(b2)  # from char to int
        n3 = ord(b3)
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
        if rightbutton > 0:
                print "RIGHTBUTTON"

        if n2 > 128:
                n2 = n2 - 255
        if n3 > 128:
                n3 = n3 - 255
        print "X" , n2
        print "Y" , n3
        print button_state
        if left > 0:
                print "LEFT"
        else:
                print "RIGHT"

        if down > 0:
                print "DOWN"
        else:
                print "UP"
        time.sleep(.5)

