# Encapsulated ######
class MainClass:
    special_value = 'this is special value'


class ChildA(MainClass):
    pass


class ChildB(MainClass):
    pass

# Encapsulated ######

# Tuk imam povtorenie na tozi method i v dvata klasa koeto e problem
# I zatova tuk primerno moga da polzvam Mixins za da se spravq s tozi problem
class ModifiedA(ChildA):
    def print_value(self):
        print(self.special_value)


class ModifiedB(ChildB):
    def print_value(self):
        print(self.special_value)



class Mixin():
    def print_value(self):
        print(self.special_value)

# Taka sega dvata modela kato nasledqt Mixin taka i dvata klasa imat tazi funcionalnost print_value
class SuperModifiedA(Mixin, ChildA):
    pass


class SuperModifiedB(Mixin, ChildB):
    pass



sma = SuperModifiedA()
smb = SuperModifiedB()
sma.print_value()
smb.print_value()