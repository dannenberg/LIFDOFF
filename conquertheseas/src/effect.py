import copy
class Effect:   # like mass effect amirite
    TANGLED = 1
    DOUBLESHOT = 2
    AERODYNAMIC = 3
    LUCKY = 4
    GOLD = 5
    ARMORED = 6
    def __init__(self, etype, left, amount=0, **args):
        self.etype = etype
        self.left = left
        self.amount = amount
        self.default = None
        self.__dict__.update(args)
    
    def clone(self):
        return copy.deepcopy(self)
    
    def apply_effect(self, unit):
        print "effects.apply_effect: defensiveUnit has an effect", self
        if self.etype in (TANGLED, AERODYNAMIC):
            if self.default is None:
                self.default = unit._move_speed
                a = self.amount
                if self.etype == AERODYNAMIC:
                    a *= -1
                unit._move_speed = self.default-self.amount
            if self.left == 0:
                unit._move_speed = self.default
                unit.effects.remove(effect)
                print "effects.apply_effect: removing bad effect"
            elif self.left > 0: # else intrinsic
                self.left -= 1
        elif self.etype == LUCKY:
            pass    # lollerskates
    
    def __str__(self):
        return "Effect: type:"+str(self.etype)+", turns remaining:"+str(self.left)
