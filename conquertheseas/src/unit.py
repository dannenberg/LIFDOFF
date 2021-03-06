import pygame
from effect import Effect
from action import Action
from constants import SQUARE_SIZE
from animation import Animation


class UnitFactory(object):
    MINE = 1
    CRAB = 2
    SQUIDDLE = 3
    MERMAID = 4
    BULLET = 5
    TADPOLE = 6
    ANGRYFISH = 7
    TERRAIN1 = 17
    TERRAIN2 = 18
    GOLD = 19
    PURPLE_SUB = 20
    YELLOW_SUB = 21
    unitsize = {TADPOLE: (1, 1), MINE: (2, 2), CRAB: (1, 1), SQUIDDLE: (1, 1), MERMAID: (2, 1), BULLET: (1, 1), ANGRYFISH: (1, 1), TERRAIN1: (1, 1), TERRAIN2: (1, 2), GOLD: (1, 1), PURPLE_SUB: (2, 2), YELLOW_SUB: (2, 2)}
    cash_val = {TADPOLE: 5, MINE: 5, CRAB: 5, SQUIDDLE: 5, MERMAID: 10, BULLET: 0, ANGRYFISH: 10, TERRAIN1: 0, TERRAIN2: 0, GOLD: 10, PURPLE_SUB: 0, YELLOW_SUB: 0}
    exp_val = {TADPOLE: 5, MINE: 5, CRAB: 5, SQUIDDLE: 5, MERMAID: 5, BULLET: 0, ANGRYFISH: 5, TERRAIN1: 0, TERRAIN2: 0, GOLD: 0, PURPLE_SUB: 0, YELLOW_SUB: 0}
    move_spd = {TADPOLE: 3, MINE: 1, CRAB: 3, SQUIDDLE: 1, MERMAID: 1, BULLET: 3, ANGRYFISH: 3, TERRAIN1: 1, TERRAIN2: 1, GOLD: 1, PURPLE_SUB: 5, YELLOW_SUB: 5}
    damage = {SQUIDDLE: 0}
    animations = {TADPOLE: Animation("idle", idle=[(1, 50, (0, 0)), (2, 50, (2, 0)), (3, 50, (0, 0)), (0, 50, (1, 0))]),
                  MINE: Animation("idle"),
                  CRAB: Animation("idle"),
                  SQUIDDLE: Animation("idle", idle=[(1, 50, (0, 0)), (2, 50, (1, 0)), (3, 50, (2, 0)), (4, 50, (3, 0)), (5, 50, (4, 0)), (0, 50, (2, 0))]),
                  MERMAID: Animation("idle", idle=[(1, 50, (0, 0)), (0, 50, (1, 0))]),
                  BULLET: Animation("idle"),
                  ANGRYFISH: Animation("idle"),
                  TERRAIN1: Animation("idle"),
                  TERRAIN2: Animation("idle"),
                  GOLD: Animation("idle", idle=[(1, 50, (0, 0)), (2, 50, (1, 0)), (3, 50, (2, 0)), (4, 50, (3, 0)), (5, 50, (4, 0)), (6, 50, (3, 0)), (7, 50, (2, 0)), (0, 50, (1, 0))]),
                  PURPLE_SUB: Animation("idle", idle=[(1, 50, (0, 0)), (2, 50, (1, 0)), (3, 50, (0, 0)), (0, 50, (2, 0))]),
                  YELLOW_SUB: Animation("idle", idle=[(1, 50, (0, 0)), (2, 50, (1, 0)), (3, 50, (0, 0)), (0, 50, (2, 0))])}
    effects = {SQUIDDLE: [Effect(Effect.TANGLED, left=3, amount=3)]}
    img = {
        TADPOLE: "../img/tadpole.png",
        MINE: "../img/mine.png",
        CRAB: "../img/crab.png",
        SQUIDDLE: "../img/squiddle.png",
        MERMAID: "../img/mermaid.png",
        BULLET: "../img/bullet.png",
        ANGRYFISH: "../img/angryfish.png",
        TERRAIN1: "../img/terrain1.png",
        TERRAIN2: "../img/terrain2.png",
        GOLD: "../img/gold.png",
        PURPLE_SUB: "../img/purple_sub.png",
        YELLOW_SUB: "../img/yellow_sub.png",
    }

    def __new__(_, idd, loc, fo_real=False):
        utype = Unit.OFFENSE if fo_real else Unit.STAGING
        utoken = None if fo_real else idd
        if idd == UnitFactory.TADPOLE:
            return Unit(idd, loc, utype, token=utoken)
        if idd == UnitFactory.MINE:
            return Unit(idd, loc, utype, token=utoken)
        if idd == UnitFactory.CRAB:
            return Unit(idd, loc, utype, token=utoken)
        if idd == UnitFactory.SQUIDDLE:
            return Unit(idd, loc, utype, token=utoken)
        if idd == UnitFactory.MERMAID:
            return Unit(idd, loc, utype, token=utoken)
        if idd == UnitFactory.ANGRYFISH:
            return Unit(idd, loc, utype, token=utoken)
        if idd == UnitFactory.BULLET:
            return Unit(idd, loc, Unit.BULLET)
        if idd == UnitFactory.TERRAIN1:
            return Unit(idd, loc, Unit.TERRAIN)
        if idd == UnitFactory.TERRAIN2:
            return Unit(idd, loc, Unit.TERRAIN)
        if idd == UnitFactory.GOLD:
            return Unit(idd, loc, Unit.GOLD)
        raise ValueError("Unknown unit id "+str(idd))

    @staticmethod
    def get_shape_from_token(idd):  # returns the size of the unit (0, 0), (0, 1), (1, 0), (1, 1) for a 2x2 unit
        return [(x, y) for x in xrange(UnitFactory.unitsize[idd][0]) for y in xrange(UnitFactory.unitsize[idd][1])]


class Unit(object):
    DEFENSE = 1
    OFFENSE = 2
    BULLET = 3
    TERRAIN = 4
    GOLD = 5
    STAGING = 0

    def __init__(self, idd, (x, y), cls, parent=None, token=None):
        if parent is not None:
            self._class = parent._class
            self._parent = parent
        else:
            self._parent = None
            self._class = cls
        self.idd = idd
        self._tileset = pygame.image.load(UnitFactory.img[idd])
        self._token = token
        self._spr_src = (0, 0)     # topleft of source tile
        self._size = UnitFactory.unitsize[idd]
        self._spr_size = (self._size[0]*SQUARE_SIZE, self._size[1]*SQUARE_SIZE)  # width and height in pixels
        self._loc = (x, y)           # location on the board
        self._unaltered_loc = (x, y)
        self._actions = []
        self.exp_value = UnitFactory.exp_val[idd]
        self.cash_value = UnitFactory.cash_val[idd]
        self._move_speed = UnitFactory.move_spd[idd]
        self.animation = UnitFactory.animations[idd].clone()
        self.effects = []
        if idd in UnitFactory.effects:
            self.effects = [e.clone() for e in UnitFactory.effects[idd]]
        self.damage = 5
        if idd in UnitFactory.damage:
            self.damage = UnitFactory.damage[idd]
        self.moves_remaining = self._move_speed
        self.health = 1
        self.level = 0
        self.moved = False

    def __getstate__(self):
        # !!!! CRITICALLY IMPORTANT !!!!
        # If we need to change the order or contents of the items in this function,
        # or the accompanying __setstate__, or really any sort of save/load helper
        # function, increment the VERSION number in constants.py
        return {k: v for k, v in self.__dict__.items() if k != '_tileset'}
        #return [self._w, self._h, self.cells, self.units, self._actions, self.exp, self.gold]

    def __setstate__(self, data):
        # !!!! CRITICALLY IMPORTANT !!!!
        # See above
        self.__dict__.update(data)
        self._tileset = pygame.image.load(UnitFactory.img[self.idd])

    def add_effect(self, effect):
        self.effects.append(effect.clone())
        effect.apply_effect(self)
        if effect.etype == Effect.ARMORED:
            self.level |= 4
        if effect.etype == Effect.DOUBLESHOT:
            self.level |= 2
        if effect.etype == Effect.AERODYNAMIC:
            self.level |= 1

    def has_effect(self, effect):
        return effect in [e.etype for e in self.effects]

    def advance_sprite(self):
        temp = self.animation.advance_sprite(50)   # TODO: 50 is a terrible guess
        self._spr_src = (temp[0]*self._spr_size[0], self.level*self._spr_size[1])

    def draw_sprite(self, destsurface, loc=None):
        self.advance_sprite()
        if loc is not None:  # for drawing an addon using relative position
            loc = tuple(map(sum, zip(self._loc, loc)))  # sum the tuples
        else:
            loc = self._loc
        destsurface.blit(self._tileset, [z*SQUARE_SIZE for z in loc], (self._spr_src, self._spr_size))

    def update_position(self, pos=None):
        self._loc = pos
        # TODO collisions

    def get_coord(self):
        if self._parent:
            return tuple(map(sum, zip(self._loc, self._parent.get_coord())))
        return self._loc

    def get_cells(self):
        coord = self.get_coord()
        return [(coord[0]+x, coord[1]+y) for x in xrange(self._size[0]) for y in xrange(self._size[1])]

    def get_shape(self):
        return [(x, y) for x in xrange(self._size[0]) for y in xrange(self._size[1])]

    def queue_movements(self, dests):
        for d in dests:
            self.moves_remaining -= 1
            self._actions.append(Action(Action.MOVE, d))

    def queue_shoot(self):
        self.moves_remaining -= 1
        self._actions.append(Action(Action.SHOOT))

    def reset_moves(self, board):
        board.move_unit(self, self._unaltered_loc)
        self.moves_remaining = self._move_speed
        self._loc = self._unaltered_loc
        self._actions = []

    def take_damage(self, board, dmg=None):
        """Deal damage to the unit and return its remaining health."""
        if dmg is None or self.health-dmg <= 0:
            board.gold += self.cash_value
            board.exp += self.exp_value
            board.remove_unit(self)  # D:
            if self._class == Unit.DEFENSE:
                board.defensive[self.idd].dead = True
            self.health = 0
        else:
            self.health -= dmg
        return self.health

    def on_collision(self, opposed, board):
        """Return damage done to opponent."""
        # do lots of checks for what two things are hitting and act appropriately
        sSelf, sOpposed = sorted([self, opposed], key=lambda x: x._class)
        if sSelf._class == Unit.DEFENSE:
            if sOpposed._class == Unit.GOLD:
                sOpposed.take_damage(board)
                board.gold += 5
            elif sOpposed._class == Unit.TERRAIN:
                #print "unit is hitting terrain...die"
                sSelf.take_damage(board)
            elif sOpposed._class == Unit.BULLET:
                sOpposed.take_damage(board)
            elif sOpposed._class == Unit.OFFENSE:
                #print sSelf.effects
                armor = filter(lambda x: Effect.ARMORED == x.etype, sSelf.effects)
                if armor:
                    sSelf.effects.remove(armor[0])
                    sSelf.level &= ~4
                else:
                    sSelf.take_damage(board, sOpposed.damage)
                sOpposed.take_damage(board, sSelf.damage)
                sSelf.effects += [effect.clone() for effect in sOpposed.effects]
        elif sSelf._class == Unit.OFFENSE:
            if sOpposed._class == Unit.TERRAIN:
                sSelf.take_damage(board)
            elif sOpposed._class == Unit.BULLET:
                sSelf.take_damage(board)
            elif sOpposed._class == Unit.GOLD:
                return False
        elif sSelf._class == Unit.BULLET:
            if sOpposed._class == Unit.GOLD:
                sOpposed.take_damage(board)
            elif sOpposed._class == Unit.TERRAIN:
                sSelf.take_damage(board)
        elif sSelf._class == Unit.TERRAIN:
            if sOpposed._class == Unit.GOLD:
                sOpposed.take_damage(board)
        return True

    def create_move(self, rand):
        if self._class == Unit.BULLET:
            for i in xrange(self._move_speed):
                self._actions.append(Action(Action.MOVE, (self._loc[0] + i + 1, self._loc[1])))
        elif self._class == Unit.OFFENSE:
            if self.idd == UnitFactory.SQUIDDLE:    # squiddle move AI
                for i in xrange(self._move_speed):
                    self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, self._loc[1])))
                    randval = rand.randint(-1, 1)
                    #print "SQUIDDLE", randval
                    self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, max(0, min(10, randval+self._loc[1])))))
            elif self.idd == UnitFactory.MINE:      # mine move AI
                for i in xrange(self._move_speed):
                    self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, self._loc[1])))
                    randval = rand.randint(0, 1)
                    #print "MINE", randval
                    self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1,  min(9, randval+self._loc[1]))))
            else:
                for i in xrange(self._move_speed):
                    self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, self._loc[1])))
        elif self._class == Unit.TERRAIN:
            for i in xrange(self._move_speed):
                self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, self._loc[1])))
        elif self._class == Unit.GOLD:
            for i in xrange(self._move_speed):
                self._actions.append(Action(Action.MOVE, (self._loc[0] - i - 1, self._loc[1])))
