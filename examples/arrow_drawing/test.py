import os, unittest

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
        self.arrow_locs = [[0,0,0]]
    
    def reverse(self, bit):
        if bit < 4:
            return bit*4
        return bit//4
    
    # add (nx, ny) to the arrows
    def update_arrows(self, nx, ny):
        arrow_locs = self.arrow_locs[:]
        cutme = [tuple(z[:2]) for z in arrow_locs]
        if (nx, ny) in cutme:  # doubling over, cut yourself short
            ind = cutme.index((nx, ny))+1
            arrow_locs[ind-1][2] &= ~self.reverse(arrow_locs[ind][2]) # WRONG
            arrow_locs[:] = arrow_locs[:ind]
            # and then we need to make the arrow point the right way...
            print "CUT"
            self.arrow_locs = arrow_locs
            return
        else:
            print "No of course",nx,",",ny,"wasn't in",cutme
        
        while abs(nx-arrow_locs[-1][0]) + abs(ny-arrow_locs[-1][1]) > movespd - len(arrow_locs) +1:
            if len(arrow_locs) == 1:
                return arrow_locs
            rembit = self.reverse(arrow_locs[-1][2])
            arrow_locs[:] = arrow_locs[:-1]
            arrow_locs[-1][2] &= ~rembit
        
        for x in xrange(arrow_locs[-1][0]+1,nx+1):
            arrow_locs[-1][2] |= 2
            arrow_locs.append([x,arrow_locs[-1][1],8])
        for x in xrange(arrow_locs[-1][0]-1,nx-1, -1):
            arrow_locs[-1][2] |= 8
            arrow_locs.append([x,arrow_locs[-1][1],2])
        for y in xrange(arrow_locs[-1][1]+1,ny+1):
            arrow_locs[-1][2] |= 4
            arrow_locs.append([arrow_locs[-1][0],y,1])
        for y in xrange(arrow_locs[-1][1]-1,ny-1, -1):
            arrow_locs[-1][2] |= 1
            arrow_locs.append([arrow_locs[-1][0],y,4])
        self.arrow_locs = arrow_locs
        return
        
    def __iter__(self):
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
        board[py+x[1]][px+x[0]] = _lookup[x[2]]

def main():
    arrow_locs = Arrows(movespd)
    board = []
    
    while 1:
        update_board(board, arrow_locs)
        #clear()
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

if __name__ == "__main__":
    if(raw_input(">")=="i"):
        main()
    else:
        unittest.main()
