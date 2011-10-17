import types
import unittest

class Screen:
    def __init__(self, init, display):
        self.screen = (1280, 800)
        self.init = types.MethodType(init, self)
        self.display = types.MethodType(display, self)
        self.clickbox = MouseHitboxes()
        self.overbox = MouseHitboxes()
        self.init()
    
    def click(self,mpos):
        result = self.clickbox[mpos]
        if result != None:
            result["func"](self, (mpos[0]-result["left"],mpos[1]-result["top"]))
    
    def over(self,mpos):
        result = self.overbox[mpos]
        if result != None:
            result["func"](self, (mpos[0]-result["left"],mpos[1]-result["top"]))

class MouseHitboxes:
    def __init__(self):
        self._data = []
        self._last = None
        
    def append(self, rect, func):
        k = {"left":rect[0],"top":rect[1],"width":rect[2],"height":rect[3],"right":rect[0]+rect[2],"bottom":rect[1]+rect[3],"func":func}
        for x in self._data:
            if  (x["left"] <= k["left"] < x["right"] or x["left"] < k["right"] <= x["right"] or k["left"] <= x["left"] < k["right"] or k["left"] < x["right"] <= k["right"])\
            and (x["top"] <= k["top"] < x["bottom"] or x["top"] < k["bottom"] <= x["bottom"] or k["top"] <= x["top"] < k["bottom"] or k["top"] < x["bottom"] <= k["bottom"]):
                raise AttributeError("You have overlapping hitboxes!")
        self._data.append(k)
        
    def __getitem__(self, key):
        if self._last != None:  # this SHOULD improve performance with many elements. if it turns out it doesn't, you can remove this block
            x = self._data[self._last]
            if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                return x
        for i,x in enumerate(self._data):
            if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                self._last = i
                return x
        self._last = None
        return None
        
    def clear(self):
        self._data = []
        
    def __repr__(self):
        toR = []
        for x in self._data:
            toR.append("Left:%d, Top:%d, Right:%d, Bottom:%d"%(x["left"],x["top"],x["right"],x["bottom"]))
        return '\n'.join(toR)
        
class TestMouseHitboxes(unittest.TestCase):
    def setUp(self):
        self.mh = MouseHitboxes()
    
    #     +----+
    #  +--+--+ |
    #  |  |  | |
    #  +--+--+ |
    #     +----+
    def test_half_inside(self):
        self.mh.append((0,1,2,2))
        self.assertRaises(AttributeError, self.mh.append((1,0,2,4)))
    
    #   +---+
    #   |   |
    # +-+-+ |
    # | | | |
    # | +-+-+
    # |   |
    # +---+
    def test_one_corner(self):
        self.mh.append((0,1,2,2))
        self.assertRaises(AttributeError, self.mh.append((1,0,2,2)))
    
    # opposite of previous
    def test_different_corner(self):
        self.mh.append((1,0,2,2))
        self.assertRaises(AttributeError, self.mh.append((0,1,2,2)))
    
    # +--------------+
    # |  +--------+  |
    # |  |        |  |
    # |  +--------+  |
    # +--------------+
    def test_one_in_other(self):
        self.mh.append((0,0,3,3))
        self.assertRaises(AttributeError, self.mh.append((1,1,1,1)))
    
    #    +--+
    #    |  |
    # +--+--+--+
    # |  |  |  |
    # +--+--+--+
    #    |  |
    #    +--+
    def test_cross(self):
        self.mh.append((1,0,1,3))
        self.assertRaises(AttributeError, self.mh.append((0,1,3,1)))
    
    # opposite of previous
    def test_other_cross(self):
        self.mh.append((0,1,3,1))
        self.assertRaises(AttributeError, self.mh.append((1,0,1,3)))
    
    def test_separate1(self):
        self.mh.append((0,0,2,2))
        self.mh.append((2,2,1,3))
    
    def test_separate2(self):
        self.mh.append((0,0,2,2))
        self.mh.append((0,2,1,3))
    
    def test_separate3(self):
        self.mh.append((0,0,2,2))
        self.mh.append((2,0,1,3))
    
    def test_separate4(self):
        self.mh.append((2,2,1,3))
        self.mh.append((0,0,2,2))
    
    def test_separate5(self):
        self.mh.append((0,2,1,3))
        self.mh.append((0,0,2,2))
    
    def test_separate6(self):
        self.mh.append((2,0,1,3))
        self.mh.append((0,0,2,2))
