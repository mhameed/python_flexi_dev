class Ring():
    def __init__(self, items):
        self.items = items 
        self.index = 0

    def next(self):
        if self.index < len(self.items)-1:
            self.index += 1
        else:
            self.index = 0

    def prev(self):
        if self.index == 0:
            self.index = len(self.items)-1
        else:
            self.index -= 1

    def __eq__(self, other):
        if self.items[self.index] == other.__str__(): return True
        return False

    def __str__(self):
        return self.items[self.index]

