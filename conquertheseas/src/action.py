class Action:
    """ An action that a unit can take: usually moving or shooting """
    MOVE = 1
    SHOOT = 2
    CREATE = 3
    SPECIAL = 4
    UNDO = 5
    img_lookup = {MOVE:0, SHOOT:1, SPECIAL:2, UNDO:3}
    def __init__(self, action, loc=None, extra=None):
        self.action = action
        self.loc = loc
        self.extra = extra

    def __str__(self):
        if self.action == Action.MOVE:
            return "MOVE "+str(self.loc[0])+" "+str(self.loc[1])
        elif self.action == Action.SHOOT:
            return "SHOOT"
        elif self.action == Action.SPECIAL:
            return "SPECIAL "+str(self.loc[0])+" "+str(self.loc[1])
