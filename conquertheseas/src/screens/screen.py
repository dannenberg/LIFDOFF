from constants import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
from mousehitbox import MouseHitboxes


class Screen(object):
    """Screen initializes colors, mouse over/clicked events,
    and the display for launch
    nominally abstract"""

    def __init__(self, main):
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.scale = 1
        self.main = main
        self.clickbox = MouseHitboxes()
        self.overbox = MouseHitboxes()

    def display(self, screen):
        """takes a screen draws screen state to screen"""
        screen.fill(COLORS["bg"])

    def abs_scale(self, size):
        self.scale = size

    def on_switch_in(self):
        """when this screen is switched to, do this"""
        pass

    def click(self, mpos):
        """handles click events"""
        mpos = (int(mpos[0]/self.scale), int(mpos[1]/self.scale))
        result = self.clickbox[mpos]
        if result is not None:
            result["on"]((mpos[0] - result["left"], mpos[1] - result["top"]))
        else:
            print "screen.click: "+str(mpos)+": No item found"

    def over(self, mpos):
        """handles mouseover events"""
        mpos = (int(mpos[0]/self.scale), int(mpos[1]/self.scale))
        self.overbox.out(mpos)()
        result = self.overbox[mpos]
        if result is not None:
            result["on"]((mpos[0] - result["left"], mpos[1] - result["top"]))

    def notify_key(self, key):
        pass    # implementation is subclass-specific
