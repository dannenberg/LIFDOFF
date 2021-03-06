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
        #print "effects.apply_effect: defensiveUnit has an effect", self
        if self.etype in (Effect.TANGLED, Effect.AERODYNAMIC):
            if self.default is None:
                self.default = unit._move_speed
                a = self.amount
                if self.etype == Effect.AERODYNAMIC:
                    a *= -1
                    #print "movespeed is ", self.default-a
                unit._move_speed = self.default-a
            if self.left == 0:
                unit._move_speed = self.default
                unit.effects.remove(self)
            elif self.left > 0:  # else intrinsic
                self.left -= 1
        elif self.etype == Effect.LUCKY:
            pass    # lollerskates

    def __str__(self):
        return "Effect: type:"+str(self.etype)+", turns remaining:"+str(self.left)
