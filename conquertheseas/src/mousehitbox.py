import unittest

class MouseHitboxes:
    def __init__(self):
        self._data = []
        self._last = None   # the index of the last element you saw; used for mouseout
        
    def append(self, rect, on, off=lambda x:None, z=0):
        k = {"left":rect[0], "top":rect[1], "width":rect[2], "height":rect[3], "right":rect[0] + rect[2], "bottom":rect[1] + rect[3], "on":on, "off":off, "z":z}
        i = 0
        for i,x in enumerate(self._data):
            if x["z"] == k["z"] and (x["left"] < k["right"] and x["right"] > k["left"] and x["top"] < k["bottom"] and x["bottom"] > k["top"]):
                raise AttributeError("You have overlapping hitboxes! "+str(x))
            if x["z"] < k["z"]:
                i-=1
                break
        i+=1
        self._data = self._data[:i]+[k]+self._data[i:]
        if self._last>=i:
            self._last += 1
        
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
        i=0
        if self._last != None:  # this SHOULD improve performance with many elements. if it turns out it doesn't, you can remove this block
            last = self._data[self._last]
            for i, x in enumerate(self._data):
                if x["z"] <= last["z"]: # the < should never come into play, but just to be safe
                    break
                if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                    self._last = i
                    return i
            # _last gets priority over all in the z-class
            if last["left"]<=key[0]<last["right"] and last["top"]<=key[1]<last["bottom"]:
                return self._last
        for j, x in enumerate(self._data[i:]):
            if x["left"]<=key[0]<x["right"] and x["top"]<=key[1]<x["bottom"]:
                self._last = i+j
                return i+j
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
        
    def function(self, value):
        return lambda x:value
    
    def test_one_is_other(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0,0,5,5), self.function(0))
            self.mh.append((0,0,5,5), self.function(1))
    
    def test_one_is_other_layered(self):
        self.mh.append((0,0,5,5), self.function(0))
        self.mh.append((0,0,5,5), self.function(1), z=4)
        self.assertEquals(self.mh[(1,1)]["on"]("doesnt matter what i put here"), 1)
    
    def test_one_is_other_layered_opposite(self):
        self.mh.append((0,0,5,5), self.function(0), z=9)
        self.mh.append((0,0,5,5), self.function(1), z=4)
        self.assertEquals(self.mh[(1,1)]["on"]("doesnt matter what i put here"), 0)
    
    #     +----+
    #  +--+--+ |
    #  |  |  | |
    #  +--+--+ |
    #     +----+
    def test_half_inside(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 1, 2, 2), self.function(0))
            self.mh.append((1, 0, 2, 4), self.function(1))

    def test_half_inside_same_layer(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 1, 2, 2), self.function(0), z=3)
            self.mh.append((1, 0, 2, 4), self.function(1), z=3)
    
    def test_half_inside_layered(self):
        self.mh.append((0, 2, 4, 4), self.function(0), z=0)
        self.mh.append((2, 0, 4, 8), self.function(1), z=2)
        self.assertEquals(self.mh[(0,3)]["on"]("doesnt matter what i put here"), 0)
        self.assertEquals(self.mh[(3,5)]["on"]("doesnt matter what i put here"), 1)
        self.assertEquals(self.mh[(3,3)]["on"]("doesnt matter what i put here"), 1)
        self.assertEquals(self.mh[(3,7)]["on"]("doesnt matter what i put here"), 1)
    
    def test_half_inside_layered_opposite(self):
        self.mh.append((0, 2, 4, 4), self.function(0), z=2)
        self.mh.append((2, 0, 4, 8), self.function(1), z=0)
        self.assertEquals(self.mh[(0,3)]["on"]("doesnt matter what i put here"), 0)
        self.assertEquals(self.mh[(3,5)]["on"]("doesnt matter what i put here"), 0)
        self.assertEquals(self.mh[(3,3)]["on"]("doesnt matter what i put here"), 0)
        self.assertEquals(self.mh[(3,7)]["on"]("doesnt matter what i put here"), 1)
    
    #   +---+
    #   |   |
    # +-+-+ |
    # | | | |
    # | +-+-+ 
    # |   |
    # +---+
    def test_one_corner(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 1, 2, 2), self.function(0))
            self.mh.append((1, 0, 2, 2), self.function(1))
    
    # opposite of previous
    def test_different_corner(self):
        with self.assertRaises(AttributeError):
            self.mh.append((1, 0, 2, 2), self.function(0))
            self.mh.append((0, 1, 2, 2), self.function(1))
    
    # +--------------+
    # |  +--------+  |
    # |  |        |  |
    # |  +--------+  |
    # +--------------+
    def test_one_in_other(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 0, 3, 3), self.function(0))
            self.mh.append((1, 1, 1, 1), self.function(1))
    
    # +--------------+
    # |  +--------+  |
    # |  | []     |  |
    # |  |        |  |
    # |  |    []  |  |
    # |  +--------+  |
    # +--------------+
    def test_many_layers(self):
        self.mh.append((0, 0, 12, 12), self.function(0), z=0)
        self.mh.append((2, 2, 8, 8), self.function(1), z=1)
        self.mh.append((4, 4, 2, 2), self.function(2), z=2)
        self.mh.append((6, 6, 2, 2), self.function(3), z=2)
        self.assertEquals(self.mh[(1,1)]["on"]("doesnt matter what i put here"), 0)
        self.assertEquals(self.mh[(3,3)]["on"]("doesnt matter what i put here"), 1)
        self.assertEquals(self.mh[(5,5)]["on"]("doesnt matter what i put here"), 2)
        self.assertEquals(self.mh[(7,7)]["on"]("doesnt matter what i put here"), 3)
    
    # cant diagram this due to lack of three space but think one 
    # then another on top but only slightly, with another on top of that
    # haning over the first and beyond the first
    def test_overhang(self):
        self.mh.append((6, 0, 12, 12), self.function(0), z=0)
        self.mh.append((0, 0, 12, 12), self.function(1), z=1)
        self.mh.append((4, 4, 28, 28), self.function(2), z=2)
        self.assertEquals(self.mh[(1,1)]["on"]("doesnt matter what i put here"), 1)
        self.assertEquals(self.mh[(15,1)]["on"]("doesnt matter what i put here"), 0)
        self.assertEquals(self.mh[(30,30)]["on"]("doesnt matter what i put here"), 2)
        self.assertEquals(self.mh[(16,5)]["on"]("doesnt matter what i put here"), 2)

    #    +--+
    #    |  |
    # +--+--+--+
    # |  |  |  |
    # +--+--+--+
    #    |  |
    #    +--+
    def test_cross(self):
        with self.assertRaises(AttributeError):
            self.mh.append((1, 0, 1, 3), self.function(0))
            self.mh.append((0, 1, 3, 1), self.function(1))
    
    # opposite of previous
    def test_other_cross(self):
        with self.assertRaises(AttributeError):
            self.mh.append((0, 1, 3, 1), self.function(0))
            self.mh.append((1, 0, 1, 3), self.function(1))
    
    def test_separate1(self):
        self.mh.append((0, 0, 2, 2), self.function(0))
        self.mh.append((2, 2, 1, 3), self.function(1))
        self.assertTrue(True)
    
    def test_separate2(self):
        self.mh.append((0, 0, 2, 2), self.function(0))
        self.mh.append((0, 2, 1, 3), self.function(1))
        self.assertTrue(True)
    
    def test_separate3(self):
        self.mh.append((0, 0, 2, 2), self.function(0))
        self.mh.append((2, 0, 1, 3), self.function(1))
        self.assertTrue(True)
    
    def test_separate4(self):
        self.mh.append((2, 2, 1, 3), self.function(0))
        self.mh.append((0, 0, 2, 2), self.function(1))
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
