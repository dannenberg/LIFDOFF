import os, unittest
import heapq

_lookup = (u"\u2592", [u"\u2193", u"\x19"][os.name=='nt'],
          [u"\u2190", u"\x1b"][os.name=='nt'], u"\u2514",
          [u"\u2191", u"\x18"][os.name=='nt'], u"\u2502",
           u"\u250C", "E", [u"\u2192", u"\x1a"][os.name=='nt'], u"\u2518",
           u"\u2500", "E", u"\u2510","E","E","E","E")
movespd = 3
W = movespd*2+1
px, py = movespd, movespd

def clear():
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

class Arrows:
    def __init__(self, movespd):
        self.movespd = movespd
        self.arrow_locs = [[0,0,0,0]]   # [x,y,in,out]. The list should always at least contain this entry
        
    def reverse(self, bit):
        if bit < 4:
            return bit*4
        return bit//4
        
    def get_arrow_type(self, data):
        return data[2]|data[3]
        
    def update_arrows(self, nx, ny):
        cut = self.coords(self.arrow_locs)
        if [nx, ny] in cut: # cut the start
            self.cut_arrows(cut.index([nx, ny]))
            return True
        hold = self.arrow_locs[:]
        
        while self.arrow_locs:
            cut = self.coords(self.arrow_locs)
            paths = {}
            seen = set([tuple(x[:2]) for x in self.arrow_locs])
            x = tuple(self.arrow_locs[-1][:2])
            pq = [(self.heuristic(x,self.arrow_locs), x)]
            while pq:
                x = heapq.heappop(pq)[1]
                seen.add(x)
                if x == (nx,ny):    # reconstruct (you've made it)
                    nextpath = []
                    while x != tuple(cut[-1]):
                        nextpath = [tuple(x[:])]+nextpath
                        x = paths[x]
                    self.arrow_locs += self.direct_arrows(nextpath, self.arrow_locs[-1])
                    return True
                for y in self.get_adj(x, seen):
                    if y not in pq: # ???
                        h = self.heuristic(y, self.arrow_locs)
                        if h<=self.movespd:
                            heapq.heappush(pq, (h, y))
                            paths[y] = x
            self.cut_arrows()   # cut the tail
        self.arrow_locs = hold
        return False    # found no path
        
    def direct_arrows(self, arrowlist, last):
        toR = []
        for x in arrowlist:
            back = 8 if last[0]<x[0] else (2 if last[0]>x[0] else (1 if last[1]<x[1] else 4))   # get the direction
            toR += [list(x)+[back,0]]
            last[3] = self.reverse(back)
            last = toR[-1]
        return toR
        
    def cut_arrows(self, index=None):
        """ Cut the arrow-snake at index. If no index is given, cut off the last arrow """
        if index is None:   # cut the last one
            index = len(self.arrow_locs)-2
        self.arrow_locs[index][3] = 0   # make the last arrow a point
        self.arrow_locs = self.arrow_locs[:index+1]       # slice
        
    def get_adj(self, (x,y), arrows):
        """ Get the locations adjacent to (x,y), as long as they don't intersect
        any existing arrows """
        cut = self.coords(arrows)
        return (z for z in ((x+1,y), (x,y+1), (x-1,y), (x,y-1)) if z not in cut)
        
    def heuristic(self, (x,y), arrows):
        ex,ey = arrows[-1][:2]
        return abs(ex-x)+abs(ey-y)+len(arrows)-1    # h+g
        
    def coords(self, arrows):
        """ Get the arrows without direction information """
        return [a[:2] for a in arrows]
        
    def __iter__(self): # iterater skips the first (always (0,0))
        return self.arrow_locs[1:].__iter__()

def print_board(board):
    toR = ""
    for y in board:
        for x in y:
            toR += x
        toR += "\n"
    print toR

# redraw the board
def update_board(board, arrow_locs):
    board[:] = [[u"\u2591" for _ in xrange(W)] for _ in xrange(W)]
    board[py][px] = "@"
    for y in xrange(-movespd, movespd+1):
        for x in xrange(-movespd+abs(y), movespd+1-abs(y)):
            if not (y==x==0):
                board[py+y][px+x] = _lookup[0]
    for x in arrow_locs:
        board[py+x[1]][px+x[0]] = _lookup[arrow_locs.get_arrow_type(x)]

def main():
    arrow_locs = Arrows(movespd)
    board = []
    
    while 1:
        update_board(board, arrow_locs)
        print_board(board)
        coord = raw_input("next coord:")
        try:
            coord = coord.split(",")
            nx, ny = int(coord[0]), int(coord[1])
        except (IndexError, ValueError):
            print "Bad input."
            continue
        arrow_locs.update_arrows(nx, ny)

class TestArrows(unittest.TestCase):
    def setUp(self):
        self.arrow = Arrows(3)
    
    def test_arrow_limit_length1(self):
        self.arrow.update_arrows(0,1)
        self.arrow.update_arrows(1,1)
        self.arrow.update_arrows(1,0)
        self.arrow.update_arrows(2,0)
        musteq = [[1,0,10],[2,0,8]]
        for i,a in enumerate(self.arrow):
            self.assertEquals(a, musteq[i])

    def test_arrow_not_move(self):
        self.arrow.update_arrows(1,0)
        self.arrow.update_arrows(1,0)
        musteq = [[1,0,8]]
        for i,a in enumerate(self.arrow):
            self.assertEquals(a, musteq[i])

    def test_arrow_double_back(self):
        self.arrow.update_arrows(1,0)
        self.arrow.update_arrows(0,1)
        musteq = [[0,1,4]]
        for i,a in enumerate(self.arrow):
            self.assertEquals(a, musteq[i])

if __name__ == "__main__":
    if(raw_input(">")=="i"):
        main()
    else:
        unittest.main()
