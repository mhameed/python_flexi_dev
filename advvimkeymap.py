from plumbum.cmd import xte, spd_say
from jsdriver import Driver
from ring import Ring
say = spd_say['-r', '100', '-P', 'important']

class VimKeymap(Driver):
    def __init__(self,*args, **kwargs):
        super(VimKeymap, self).__init__(*args, **kwargs)
        self.navType = Ring(['line', 'word', 'char'])
        self.layoutType = Ring(['arrow', 'orca', 'vim'])
        self.lastNavKey = ['key Down']

    def js_btn0(self,value):
        """ shooting trigger, repeat last navigation command. """
        #if value:
        xte[tuple(self.lastNavKey)]()

    def js_btn1(self,value):
        """ Bottom middle button. """
        if not value:  return
        k = []
        nt = self.navType
        lt = self.layoutType

        if lt == 'arrow' and nt == 'line': k = ['key Down'] 
        if lt == 'arrow' and nt == 'word': k = ['keydown Control_L', 'key Right', 'keyup Control_L']
        if lt == 'arrow' and nt == 'char': k = ['key Right'] 

        if lt == 'vim' and nt == 'line': k = ['key j'] 
        if lt == 'vim' and nt == 'word': k = ['key w']                 
        if lt == 'vim' and nt == 'char': k = ['key l']                 

        if lt == 'orca' and nt == 'line': k = ['key KP_9'] 
        if lt == 'orca' and nt == 'word': k = ['key KP_6']                 
        if lt == 'orca' and nt == 'char': k = ['key KP_3']                 

        self.lastNavKey = k
        xte[tuple(k)]()

    def js_btn2(self, value):
        """ bottom left button. """
        if not value:  return
        k = []
        nt = self.navType
        lt = self.layoutType

        if lt == 'arrow' and nt == 'line': k = ['key Up'] 
        if lt == 'arrow' and nt == 'word': k = ['keydown Control_L', 'key Left', 'keyup Control_L']
        if lt == 'arrow' and nt == 'char': k = ['key Left'] 

        if lt == 'vim' and nt == 'line': k = ['key k'] 
        if lt == 'vim' and nt == 'word': k = ['key b']                 
        if lt == 'vim' and nt == 'char': k = ['key h']                 

        if lt == 'orca' and nt == 'line': k = ['key KP_7'] 
        if lt == 'orca' and nt == 'word': k = ['key KP_4']                 
        if lt == 'orca' and nt == 'char': k = ['key KP_1']                 

        self.lastNavKey = k
        xte[tuple(k)]()

    def js_btn3(self,value):
        """ bottom right, enter."""
        if value:
            xte['key Return']()

    def js_btn4(self,value):
        """ top left corner, q """
        if value: 
            xte['key q']()

    def js_btn5(self,value):
        """ top right corner, toggle quickNav """
        if value: 
           xte['key t']() 

    def js_axis3(self,value):
        """ top right corner, toggle quickNav """
        if value>0: 
            self.layoutType.next()
            say[self.layoutType.__str__()]()
        elif  value<0: 
            self.layoutType.prev()
            say[self.layoutType.__str__()]()

    def js_axis4(self,value):
        """ top right corner, toggle quickNav """
        if value>0: 
            self.navType.next()
            say[self.navType.__str__()]()
        elif  value<0: 
            self.navType.prev()
            say[self.navType.__str__()]()
