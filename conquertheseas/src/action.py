class Action:
    """ An action that a unit can take: usually moving or shooting """
    MOVE = 1
    SHOOT = 2
    SPECIAL = 4
    img_lookup = {MOVE:0, SHOOT:1, SPECIAL:2}
    def __init__(self, action, loc=None):
        self.action = action
        self.loc = loc
