import pygame
import math
import heapq
from constants import *
from offense_panel import OffensePanel
from board import Board
from unit import Unit, UnitFactory
from screen import Screen
from action import Action

from screens.shopscreen import ShopScreen   # :(


def fxrange(start, end=None, inc=None):
    """Why can't python do this. Come on."""
    start = float(start)
    if end is None:
        end = start
        start = 0.0
    if inc is None:
        inc = 1.0
    count = int((end-start)/inc)
    if start+count*inc != end:
        count += 1
    for i in xrange(count):
        yield start+i*inc


class GameScreen(Screen):
    """in game screen"""
    NO_MODE = 0
    DEPLOYING = 1
    ACTION_MENU = 2
    MOVING = 3
    GAMEOVER = 4
    WAITING = 5
    PAUSE_MENU = 6

    def __init__(self, main, num_players=2, local=True):
        Screen.__init__(self, main)

        if isinstance(num_players, int):
            boards = None
        else:
            boards = num_players
            num_players = len(num_players)
        self.num_players = num_players
        self.people_done = 0
        self.local = local
        self.enemy_board_index = 0

        self.to_server = []

        self.tabs = pygame.Surface((1280-201, 60), pygame.SRCALPHA)
        self.sin_cache = [math.sin(i) for i in fxrange(0, math.pi, math.pi/180)]
        self.font = pygame.font.Font(None, 40)
        self.mode = GameScreen.NO_MODE
        self.action_surface = None
        self.last_turn = False
        self.victoryimg = None
        self.pause_img = pygame.image.load("../img/pause_menu.png")

        self.action_loc = None
        self.water_level = 0
        self.water_range = SQUARE_SIZE/4
        self.held = None

        self.offense_panel = OffensePanel(OFFENSIVE_PANEL_SQUARES_X, OFFENSIVE_PANEL_SQUARES_Y)
        self.offense_panel.add_unit(UnitFactory.TADPOLE)
        self.local_opanel = OffensePanel(OFFENSIVE_PANEL_SQUARES_X, OFFENSIVE_PANEL_SQUARES_Y)
        self.local_opanel.add_unit(UnitFactory.TADPOLE)
        self.local_shop = ShopScreen(self.main)

        self.create_boards(num_players, boards)

        self.waiting_img = pygame.image.load("../img/wait_overlay.png")
        self.action_imgs = pygame.image.load("../img/action_choices.png")
        self.arrows = pygame.image.load("../img/arrow_formatted.png")
        self.arrow_locs = Arrows((0, 0), 0)
        self.arrow_offset = (0, 0)

        def to_shop(mpos):
            self.main.change_screen("shop")
        self.clickbox.append((660, 742, 122, 57), to_shop)  # SO MAGICAL!

        def to_upgrade(mpos):
            self.main.change_screen("upgrade")
        self.clickbox.append((785, 742, 230, 57), to_upgrade)  # SO MAGICAL!

        def to_mainmenu(mpos):
            self.set_mode(GameScreen.PAUSE_MENU)
            self.clickbox.append((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), lambda mpos: None, z=13)  # blocking
            self.overbox.append((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), lambda mpos: None, z=14)  # blocking

            def return_to_game(mpos):
                self.set_mode(GameScreen.NO_MODE)

            def to_savescreen(mpos):
                self.set_mode(GameScreen.NO_MODE)
                self.main.change_screen("saveload")
                self.main.screens["saveload"].redraw_save_load(True)
                self.main.screens["saveload"].return_to = "game"

            def quit_game(mpos):
                # TODO: multiplayer "that's it i'm out"
                self.main.change_screen("main")

            self.clickbox.append((440, 250, 393, 60), return_to_game, z=14)    # return to game
            self.clickbox.append((440, 323, 393, 60), to_savescreen, z=14)    # save game
            self.clickbox.append((440, 396, 393, 60), quit_game, z=14)    # quit game

        self.clickbox.append((1020, 742, 260, 57), to_mainmenu)    # TOOOO MAGICAL!

        def enemy_boardclick(mpos):
            gpos = (BOARD_SQUARES_X - 1 - mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE)
            # curunit = self.enemy_board.get_cell_content(gpos)  # grab the unit @ this pos
            #print "gamescreen.enemy_boardclick (gpos)"+str(gpos)

            if self.mode == GameScreen.DEPLOYING:
                #if not isinstance(self.held, Unit):
                #print "gamescreen.boardclick: add-pole!"
                if BOARD_SQUARES_X-OFFENSIVE_PLACEMENT_DEPTH > gpos[0] or not self.enemy_board.add_unit(UnitFactory(self.held, gpos)):
                    #print "gamescreen.boardclick: can't drop here!"
                    return
                self.add_to_server_list("SENT", self.enemy_board_index, self.held, *gpos)
                if pygame.K_LSHIFT not in self.main.keys:
                    self.set_mode(GameScreen.NO_MODE)

        def my_boardclick(mpos):
            gpos = (mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE)
            curunit = self.held
            clicked_unit = self.my_board.get_cell_content(gpos)   # grab the unit @ this pos
            if curunit is None:
                curunit = clicked_unit
            elif curunit == clicked_unit:
                self.set_mode(GameScreen.NO_MODE)
                curunit = None
            elif self.mode != GameScreen.MOVING:
                self.set_mode(GameScreen.NO_MODE)
                curunit = clicked_unit

            #print "gamescreen.my_boardclick (gpos) "+str(gpos)

            self.held = curunit
            if self.mode == GameScreen.MOVING:
                if gpos in self.movement_locs:
                    self.held.queue_movements(x[:2] for x in self.arrow_locs)   # queue his movements based on the arrows
                    self.my_board.move_unit(self.held, self.arrow_locs.get_loc())
                    #print "gamescreen.my_boardclick (the gentleman's actions) "+str(self.held._actions)
                    self.set_mode(GameScreen.NO_MODE)

            elif curunit is not None:  # clicked on a unit: do as he wants
                if curunit._class == Unit.DEFENSE:  # TODO make a action menu creator for action mode!
                    options = curunit.get_abilities()  # get his possible actions
                    self.set_mode(GameScreen.ACTION_MENU)
                    self.action_surface = pygame.Surface((ACTION_BUTTON_SIZE*len(options), ACTION_BUTTON_SIZE))
                    for i, o in enumerate(options):
                        self.action_surface.blit(self.action_imgs, (ACTION_BUTTON_SIZE*i, 0), ((ACTION_BUTTON_SIZE*Action.img_lookup[o], 0), (ACTION_BUTTON_SIZE, ACTION_BUTTON_SIZE)))

                    def action_click(mpos):
                        ui_action(options[mpos[0]//ACTION_BUTTON_SIZE], curunit)  # show the ui for that action

                    try:  # oh good jesus the math
                        self.action_loc = (min(gpos[0]*SQUARE_SIZE, (BOARD_SQUARES_X - (ACTION_BUTTON_SIZE*len(options)/SQUARE_SIZE + 1))*SQUARE_SIZE), min(gpos[1]*SQUARE_SIZE, (BOARD_SQUARES_Y - 2) * SQUARE_SIZE))
                        self.clickbox.append((self.action_loc[0] + MY_BOARD_X, self.action_loc[1] + MY_BOARD_Y, ACTION_BUTTON_SIZE*len(options), ACTION_BUTTON_SIZE), action_click, z=2)
                        #self.clickbox.append((300, 0, ACTION_BUTTON_SIZE*len(options), ACTION_BUTTON_SIZE), action_click)
                        #self.action_loc = (gpos[0]*SQUARE_SIZE, gpos[1]*SQUARE_SIZE, 0)
                    except AttributeError:
                        print "TODO: avoid double placing this hitbox"

        self.clickbox.append((ENEMY_BOARD_X, ENEMY_BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), enemy_boardclick)
        self.clickbox.append((MY_BOARD_X, MY_BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), my_boardclick)

        def action_button(mpos):
            if self.local:
                self.set_mode(GameScreen.NO_MODE)
                self.enemy_board.remove_staging()
                for unit in self.my_board.units:
                    self.my_board.move_unit(unit, unit._unaltered_loc)

                self.generate_ai_turns()
                self.my_board.remove_staging()
                for unit in self.enemy_board.units:
                    self.enemy_board.move_unit(unit, unit._unaltered_loc)
                self.enemy_board.take_turn(self.main.rand)
                self.my_board.take_turn(self.main.rand)
                self.enemy_board.initialize_turn(self.main.rand)
                self.my_board.initialize_turn(self.main.rand)
                self.handle_gameover()

            else:
                # send everything to server
                # server does take_turn
                # sends results back
                left = True
                while left:
                    #print "gamescreen.action_button: LEFT", left
                    left = 0
                    for u in self.my_board.units:
                        #print "gamescreen.action_button:", u._actions
                        if u._actions:
                            #print "gamescreen.action_button: push to server:", str(u._actions[0])
                            self.add_to_server_list(u._actions[0], u.idd)
                            del u._actions[0]
                            left += 1
                    if left:
                        #print "gamescreen.action_button: TURN"
                        self.add_to_server_list("TURN")
                self.add_to_server_list("END")
                #print self.to_server
                self.set_mode(GameScreen.WAITING)
                self.clickbox.append((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), lambda x: None, z=17)
                for msg in self.to_server:
                    self.main.client.send(msg)
                self.enemy_board.clear_staging()
                for unit in self.my_board.units:
                    self.my_board.move_unit(unit, unit._unaltered_loc)
                self.to_server = []

        self.clickbox.append((1, 740, 207, 60), action_button)  # TODO SO MAGICAL

        def ui_action(token, curunit):
            if token == Action.MOVE:
                movespd = curunit.moves_remaining
                self.movement_locs = set((x+z[0], y+z[1]) for z in curunit.get_cells() for y in xrange(-movespd, movespd+1) for x in xrange(-movespd+abs(y), movespd-abs(y)+1))
                self.arrow_offset = (int(((curunit._size[0]-1)/2.0)*SQUARE_SIZE), int(((curunit._size[1]-1)/2.0)*SQUARE_SIZE))
                self.set_mode(GameScreen.MOVING)
                self.held = curunit
                self.arrow_locs = Arrows(self.held._loc, self.held.moves_remaining)
                #print "gamescreen.ui_action: Created a new arrows of length", self.held._move_speed
            elif token == Action.SHOOT:
                curunit.queue_shoot()
                self.set_mode(GameScreen.NO_MODE)
            elif token == Action.UNDO:
                curunit.reset_moves(self.my_board)
                self.set_mode(GameScreen.NO_MODE)
            else:
                raise AttributeError("Unrecognized token "+str(token))

        def offense_panel_click(mpos):
            if self.mode != GameScreen.DEPLOYING:
                self.set_mode(GameScreen.DEPLOYING)
            gpos = (mpos[0]//PANEL_SQUARE_SIZE, mpos[1]//PANEL_SQUARE_SIZE)
            self.held = self.offense_panel.on_click(gpos)
            if self.held is None:
                self.set_mode(GameScreen.NO_MODE)

        self.clickbox.append((OFFENSIVE_PANEL_X, OFFENSIVE_PANEL_Y, OFFENSIVE_PANEL_WIDTH, OFFENSIVE_PANEL_HEIGHT), offense_panel_click)

        self.movement_locs = []
        self.mouseover_highlight = []
        self.highlit_board = 0
        self.highlight = pygame.Surface((SQUARE_SIZE-2, SQUARE_SIZE-2))  # the size of your rect
        self.highlight.set_alpha(128)  # alpha level
        self.highlight.fill(COLORS["highlight"])  # this fills the entire surface

        self.highlight_panel_square = None
        self.highlight_panel = pygame.Surface((PANEL_SQUARE_SIZE-2, PANEL_SQUARE_SIZE-2))  # the size of your rect
        self.highlight_panel.set_alpha(128)  # alpha level
        self.highlight_panel.fill(COLORS["highlight"])  # this fills the entire surface

        self.water_tint = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
        self.water_tint.fill(COLORS["water"])
        self.water_tint.set_alpha(64)

        mmbutton = pygame.image.load("../img/mainmenu.png")
        ubutton = pygame.image.load("../img/upgrades.png")
        sbutton = pygame.image.load("../img/shop.png")
        abutton = pygame.image.load("../img/action.png")

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

        def limit_by_multiple(x, y, s):
            return ((x-y)//s)*s+y

        def mouseout():
            self.mouseover_highlight = []
            self.highlight_panel_square = None

        # offensive panel mouse over
        def hold(mpos):
            self.highlight_panel_square = (limit_by_multiple(mpos[0], 0, PANEL_SQUARE_SIZE)+2, limit_by_multiple(mpos[1], 0, PANEL_SQUARE_SIZE)+2)
        self.overbox.append((OFFENSIVE_PANEL_X, OFFENSIVE_PANEL_Y, OFFENSIVE_PANEL_WIDTH, OFFENSIVE_PANEL_HEIGHT), hold, mouseout)

        # enemy board mouse over
        def mouseover(player):
            def reverse(num):
                if num < 3:
                    return num*4
                return num//4

            def hold(mpos):
                if self.mode == GameScreen.ACTION_MENU:
                    return
                if player:
                    whichboard = self.my_board
                    gpos = (mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE)
                else:
                    whichboard = self.enemy_board
                    gpos = (BOARD_SQUARES_X - 1-mpos[0]//SQUARE_SIZE, mpos[1]//SQUARE_SIZE)
                curunit = whichboard.get_cell_content(gpos)
                if not self.held:
                    if not curunit:  # no unit mouseover'd
                        self.mouseover_highlight = [gpos]
                    else:
                        self.mouseover_highlight = curunit.get_cells()
                elif isinstance(self.held, Unit):
                    """
                    if gpos in self.movement_locs:
                        to_check = self.arrow_locs[-1][:2] if len(self.arrow_locs) else self.held._loc  # go from the last arrow drawn. if no last arrow drawn, go from unit
                        if gpos != to_check:    # don't draw over an arrow you've already placed
                            self.arrow_locs.append((gpos[0], gpos[1], 1))
                    """

                    if self.mode == GameScreen.MOVING and player == 1:
                        gpos = ((mpos[0]-self.arrow_offset[0])//SQUARE_SIZE, (mpos[1]-self.arrow_offset[1])//SQUARE_SIZE)
                        self.arrow_locs.update_arrows(*gpos)

                    self.mouseover_highlight = [(loc[0]+gpos[0], loc[1]+gpos[1]) for loc in self.held.get_shape()]
                else:
                    self.mouseover_highlight = [(loc[0]+gpos[0], loc[1]+gpos[1]) for loc in UnitFactory.get_shape_from_token(self.held)]
                self.highlit_board = player
            return hold
        self.overbox.append((ENEMY_BOARD_X, ENEMY_BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), mouseover(0), mouseout)
        self.overbox.append((MY_BOARD_X, MY_BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), mouseover(1), mouseout)

        def on_click(ind):
            def anon(mpos):
                self.enemy_board_index = ind
                self.enemy_board = self.enemy_boards[ind]
                self.redraw_tabs()
            return anon

        if self.num_players > 2:
            off = 0
            for i, x in enumerate(self.enemy_boards):
                if x == self.my_board:
                    off = -1
                    continue

                self.clickbox.append((201+(i+off)*200, 20, 200, 40), on_click(i))
            self.redraw_tabs()

    def new_turn(self):
        """ Receiving the turns back """
        self.people_done = 0
        self.set_mode(GameScreen.NO_MODE)

    def server_unit_move(self, msg):
        x, y, dude = msg.split(" ")
        self.enemy_boards[self.people_done].defensive[int(dude)].queue_movements([(int(x), int(y))])

    def server_unit_send(self, msg):
        """ uft x y """  # TODO: what the fuck does this mean
        uft, x, y = map(int, msg.split(" "))
        if self.enemy_boards[self.people_done].cells[x][y] is None:  # not technically correct
            self.enemy_boards[self.people_done].add_unit(UnitFactory(uft, (x, y)))

    def server_unit_shoot(self, msg):
        self.enemy_boards[self.people_done].defensive[int(msg)].queue_shoot()

    def server_unit_special(self, msg):
        pass

    def server_unit_buy(self, msg):
        pass

    def server_unit_upgrade(self, msg):
        unit, upgrade_id = map(int, msg.split(" "))
        self.main.screens["upgrade"].purchased_effect(self.enemy_boards[self.people_done], unit, upgrade_id)

    def redraw_tabs(self):
        tabsize = (210, 40)
        draw = ((10, 0), (0, 10), (0, tabsize[1]), tabsize, (tabsize[0], 0))
        tabshape = pygame.Surface(tabsize, pygame.SRCALPHA)
        pygame.draw.polygon(tabshape, (0xFF, 0, 0), draw)
        pygame.draw.polygon(tabshape, (0, 0, 0), draw, 3)
        off = 0
        for i, x in enumerate(self.enemy_boards):
            if x == self.my_board:
                off = -1
                continue
            if self.enemy_board_index == i:  # yellow!
                ts = pygame.Surface(tabsize, pygame.SRCALPHA)
                pygame.draw.polygon(ts, (0xFF, 0xC0, 0), draw)
                pygame.draw.polygon(ts, (0, 0, 0), draw, 3)
                self.tabs.blit(ts,       ((tabsize[0]-10)*(i+off), 20))
            else:
                self.tabs.blit(tabshape, ((tabsize[0]-10)*(i+off), 20))
            self.tabs.blit(self.font.render(x.name, True, (0xFF, )*3), ((tabsize[0]-10)*(i+off)+10, 30))

    def generate_ai_turns(self):
        for x in xrange(3):
            for _ in xrange(3):
                r = self.main.rand.randint(0, 3)
                if r < 2:
                    dx = 0
                    dy = (r % 2)*2 - 1
                else:
                    dx = (r % 2)*2 - 1
                    dy = 0
                self.enemy_boards[1].defensive[x]._loc = (max(0, min(33, self.enemy_boards[1].defensive[x]._loc[0]+dx)), max(0, min(9, self.enemy_boards[1].defensive[x]._loc[1]+dy)))
                self.enemy_boards[1].defensive[x].queue_movements([(self.enemy_boards[1].defensive[x]._loc)])
                 #print "Please move", x
            if not self.main.rand.randint(0, 3):
                self.enemy_boards[1].defensive[x].queue_shoot()
        for _ in xrange(self.main.rand.randint(2, 5)):
            self.my_board.add_unit(UnitFactory(UnitFactory.TADPOLE, (BOARD_SQUARES_X-self.main.rand.randint(1, OFFENSIVE_PLACEMENT_DEPTH), self.main.rand.randint(0, BOARD_SQUARES_Y-1))))

    def resolve_turn(self, msg):
        """ ??? """
        self.enemy_boards[self.people_done].remove_staging()
        self.enemy_boards[self.people_done].take_turn(self.main.rand)
        self.enemy_boards[self.people_done].initialize_turn(self.main.rand)
        self.people_done += 1
        #print "people done", self.people_done
        if self.people_done == self.num_players:
            lose = all(u.dead for _, u in self.my_board.defensive.items())
            win = all(all(u.dead for _, u in b.defensive.items()) for b in self.enemy_boards if b is not self.my_board)
            if lose:
                self.main.client.send("DEAD ")
            if win or lose:
                self.clickbox.clear()
                self.overbox.clear()

                def toMenu(mpos):
                    self.main.change_screen("main")
                self.clickbox.append((544, 512, 210, 61), toMenu)  # SO MAGICAL
                self.victoryimg = pygame.image.load("../img/"+("", "defeat", "victory", "tie")[win*2 + lose]+".png")
                self.set_mode(GameScreen.GAMEOVER)
                return
            self.new_turn()

    def create_boards(self, num_players, x=None):
        if x is not None:
            if isinstance(x[0], basestring):    # names
                self.enemy_boards = [Board(BOARD_SQUARES_X, BOARD_SQUARES_Y, x[i], x[i] == self.main.player_name) for i in xrange(num_players)]
            else:   # actual boards
                self.enemy_boards = x
            my_index = [i for i, j in enumerate(x) if j == self.main.player_name][0]
            #print "my index", my_index
            self.my_board = self.enemy_boards[my_index]
            if my_index == 0:
                self.enemy_board_index = 1
            else:
                self.enemy_board_index = 0
            self.enemy_board = self.enemy_boards[self.enemy_board_index]
        else:   # start up
            names = ["AI Player "+str(j) if j else "You" for j in xrange(num_players)]
            self.enemy_boards = [Board(BOARD_SQUARES_X, BOARD_SQUARES_Y, names[i], not i) for i in xrange(num_players)]
        # NOPE
            self.enemy_board = self.enemy_boards[1]
            self.my_board = self.enemy_boards[0]

    def add_to_server_list(self, action, *args):
        """ Adds to the list of commands we send to the server """
        self.to_server.append(str(action)+" "+(" ".join([str(x) for x in args])))

    def handle_gameover(self):
        lose = all(u.dead for _, u in self.my_board.defensive.items())
        win = all(all(u.dead for _, u in b.defensive.items()) for b in self.enemy_boards if b is not self.my_board)
        if win or lose:
            self.set_mode(GameScreen.GAMEOVER)
            self.clickbox.clear()
            self.overbox.clear()

            def toMenu(mpos):
                self.main.change_screen("main")
            self.clickbox.append((544, 512, 210, 61), toMenu)  # SO MAGICAL
            self.victoryimg = pygame.image.load("../img/"+("", "defeat", "victory", "tie")[win*2 + lose]+".png")

    def set_mode(self, new_mode):
        if self.mode == GameScreen.WAITING:
            self.clickbox.clear(17)  # I bet you'd like a comment here, huh?
        if self.mode == GameScreen.DEPLOYING:
            self.offense_panel.selected = None
            self.held = None
        if self.mode == GameScreen.MOVING:
            self.held = None
            self.movement_locs = []
            self.arrow_locs = []
        if self.mode == GameScreen.ACTION_MENU:
            self.held = None
            self.clickbox.remove((self.action_loc[0]+MY_BOARD_X, self.action_loc[1]+MY_BOARD_Y))
            self.action_loc = None
        if self.mode == GameScreen.PAUSE_MENU:
            self.clickbox.clear(13)  # blocking
            self.clickbox.clear(14)  # buttons
            self.overbox.clear(14)
        self.mode = new_mode

    def display(self, screen):
        Screen.display(self, screen)
        self.board_sans_buttons.fill(COLORS["bg"])

        pygame.draw.rect(self.my_board.surface, COLORS["sky"], (0, 0, BOARD_WIDTH, BOARD_HEIGHT))
        pygame.draw.rect(self.enemy_board.surface, COLORS["sky"], (0, 0, BOARD_WIDTH, BOARD_HEIGHT))

        self.water_level = (self.water_level+1) % len(self.sin_cache)
        modifier = int(SQUARE_SIZE * .5 + self.sin_cache[self.water_level] * self.water_range)
        pygame.draw.rect(self.enemy_board.surface, COLORS["water"], (0, modifier, BOARD_WIDTH, BOARD_HEIGHT - modifier))
        pygame.draw.rect(self.my_board.surface, COLORS["water"], (0, modifier, BOARD_WIDTH, BOARD_HEIGHT - modifier))

        self.my_board.draw_board()
        self.enemy_board.draw_board()
        self.offense_panel.draw_panel()

        self.my_board.surface.blit(self.water_tint, ((0, modifier), (BOARD_WIDTH, BOARD_HEIGHT - modifier)))
        self.enemy_board.surface.blit(self.water_tint, ((0, modifier), (BOARD_WIDTH, BOARD_HEIGHT - modifier)))

        for x in self.movement_locs:
            self.my_board.surface.blit(self.highlight, (x[0]*SQUARE_SIZE+2, x[1]*SQUARE_SIZE+2))

        for x in self.arrow_locs:
            self.my_board.surface.blit(self.arrows, (x[0]*SQUARE_SIZE+2+self.arrow_offset[0], x[1]*SQUARE_SIZE+2+self.arrow_offset[1]), ((SQUARE_SIZE*(x[2] | x[3]), 0), (SQUARE_SIZE, SQUARE_SIZE)))

        if self.mode == GameScreen.DEPLOYING:
            self.enemy_board.surface.blit(pygame.transform.scale(self.highlight, (SQUARE_SIZE*OFFENSIVE_PLACEMENT_DEPTH, SQUARE_SIZE*BOARD_SQUARES_Y)), ((BOARD_SQUARES_X-OFFENSIVE_PLACEMENT_DEPTH)*SQUARE_SIZE, 0))

        # panel highlight
        if self.highlight_panel_square is not None:
            self.offense_panel.surface.blit(self.highlight_panel, self.highlight_panel_square)

        # gp/xp
        gold_text = self.font.render("Gold: "+str(self.my_board.gold), True, COLORS["white"])
        exp_text = self.font.render("EXP: "+str(self.my_board.exp), True, COLORS["white"])
        self.board_sans_buttons.blit(gold_text, (7, 408))
        self.board_sans_buttons.blit(exp_text, (7, 448))

        # board highlight
        curboard = self.my_board.surface if self.highlit_board else self.enemy_board.surface
        for loc in self.mouseover_highlight:
            curboard.blit(self.highlight, (loc[0]*SQUARE_SIZE+2, loc[1]*SQUARE_SIZE+2))

        #grid lines
        self.enemy_board.surface.blit(self.gridlines, (0, 0))
        self.my_board.surface.blit(self.gridlines, (0, 0))

        # action menu if needed
        if self.mode == GameScreen.ACTION_MENU:
            self.my_board.surface.blit(self.action_surface, self.action_loc)

        self.board_sans_buttons.blit(pygame.transform.flip(self.enemy_board.surface, True, False), (ENEMY_BOARD_X, ENEMY_BOARD_Y))
        self.board_sans_buttons.blit(self.my_board.surface, (MY_BOARD_X, MY_BOARD_Y))
        self.board_sans_buttons.blit(self.offense_panel.surface, (OFFENSIVE_PANEL_X, OFFENSIVE_PANEL_Y))

        # Game Borders vvv
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (201, 60), (201, 730), 2)  # side line
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (0, 60), (1250, 60), 2)  # top line
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (201, 390), (1250, 390), 2)  # center line t
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (1250, 390), (1250, 60), 2)  # right line t
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (0, 395), (201, 395), 2)  # center line c
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (201, 400), (1250, 400), 2)  # center line b
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (1250, 730), (1250, 400), 2)  # right line b
        pygame.draw.line(self.board_sans_buttons, COLORS["lines"], (0, 730), (1280, 730), 2)  # bottom line

        screen.blit(self.board_sans_buttons, (0, 0))
        screen.blit(self.button_bar, (0, 740))

        if self.mode == GameScreen.PAUSE_MENU:
            screen.blit(self.pause_img, (0, 0))

        if self.mode == GameScreen.WAITING:
            screen.blit(self.waiting_img, (0, 0))

        if self.mode == GameScreen.GAMEOVER:
            screen.blit(self.victoryimg, (0, 0))

        if self.num_players > 2:
            screen.blit(self.tabs, (201, 0))


class Arrows:
    def __init__(self, (x, y), movespd):
        self.movespd = movespd
        self.arrow_locs = [[x, y, 0, 0]]   # [x, y, in, out]. The list should always at least contain this entry

    def reverse(self, bit):
        if bit < 4:
            return bit*4
        return bit//4

    def get_arrow_type(self, data):
        return data[2] | data[3]

    def get_loc(self):
        return self.arrow_locs[-1][:2]

    def update_arrows(self, nx, ny):
        if(abs(nx-self.arrow_locs[0][0]) + abs(ny-self.arrow_locs[0][1]) > self.movespd):   # OOB
            return False
        cut = self.coords(self.arrow_locs)
        if [nx, ny] in cut:  # cut the start
            self.cut_arrows(cut.index([nx, ny]))
            return True
        hold = self.arrow_locs[:]

        while self.arrow_locs:
            cut = self.coords(self.arrow_locs)
            paths = {}
            seen = set([tuple(x[:2]) for x in self.arrow_locs])
            x = tuple(self.arrow_locs[-1][:2])
            pq = [(self.heuristic(x, self.arrow_locs), x)]
            while pq:
                x = heapq.heappop(pq)[1]
                seen.add(x)
                if x == (nx, ny):    # reconstruct (you've made it)
                    nextpath = []
                    while x != tuple(cut[-1]):
                        nextpath = [tuple(x[:])]+nextpath
                        x = paths[x]
                    self.arrow_locs += self.direct_arrows(nextpath, self.arrow_locs[-1])
                    return True
                for y in self.get_adj(x, seen):
                    if y not in pq:  # ???
                        h = self.heuristic(y, self.arrow_locs)
                        if h <= self.movespd:
                            heapq.heappush(pq, (h, y))
                            paths[y] = x
            self.cut_arrows()   # cut the tail
        self.arrow_locs = hold
        return False    # found no path

    def direct_arrows(self, arrowlist, last):
        toR = []
        for x in arrowlist:
            back = 8 if last[0] < x[0] else (2 if last[0] > x[0] else (1 if last[1] < x[1] else 4))   # get the direction
            toR += [list(x)+[back, 0]]
            last[3] = self.reverse(back)
            last = toR[-1]
        return toR

    def cut_arrows(self, index=None):
        """ Cut the arrow-snake at index. If no index is given, cut off the last arrow """
        if index is None:   # cut the last one
            index = len(self.arrow_locs)-2
        self.arrow_locs[index][3] = 0   # make the last arrow a point
        self.arrow_locs = self.arrow_locs[:index+1]       # slice

    def get_adj(self, (x, y), arrows):
        """ Get the locations adjacent to (x, y), as long as they don't intersect
        any existing arrows """
        cut = self.coords(arrows)
        return (z for z in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)) if z not in cut)

    def heuristic(self, (x, y), arrows):
        ex, ey = arrows[-1][:2]
        return abs(ex-x)+abs(ey-y)+len(arrows)-1    # h+g

    def coords(self, arrows):
        """ Get the arrows without direction information """
        return [a[:2] for a in arrows]

    def __iter__(self):  # iterater skips the first (always (0, 0))
        return self.arrow_locs[1:].__iter__()
