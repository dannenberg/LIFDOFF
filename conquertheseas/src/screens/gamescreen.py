import pygame
import math
from constants import *
from offense_panel import OffensePanel
from board import Board
from unit import Unit,UnitFactory
from screen import Screen
from mousehitbox import MouseHitboxes
from action import Action

class GameScreen(Screen):
    """in game screen"""
    def __init__(self):
        Screen.__init__(self)
        
        self.action_surface = None

        self.action_loc = None
        self.water_level = 0
        self.water_range=SQUARE_SIZE/4
        self.held = None
        
        self.current_action = None

        self.offense_panel = OffensePanel(OFFENSIVE_PANEL_SQUARES_X, OFFENSIVE_PANEL_SQUARES_Y)
        self.offense_panel.add_unit(UnitFactory.TADPOLE)
        self.offense_panel.add_unit(UnitFactory.YELLOW_SUB)
        
        self.enemy_board = Board(BOARD_SQUARES_X, BOARD_SQUARES_Y)
        self.my_board = Board(BOARD_SQUARES_X, BOARD_SQUARES_Y)
        
        self.action_imgs = pygame.image.load("../img/action_choices.png")
        self.arrows = pygame.image.load("../img/arrow_formatted.png")
        self.arrow_locs = []
        
        self.command = ""
        def toShop(scr, mpos):
            self.command = "transition shop"
        self.clickbox.append((660,742,122,57), toShop) # SO MAGICAL!
        
        def boardclick(scr, mpos):
            mpos = ((mpos[0])//SQUARE_SIZE, (mpos[1])//SQUARE_SIZE)
            curunit = self.enemy_board.get_cell_content(mpos)
            print "gamescreen.boardclick "+str(mpos)
            if isinstance(self.held, Unit):
                if mpos not in self.movement_locs:
                    self.held = None
                    self.current_action = None
                    self.movement_locs = []
                else:   # show where he would like to go
                    self.held.queue_movements(x[:2] for x in self.arrow_locs)
                    print self.held._actions
                    self.held = None
                    self.current_action = None
                    self.movement_locs = []
            if curunit != None: # clicked on a unit: do as he wants
                options = curunit.get_abilities()
                if len(options) == 0: # no actions dont select
                    pass
                elif len(options) == 1: # do only action
                    ui_action(options[0], curunit)
                else:
                    self.action_surface = pygame.Surface((45*len(options),45))
                    for i,o in enumerate(options):
                        self.action_surface.blit(self.action_imgs, (45*i,0), ((45*Action.img_lookup[o],0), (45,45)))
                    def action_click(scr, mpos):
                        self.current_action = self.held.get_abilities()[mpos[0]//45]
                    self.clickbox.append((300,0,45*len(options),45), action_click)
                    self.action_loc = (mpos[0]*SQUARE_SIZE, mpos[1]*SQUARE_SIZE, 0)
            else:               # clicked on nothing
                if self.held != None:   # looking to place
                    if not isinstance(self.held, Unit):
                        print "gamescreen.boardclick: add-pole!"
                        if not self.enemy_board.add_unit(UnitFactory(self.held, mpos)):
                            print "gamescreen.boardclick: can't drop here!"
                            return
                        self.held = None
                        self.current_action = None
                        self.offense_panel.selected = None
        self.clickbox.append((ENEMY_BOARD_X, ENEMY_BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), boardclick)
        
        def action_button(scr, mpos):
            self.held = None
            self.current_action = None
            self.movement_locs = []
            self.enemy_board.take_turn()
        
        def ui_action(token, curunit):
            if token == Action.MOVE:
                movespd = 3 # TODO: Not constant
                self.movement_locs = set((x+z[0], y+z[1]) for z in curunit.get_cells() for y in xrange(-movespd,movespd+1) for x in xrange(-movespd+abs(y), movespd-abs(y)+1))
                self.held = curunit
                self.cur_action = Action.MOVE
            elif token == Action.SHOOT:
                pass
                
            
        def offense_panel_click(scr, mpos):
            mpos = (mpos[0]//PANEL_SQUARE_SIZE, mpos[1]//PANEL_SQUARE_SIZE)  
            self.movement_locs = []
            self.held = self.offense_panel.on_click(mpos) 
        
        self.clickbox.append((OFFENSIVE_PANEL_X, OFFENSIVE_PANEL_Y, OFFENSIVE_PANEL_WIDTH, OFFENSIVE_PANEL_HEIGHT), offense_panel_click)
        
        self.clickbox.append((1, 740, 207, 60), action_button)
        
        self.movement_locs = []
        self.mouseover_highlight = []
        self.highlit_board = 0
        self.highlight = pygame.Surface((SQUARE_SIZE-2, SQUARE_SIZE-2)) # the size of your rect
        self.highlight.set_alpha(128) # alpha level
        self.highlight.fill(COLORS["highlight"]) # this fills the entire surface
        
        self.highlight_panel_square = None
        self.highlight_panel = pygame.Surface((PANEL_SQUARE_SIZE-2, PANEL_SQUARE_SIZE-2)) # the size of your rect
        self.highlight_panel.set_alpha(128) # alpha level
        self.highlight_panel.fill(COLORS["highlight"]) # this fills the entire surface
        
        mmbutton = pygame.image.load("../img/mainmenu.png")
        ubutton  = pygame.image.load("../img/upgrades.png")
        sbutton  = pygame.image.load("../img/shop.png")
        abutton  = pygame.image.load("../img/action.png")
        
        self.button_bar = pygame.Surface((1280, 60))
        self.button_bar.fill(COLORS["bg"])
        cblit = self.size[0] + BUTTON_OFFSET
        for x in (mmbutton, ubutton, sbutton):
            cblit -= x.get_size()[0] + BUTTON_OFFSET
            self.button_bar.blit(x, (cblit, 0))
        self.button_bar.blit(abutton, (0, 0))
        
        self.board_sans_buttons = pygame.Surface((1280, 742))
        
        self.gridlines = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)   # per - pixel alpha
        for x in xrange(0, BOARD_WIDTH, SQUARE_SIZE):
            pygame.draw.line(self.gridlines, COLORS["gridline"], (x, 0), (x, BOARD_HEIGHT), 2)   # v gridline
            pygame.draw.line(self.gridlines, COLORS["gridline"], (0, x), (BOARD_WIDTH, x), 2)  # h gridline
            
        def limit_by_multiple(x,y,s):
            return ((x-y)//s)*s+y
        
        def mouseout(scr):
            scr.mouseover_highlight = []
            scr.highlight_panel_square = None
        
        # offensive panel mouse over
        def hold(scr, mpos):
            scr.highlight_panel_square = (limit_by_multiple(mpos[0],0,PANEL_SQUARE_SIZE)+2,limit_by_multiple(mpos[1],0,PANEL_SQUARE_SIZE)+2)
        self.overbox.append((OFFENSIVE_PANEL_X, OFFENSIVE_PANEL_Y, OFFENSIVE_PANEL_WIDTH, OFFENSIVE_PANEL_HEIGHT),hold,mouseout)
        
        # enemy board mouse over
        def mouseover(player):
            def reverse(num):
                if num < 3:
                    return num*4
                return num//4
            def hold(scr, mpos):
                whichboard = self.my_board if player else self.enemy_board
                curunit = whichboard.get_cell_content((mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE))
                if not self.held:
                    if not curunit: # no unit mouseover'd
                        scr.mouseover_highlight = [(mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE)]
                    else:
                        scr.mouseover_highlight = curunit.get_cells()
                elif isinstance(self.held,Unit):
                    to_check = self.arrow_locs[-1][:2] if len(self.arrow_locs) else self.held._loc
                    if (mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE) != to_check:
                        self.arrow_locs.append((mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE, 1))
                            
                    """ HIDEOUS CHUNK OF BAD ARROW DRAWING
                    if self.current_action == Action.MOVE:
                        mpos = (mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE)
                        movespd = 3
                        
                        lastloc = self.arrow_locs[-1] if len(self.arrow_locs)>0 else self.held._loc
                        if lastloc[:2] == mpos:
                            return
                        if len(self.arrow_locs) >= movespd:
                            scr.arrow_locs = []
                            xran,yran = (abs(mpos[i]-self.held._loc[i]) for i in xrange(2))
                            xdir,ydir = (1 if mpos[i]-self.held._loc[i]>0 else -1 for i in xrange(2))
                            for x in xrange(1,xran):  # xdir
                                scr.arrow_locs += [(self.held._loc[0]+x*xdir, self.held._loc[1], 10)]
                            if xran and yran:   # turn
                                val = 0
                                val |= 4 if ydir>0 else 1
                                val |= 8 if xdir>0 else 2
                                scr.arrow_locs += [(mpos[0],self.held._loc[1],val)]
                            for y in xrange(1,yran):  # ydir
                                scr.arrow_locs += [(mpos[0],self.held._loc[1]+y*ydir,5)]
                            scr.arrow_locs += [(mpos[0], mpos[1], (1 if ydir>0 else 4) if yran else (8 if xdir>0 else 2))]  # bellend
                        else:
                            xran,yran = (abs(mpos[i]-lastloc[i]) for i in xrange(2))
                            xdir,ydir = (1 if mpos[i]-lastloc[i]>0 else -1 for i in xrange(2))
                            direction = (1 if ydir>0 else 4) if yran else (8 if xdir>0 else 2)
                            if len(scr.arrow_locs)>0:
                                if self.arrow_locs[-1][2] == reverse(direction):
                                    del self.arrow_locs[-1]
                                    self.arrow_locs[-1] = self.arrow_locs[-1][:2]+(self.arrow_locs[-1][2]&~direction,)
                                    return
                                self.arrow_locs[-1] = self.arrow_locs[-1][:2]+(self.arrow_locs[-1][2]|reverse(direction),)
                            self.arrow_locs += [(mpos[0],mpos[1],direction)]
                            print len(self.arrow_locs)
                        
                        """
                    scr.mouseover_highlight = [(loc[0]+mpos[0]//SQUARE_SIZE,loc[1]+mpos[1]//SQUARE_SIZE) for loc in self.held.get_shape()]
                else:
                    scr.mouseover_highlight = [(loc[0]+mpos[0]//SQUARE_SIZE,loc[1]+mpos[1]//SQUARE_SIZE) for loc in UnitFactory.get_shape_from_token(self.held)]
                scr.highlit_board = player
            return hold
        self.overbox.append((ENEMY_BOARD_X,ENEMY_BOARD_Y,BOARD_WIDTH,BOARD_HEIGHT),mouseover(0),mouseout)
        self.overbox.append((MY_BOARD_X, MY_BOARD_Y,BOARD_WIDTH,BOARD_HEIGHT),mouseover(1),mouseout)
    
    def display(self, screen):
        Screen.display(self, screen)
        self.board_sans_buttons.fill(COLORS["bg"])
        
        pygame.draw.rect(self.my_board.surface, COLORS["sky"], (0, 0, BOARD_WIDTH, BOARD_HEIGHT))
        pygame.draw.rect(self.enemy_board.surface, COLORS["sky"], (0, 0, BOARD_WIDTH, BOARD_HEIGHT))
        
        self.water_level = (self.water_level + (math.pi/180))%(math.pi * 2)
        modifier = int(SQUARE_SIZE * 2.5 + math.sin(self.water_level) * self.water_range)
        pygame.draw.rect(self.enemy_board.surface, COLORS["water"], (0, modifier, BOARD_WIDTH, BOARD_HEIGHT - modifier))
        pygame.draw.rect(self.my_board.surface, COLORS["water"], (0, modifier, BOARD_WIDTH, BOARD_HEIGHT - modifier))
        
        self.my_board.draw_board()
        self.enemy_board.draw_board()
        self.offense_panel.draw_panel()
        
        for x in self.movement_locs:
            self.enemy_board.surface.blit(self.highlight, (x[0]*SQUARE_SIZE+2, x[1]*SQUARE_SIZE+2))
        
        for x in self.arrow_locs:
            self.enemy_board.surface.blit(self.arrows, (x[0]*SQUARE_SIZE+2, x[1]*SQUARE_SIZE+2), ((SQUARE_SIZE*x[2],0),(SQUARE_SIZE,SQUARE_SIZE)))
        
                
        # panel highlight
        if self.highlight_panel_square != None:
            self.offense_panel.surface.blit(self.highlight_panel, self.highlight_panel_square)

        # board highlight
        curboard = self.my_board.surface if self.highlit_board else self.enemy_board.surface
        for loc in self.mouseover_highlight:
            curboard.blit(self.highlight, (loc[0]*SQUARE_SIZE+2,loc[1]*SQUARE_SIZE+2))
        
        #grid lines
        self.enemy_board.surface.blit(self.gridlines, (0, 0))
        self.my_board.surface.blit(self.gridlines, (0, 0))

        # action menu if needed
        if self.action_loc:
            if self.action_loc[2]:
                self.board_sans_buttons.blit(self.action_surface, (300, 0))
            else: 
                self.board_sans_buttons.blit(self.action_surface, (300, 0))

        self.board_sans_buttons.blit(self.enemy_board.surface, (ENEMY_BOARD_X, ENEMY_BOARD_Y))
        self.board_sans_buttons.blit(self.my_board.surface, (MY_BOARD_X, MY_BOARD_Y))
        self.board_sans_buttons.blit(self.offense_panel.surface, (OFFENSIVE_PANEL_X, OFFENSIVE_PANEL_Y))
        
        # Game Borders vvv
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], ( 201,  60), ( 201, 730), 2)  # side line
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (   0,  60), (1250,  60), 2)  # top line
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], ( 201, 390), (1250, 390), 2)  # center line t
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (1250, 390), (1250,  60), 2)  # right line t
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (   0, 395), ( 201, 395), 2)  # center line c
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], ( 201, 400), (1250, 400), 2)  # center line b
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (1250, 730), (1250, 400), 2)  # right line b
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (   0, 730), (1280, 730), 2)  # bottom line
        
        screen.blit(self.board_sans_buttons, (0, 0))
        screen.blit(self.button_bar, (0, 740))
        
        hold = self.command
        self.command = ""
        return hold

