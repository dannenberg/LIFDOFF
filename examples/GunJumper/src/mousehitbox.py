import unittest

class MouseHitboxes:
    def __init__(self):
        self._data = []
        self._last = None   # the index of the last element you saw; used for mouseout
        
    def append(self, rect, on, off=lambda x:None):
        k = {"left":rect[0], "top":rect[1], "width":rect[2], "height":rect[3], "right":rect[0] + rect[2], "bottom":rect[1] + rect[3], "on":on, "off":off}
        for x in self._data:
            if  (x["left"] <= k["left"] < x["right"] or x["left"] < k["right"] <= x["right"] or k["left"] <= x["left"] < k["right"] or k["left"] < x["right"] <= k["right"])\
            and (x["top"] <= k["top"] < x["bottom"] or x["top"] < k["bottom"] <= x["bottom"] or k["top"] <= x["top"] < k["bottom"] or k["top"] < x["bottom"] <= k["bottom"]):
                raise AttributeError("You have overlapping hitboxes! "+str(x))
        self._data.append(k)
        
    def out(self, key):
        if self._last != None:
            x = self._data[self._last]
            if not (x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]):
                return x["off"]
        return lambda x:None
        
    def remove(self, key):
        """ Remove the hitbox at coordinates specified. Does not 'out'."""
        x = self._index(key)
        if x == None:
            raise IndexError("No hitbox to remove at this point.")
        del self._data[x]
        if self._last == x:
            self._last = None
        if self._last > x:
            self._last -= 1
        
    def _index(self, key):
        if self._last != None:  # this SHOULD improve performance with many elements. if it turns out it doesn't, you can remove this block
            x = self._data[self._last]
            if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                return self._last
        for i, x in enumerate(self._data):
            if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                self._last = i
                return i
        self._last = None   # did not find a box
        return None
        
    def __getitem__(self, key):
        x = self._index(key)
        if x == None:
            return None
        return self._data[x]
        
    def clear(self):
        self._data = []
        self._last = None
        
    def __repr__(self):
        toR = []
        for x in self._data:
            toR.append("Left:%d, Top:%d, Right:%d, Bottom:%d"%(x["left"], x["top"], x["right"], x["bottom"]))
        return '\n'.join(toR)
        
class TestMouseHitboxes(unittest.TestCase):
    def setUp(self):
        self.mh = MouseHitboxes()
        self.function = lambda x:None
    
    #     +----+
    #  +--+--+ |
    #  |  |  | |
    #  +--+--+ |
    #     +----+
    def test_half_inside(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 1, 2, 2), self.function)
            self.mh.append((1, 0, 2, 4), self.function)
    
    #   +---+
    #   |   |
    # +-+-+ |
    # | | | |
    # | +-+-+ 
    # |   |
    # +---+
    def test_one_corner(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 1, 2, 2), self.function)
            self.mh.append((1, 0, 2, 2), self.function)
    
    # opposite of previous
    def test_different_corner(self):
        with self.assertRaises(AttributeError):
            self.mh.append((1, 0, 2, 2), self.function)
            self.mh.append((0, 1, 2, 2), self.function)
    
    # +--------------+
    # |  +--------+  |
    # |  |        |  |
    # |  +--------+  |
    # +--------------+
    def test_one_in_other(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 0, 3, 3), self.function)
            self.mh.append((1, 1, 1, 1), self.function)
    
    #    +--+
    #    |  |
    # +--+--+--+
    # |  |  |  |
    # +--+--+--+
    #    |  |
    #    +--+
    def test_cross(self):
        with self.assertRaises(AttributeError):
            self.mh.append((1, 0, 1, 3), self.function)
            self.mh.append((0, 1, 3, 1), self.function)
    
    # opposite of previous
    def test_other_cross(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 1, 3, 1), self.function)
            self.mh.append((1, 0, 1, 3), self.function)
    
    def test_separate1(self):
        self.mh.append((0, 0, 2, 2), self.function)
        self.mh.append((2, 2, 1, 3), self.function)
        self.assertTrue(True)
    
    def test_separate2(self):
        self.mh.append((0, 0, 2, 2), self.function)
        self.mh.append((0, 2, 1, 3), self.function)
        self.assertTrue(True)
    
    def test_separate3(self):
        self.mh.append((0, 0, 2, 2), self.function)
        self.mh.append((2, 0, 1, 3), self.function)
        self.assertTrue(True)
    
    def test_separate4(self):
        self.mh.append((2, 2, 1, 3), self.function)
        self.mh.append((0, 0, 2, 2), self.function)
        self.assertTrue(True)
    
    def test_separate5(self):
        self.mh.append((0, 2, 1, 3), self.function)
        self.mh.append((0, 0, 2, 2), self.function)
        self.assertTrue(True)
    
    def test_separate6(self):
        self.mh.append((2, 0, 1, 3), self.function)
        self.mh.append((0, 0, 2, 2), self.function)
        self.assertTrue(True)
    
if __name__ == "__main__":
    unittest.main()
