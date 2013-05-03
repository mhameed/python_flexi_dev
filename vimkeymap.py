from plumbum.cmd import xte
from jsdriver import Driver

class VimKeymap(Driver):
    def __init__(self,*args, **kwargs):
        super(VimKeymap, self).__init__(*args, **kwargs)
        self.vimMode = 1

    def js_btn0(self,value):
        """ shooting trigger, press enter. """
        if value:
            xte['key Return']()

    def js_btn1(self,value):
        """ bottom middle, move down or press j. """
        if value: 
            if self.vimMode:
                xte['key j']()
            else:
                xte['key Down']() 

    def js_btn2(self, value):
        """ bottom left, up or j """
        if value:
            if self.vimMode:
                xte['key k']()
            else:
                xte['key Up']()

    def js_btn3(self,value):
        """ bottom right, switch between vim and non-vim modes."""
        if value:
            self.vimMode = not self.vimMode

    def js_btn4(self,value):
        """ top left corner, q """
        if value: 
            if self.vimMode:
                xte['key q']()
