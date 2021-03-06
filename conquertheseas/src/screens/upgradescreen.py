import pygame
import math
from constants import *
from screen import Screen
from effect import Effect


class UpgradeScreen(Screen):
    def __init__(self, main):
        Screen.__init__(self, main)
        self.tree_one = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))
        self.tree_two = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))
        self.tree_three = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))
        self.info_sfc = pygame.Surface((SCREEN_WIDTH/4, SCREEN_HEIGHT))

        self.ship = 0
        self.current_upgrade = None
        self.current_tree = None
        self.img = pygame.image.load("../img/upgrade_imgs.png")

        # TODO: refactor all of this garbage.
        self.upgrades = [
            [
                {
                    "Aerodynamic": {
                        "row": 0,
                        "order": 0,
                        "next": ["Doubleshot"],
                        "cost": 5,
                        "desc": "With a sleeker propeller your ship will be able to move much farther in a turn than normal.",
                        "effect": Effect(Effect.AERODYNAMIC, -1, 2),
                        "image": 0,
                    },
                    "Gold": {
                        "row": 0,
                        "order": 1,
                        "next": ["Doubleshot", "Armor"],
                        "cost": 5,
                        "desc": "Makes your ship slightly magnetic, increasing the amount of gold that will spawn.",
                        "effect": Effect(Effect.GOLD, -1, 1),
                        "image": 1,
                    },
                    "Luck":{
                        "row": 0,
                        "order": 2,
                        "next": ["Armor"],
                        "cost": 5,
                        "desc": "Without at least a little of this you're REALLY sunk.",
                        "effect": Effect(Effect.LUCKY, -1, 2),
                        "image": 2
                    },
                    "Doubleshot": {
                        "row": 1,
                        "order": 0,
                        "next": ["Grand Windfall"],
                        "cost": 10,
                        "desc": "What's better than mounting a giant cannon on the top of your submarine? How about mounting ANOTHER cannon on the BOTTOM of your submarine?",
                        "effect": Effect(Effect.DOUBLESHOT, -1, 2),
                        "image": 3,
                    },
                    "Armor": {
                        "row": 1,
                        "order": 1,
                        "next": ["Grand Windfall"],
                        "cost": 10,
                        "desc": "Thicker armor makes your ship harder to break: it will now be able to take an extra hit before being destroyed.",
                        "effect": Effect(Effect.ARMORED, -1, 1),
                        "image": 4,
                    },
                    "Grand Windfall": {
                        "row": 2,
                        "order": 0,
                        "next": [],
                        "cost": 500,
                        "desc": "The Ultimate Ability: a guaranteed gamechanger!",
                        "image": 5,
                    }
                },
                {
                    "Aerodynamic": {
                        "row": 1,
                        "order": 1,
                        "next": ["Powershot"],
                        "cost": 5,
                        "desc": "With a sleeker propeller your ship will be able to move much farther in a turn than normal.",
                        "effect": Effect(Effect.AERODYNAMIC, -1, 2),
                        "image": 0,
                    },
                    "Gold": {
                        "row": 1,
                        "order": 0,
                        "next": ["Grand Windfall", "Powershot"],
                        "cost": 5,
                        "desc": "Makes your ship slightly magnetic, increasing the amount of gold that will spawn.",
                        "effect": Effect(Effect.GOLD, -1, 1),
                        "image": 1,
                    },
                    "Luck":{
                        "row": 0,
                        "order": 1,
                        "next": ["Aerodynamic"],
                        "cost": 5,
                        "desc": "Without at least a little of this you're REALLY sunk.",
                        "effect": Effect(Effect.LUCKY, -1, 2),
                        "image": 2,
                    },
                    "Doubleshot":{
                        "row": 0,
                        "order": 2,
                        "next": ["Aerodynamic"],
                        "cost": 10,
                        "desc": "What's better than mounting a giant cannon on the top of your submarine? How about mounting ANOTHER cannon on the BOTTOM of your submarine?",
                        "effect": Effect(Effect.DOUBLESHOT, -1, 2),
                        "image": 3,
                    },
                    "Armor":{
                        "row": 0,
                        "order": 0,
                        "next": ["Gold"],
                        "cost": 10, "desc": "Thicker armor makes your ship harder to break: it will now be able to take an extra hit before being destroyed.",
                        "effect": Effect(Effect.ARMORED, -1, 1),
                        "image": 4,
                    },
                    "Grand Windfall": {
                        "row": 2,
                        "order": 0,
                        "next": [],
                        "cost": 500,
                        "desc": "The Ultimate Ability: a guaranteed gamechanger!",
                        "image": 5,
                    },
                    "Powershot": {
                        "row": 2,
                        "order": 1,
                        "next": [],
                        "cost": 500,
                        "desc": "A much more powerful shot: it explodes on impact!",
                        "image": 6,
                    }
                },
                {
                    "Aerodynamic": {
                        "row": 1,
                        "order": 0,
                        "next": ["Grand Windfall"],
                        "cost": 5,
                        "desc": "With a sleeker propeller your ship will be able to move much farther in a turn than normal.",
                        "effect": Effect(Effect.AERODYNAMIC, -1, 2),
                        "image": 0,
                    },
                    "Gold": {
                        "row": 0,
                        "order": 1,
                        "next": ["Aerodynamic"],
                        "cost": 5,
                        "desc": "Makes your ship slightly magnetic, increasing the amount of gold that will spawn.",
                        "effect": Effect(Effect.GOLD, -1, 1),
                        "image": 1,
                    },
                    "Luck": {
                        "row": 0,
                        "order": 0,
                        "next": ["Aerodynamic"],
                        "cost": 5,
                        "desc": "Without at least a little of this you're REALLY sunk.",
                        "effect": Effect(Effect.LUCKY, -1, 2),
                        "image": 2,
                    },
                    "Doubleshot":{
                        "row": 1,
                        "order": 1,
                        "next": ["Grand Windfall", "Tripleshot"],
                        "cost": 10,
                        "desc": "What's better than mounting a giant cannon on the top of your submarine? How about mounting ANOTHER cannon on the BOTTOM of your submarine?",
                        "effect": Effect(Effect.DOUBLESHOT, -1, 2),
                        "image": 3,
                    },
                    "Armor":{
                        "row": 0,
                        "order": 2,
                        "next": ["Doubleshot"],
                        "cost": 10,
                        "desc": "Thicker armor makes your ship harder to break:  it will now be able to take an extra hit before being destroyed.",
                        "effect": Effect(Effect.ARMORED, -1, 1),
                        "image": 4,
                    },
                    "Grand Windfall": {
                        "row": 2,
                        "order": 0,
                        "next": [],
                        "cost": 500,
                        "desc": "The Ultimate Ability: a guaranteed gamechanger!",
                        "image": 5,
                    },
                    "Tripleshot":{
                        "row": 2,
                        "order": 1,
                        "next": [],
                        "cost": 1000,
                        "desc": "How do you even intend to fit that many guns on that tiny ship? Buy it and find out!",
                        "image": 7,
                    }
                },
            ], [{}, {}, {}], [{}, {}, {}]
        ]
        self.init_upgrades()

        self.dead_unit = pygame.image.load("../img/dead_upgrade.png")
        for x in (self.tree_one, self.tree_two, self.tree_three):
            x.fill((0xCC, 0xCC, 0xFF))
        self.info_sfc.fill((0x99, 0xCC, 0xCC))

        self.font = pygame.font.Font(None, 50)
        self.font2 = pygame.font.Font(None, 40)
        self.font3 = pygame.font.Font(None, 35)

        self.redraw_right_panel(True)
        self.right_buttons()

    def purchasable(self, tree=None, upgrade=None):
        if tree is None and self.current_tree is not None:
            tree = self.current_tree
        if upgrade is None and self.current_upgrade is not None:
            upgrade = self.current_upgrade
        return self.main.screens["game"].my_board.exp >= tree[upgrade]["cost"] and all([tree[p]["purchased"] for p in tree[upgrade]["prereqs"]]) and not tree[upgrade]["purchased"]

    def init_upgrades(self):
        rows = {}
        maxrow = 0
        idd = 0
        for s, ship in enumerate(self.upgrades):
            for tree in ship:
                for upgrade in tree:  # find how many there are in each row
                    if tree[upgrade]["row"] not in rows:
                        rows[tree[upgrade]["row"]] = 0  # intentional
                    rows[tree[upgrade]["row"]] += 1
                    maxrow = max(maxrow, tree[upgrade]["row"]+1)
                    tree[upgrade]["prereqs"] = []
                    tree[upgrade]["purchased"] = False
                    tree[upgrade]["id"] = idd
                    idd += 1

                for upgrade in tree:    # actually assign them to locations
                    xspacing = (SCREEN_WIDTH/4.0)/rows[tree[upgrade]["row"]]
                    yspacing = SCREEN_HEIGHT/maxrow
                    tree[upgrade]["x"] = (tree[upgrade]["order"]+.5)*xspacing
                    tree[upgrade]["y"] = (tree[upgrade]["row"]+.5)*yspacing
                    for next in tree[upgrade]["next"]:
                        tree[next]["prereqs"].append(upgrade)
                rows = {}

    def switch_ship(self, which=None):
        if which is None:
            which = self.ship
        self.ship = which

        color = [0xCC, 0xCC, 0xCC]
        color[2-which] = 0xFF
        for x in (self.tree_one, self.tree_two, self.tree_three):
            x.fill(color)

        surfs = (self.tree_one, self.tree_two, self.tree_three)
        self.clickbox.clear(2)
        for t, tree in enumerate(self.upgrades[which]):
            for upgrade in tree:    # lines first
                for prereqs in tree[upgrade]["next"]:
                    pygame.draw.line(surfs[t], (0, 0, 0), (tree[upgrade]["x"], tree[upgrade]["y"]), (tree[prereqs]["x"], tree[prereqs]["y"]), 2)
                    q = (tree[upgrade]["x"], tree[upgrade]["y"])
                    s = (tree[prereqs]["x"]-tree[upgrade]["x"], tree[prereqs]["y"]-tree[upgrade]["y"])

                    def cross(v, w):
                        return v[0]*w[1]-v[1]*w[0]

                    pt = (0, 0)
                    lstu = 1    # we want a value less than this
                    for p, r in (((tree[prereqs]["x"]-UPGRADE_ICON_SIZE/2, tree[prereqs]["y"]-UPGRADE_ICON_SIZE/2), (0, UPGRADE_ICON_SIZE)),
                                ((tree[prereqs]["x"]+UPGRADE_ICON_SIZE/2, tree[prereqs]["y"]-UPGRADE_ICON_SIZE/2), (0, UPGRADE_ICON_SIZE)),
                                ((tree[prereqs]["x"]-UPGRADE_ICON_SIZE/2, tree[prereqs]["y"]-UPGRADE_ICON_SIZE/2), (UPGRADE_ICON_SIZE, 0)),
                                ((tree[prereqs]["x"]-UPGRADE_ICON_SIZE/2, tree[prereqs]["y"]+UPGRADE_ICON_SIZE/2), (UPGRADE_ICON_SIZE, 0))):
                        q_p = (q[0]-p[0], q[1]-p[1])
                        rxs = cross(r, s)
                        if not rxs:  # parallel lines
                            continue
                        u = float(cross(q_p, r)) / rxs
                        if u < lstu and 0 <= float(cross(q_p, s)) / rxs <= 1:  # lol @ the second part mattering
                            lstu = u
                            pt = (q[0]+u*s[0], q[1]+u*s[1])
                    # and now we have the point

                    angle = math.atan(s[0]/s[1])    # backwards
                    pygame.draw.line(surfs[t], (0, 0, 0), pt, (pt[0]-math.sin(angle+math.pi/5)*10, pt[1]-math.cos(angle+math.pi/5)*10), 2)  # arrowheads
                    pygame.draw.line(surfs[t], (0, 0, 0), pt, (pt[0]-math.sin(angle-math.pi/5)*10, pt[1]-math.cos(angle-math.pi/5)*10), 2)

            for upgrade in tree:
                rectloc = (tree[upgrade]["x"]-UPGRADE_ICON_SIZE/2, tree[upgrade]["y"]-UPGRADE_ICON_SIZE/2, UPGRADE_ICON_SIZE, UPGRADE_ICON_SIZE)
                color = (COLORS["upg_unav"], COLORS["upg_av"], COLORS["upg_purc"])[max(self.purchasable(tree, upgrade), tree[upgrade]["purchased"]*2)]
                pygame.draw.rect(surfs[t], color, rectloc)
                surfs[t].blit(self.img, rectloc, ((UPGRADE_ICON_SIZE*tree[upgrade]["image"], 0), (UPGRADE_ICON_SIZE, UPGRADE_ICON_SIZE)))
                pygame.draw.rect(surfs[t], (0xFF if tree == self.current_tree and upgrade == self.current_upgrade else 0, 0, 0), rectloc, 2)

                def what(t, tree, upgrade):
                    def onclick(mpos):
                        self.current_upgrade = upgrade
                        self.current_tree = tree

                        self.redraw_right_panel()
                        self.switch_ship()

                        def buy(mpos):
                            if self.purchasable(tree, upgrade):
                                self.purchased_effect(self.main.screens["game"].my_board, t, tree[upgrade]["id"])
                                self.main.screens["game"].my_board.exp -= tree[upgrade]["cost"]
                                #self.main.screens["game"].to_server.append("UPGRADE " + str(tree[upgrade]["id"]))
                                tree[upgrade]["purchased"] = True
                                self.redraw_right_panel()
                                # text = self.font3.render("Purchase", True, COLORS["gray"])
                                self.switch_ship(which)  # redraw the upgrades
                                self.main.screens["game"].add_to_server_list("UPGRADE", t, tree[upgrade]["id"])

                                #pygame.draw.rect(self.info_sfc, (0xC0, 0xC0, 0xC0), (UPGRADE_PURCHASE_INDENT, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10, SCREEN_WIDTH/4-2*UPGRADE_PURCHASE_INDENT, SHOP_PURCH_H))
                                #pygame.draw.rect(self.info_sfc, COLORS["black"], (UPGRADE_PURCHASE_INDENT, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10, SCREEN_WIDTH/4-2*UPGRADE_PURCHASE_INDENT, SHOP_PURCH_H), 2)
                                #self.info_sfc.blit(text, (UPGRADE_PURCHASE_INDENT+70, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10+7))
                                #self.redraw_right_panel()
                        #self.words.blit(text, (SHOP_PURCH_X+7, SHOP_PURCH_Y+5))
                        try:
                            self.clickbox.remove((UPGRADE_PURCHASE_INDENT+SCREEN_WIDTH*3/4, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10))
                        except IndexError:
                            pass
                        self.clickbox.append((UPGRADE_PURCHASE_INDENT+SCREEN_WIDTH*3/4, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10, SCREEN_WIDTH/4-2*UPGRADE_PURCHASE_INDENT, SHOP_PURCH_H), buy)
                    return onclick
                if not self.main.screens["game"].my_board.defensive[t].dead:
                    self.clickbox.append((rectloc[0]+t*SCREEN_WIDTH/4, rectloc[1], rectloc[2], rectloc[3]), what(t, tree, upgrade), z=2)
            if self.main.screens["game"].my_board.defensive[t].dead:
                surfs[t].blit(self.dead_unit, (0, 0))

    def purchased_effect(self, board, unitnum, upgrade_id):
        upgrade = self.upgrades[0][unitnum][filter(lambda x:self.upgrades[0][unitnum][x]["id"] == upgrade_id, self.upgrades[0][unitnum])[0]]
        if "effect" in upgrade:
            board.defensive[unitnum].add_effect(upgrade["effect"])
            if upgrade["effect"].etype == Effect.AERODYNAMIC:
                board.defensive[unitnum].moves_remaining += upgrade["effect"].amount

    def display(self, screen):
        Screen.display(self, screen)

        for i, x in enumerate((self.tree_one, self.tree_two, self.tree_three, self.info_sfc)):
            screen.blit(x, (SCREEN_WIDTH/4*i, 0))
            pygame.draw.line(screen, (0, 0, 0), (i*SCREEN_WIDTH/4, 0), (i*SCREEN_WIDTH/4, SCREEN_HEIGHT), 2)

    def redraw_right_panel(self, first=False):
        self.info_sfc.fill((0x99, 0xCC, 0xCC))
        # horizontal lines
        #pygame.draw.line(self.info_sfc, (0, 0, 0), (3*SCREEN_WIDTH/4, SCREEN_HEIGHT*2/3), (SCREEN_WIDTH, SCREEN_HEIGHT*2/3), 2) # bottom third of right col
        pygame.draw.line(self.info_sfc, (0, 0, 0), (0, SCREEN_HEIGHT*2/3), (SCREEN_WIDTH, SCREEN_HEIGHT*2/3), 2)
        pygame.draw.line(self.info_sfc, (0, 0, 0), (0, SCREEN_HEIGHT*5/6), (SCREEN_WIDTH, SCREEN_HEIGHT*5/6), 2)  # splits that bottom third in half
        pygame.draw.line(self.info_sfc, (0, 0, 0), (0, SCREEN_HEIGHT*11/12), (SCREEN_WIDTH, SCREEN_HEIGHT*11/12), 2)  # splits the bottom 6th in half

        # vertical lines
        pygame.draw.line(self.info_sfc, (0, 0, 0), (SCREEN_WIDTH/8, SCREEN_HEIGHT*5/6), (SCREEN_WIDTH/8, SCREEN_HEIGHT*11/12), 2)  # splits shop/game in half
        """pygame.draw.line(self.info_sfc, (0, 0, 0), (SCREEN_WIDTH/12, SCREEN_HEIGHT*11/12), (SCREEN_WIDTH/12, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.info_sfc, (0, 0, 0), (SCREEN_WIDTH/6, SCREEN_HEIGHT*11/12), (SCREEN_WIDTH/6, SCREEN_HEIGHT), 2)"""

        # text
        shopButton = self.font.render("Shop", True, COLORS["black"])
        self.info_sfc.blit(shopButton, (0+33, SCREEN_HEIGHT*5/6+15))  # TODO: fix these magic nums
        backButton = self.font.render("Back", True, COLORS["black"])
        self.info_sfc.blit(backButton, (SCREEN_WIDTH/8 + 33, SCREEN_HEIGHT*5/6+15))

        """ship1Button = self.font2.render("Ship 1", True, COLORS["black"])
        ship2Button = self.font2.render("Ship 2", True, COLORS["black"])
        ship3Button = self.font2.render("Ship 3", True, COLORS["black"])
        self.info_sfc.blit(ship1Button, (0 + 10, SCREEN_HEIGHT*11/12 + 20))
        self.info_sfc.blit(ship2Button, (SCREEN_WIDTH/12 + 10, SCREEN_HEIGHT*11/12 + 20))
        self.info_sfc.blit(ship3Button, (SCREEN_WIDTH/6 + 10, SCREEN_HEIGHT*11/12 + 20))"""

        if not first:
            resourceOverview = self.font2.render("Resource Overview", True, COLORS["black"])
            self.info_sfc.blit(resourceOverview, (0 + 25, SCREEN_HEIGHT*2/3 + 5))
            dollars = self.font3.render("$$:" + str(self.main.screens["game"].my_board.gold), True, COLORS["black"])
            exp = self.font3.render("xp:" + str(self.main.screens["game"].my_board.exp), True, COLORS["black"])
            self.info_sfc.blit(dollars, (0 + 10, SCREEN_HEIGHT*2/3 + 45))
            self.info_sfc.blit(exp, (0 + 10, SCREEN_HEIGHT*2/3 + 85))

            if self.current_upgrade is not None:
                # sets color of purchase button text

                text = self.font3.render("Purchase"+("d" if self.current_tree[self.current_upgrade]["purchased"] else ""), True, COLORS["black" if self.purchasable() else "gray"])

                # draws purchase button
                pygame.draw.rect(self.info_sfc, (0xC0, 0xC0, 0xC0), (UPGRADE_PURCHASE_INDENT, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10, SCREEN_WIDTH/4-2*UPGRADE_PURCHASE_INDENT, SHOP_PURCH_H))
                pygame.draw.rect(self.info_sfc, COLORS["black"], (UPGRADE_PURCHASE_INDENT, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10, SCREEN_WIDTH/4-2*UPGRADE_PURCHASE_INDENT, SHOP_PURCH_H), 2)
                self.info_sfc.blit(text, (UPGRADE_PURCHASE_INDENT+70, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10+7))
                # put clickbox on purchase button

                # prepares name, cost for current upgrade
                upgrade_name = self.font2.render(self.current_upgrade, True, COLORS["black"])
                upgrade_cost = self.font2.render("Cost: " + str(self.current_tree[self.current_upgrade]["cost"]) + " xp", True, COLORS["black"])
                # draws name, cost
                self.info_sfc.blit(upgrade_name, (5, 5))
                self.info_sfc.blit(upgrade_cost, (5, SHOP_TEXT_SPACING+5))

                # prepares desc for current upgrade
                textwidth = SCREEN_WIDTH/4 - 10
                textlist = [""]
                for x in self.current_tree[self.current_upgrade]["desc"].split(" "):
                    if self.font3.size(textlist[-1]+" "+x)[0] > textwidth:
                        textlist.append("")
                    textlist[-1] += x+" "
                for i, x in enumerate(textlist):
                    text = self.font3.render(x, True, COLORS["black"])
                    self.info_sfc.blit(text, (5, SHOP_TEXT_SPACING*2+5+i*SHOP_TEXT_SPACING))
                # end of text

    def right_buttons(self):
        def click_back(mpos):
            self.main.change_screen("game")

        def click_shop(mpos):
            self.main.change_screen("shop")

        def click_ship(which):
            def anon(mpos):
                self.switch_ship(which)
            return anon

        self.clickbox.append((SCREEN_WIDTH*6/8, SCREEN_HEIGHT*5/6, SCREEN_WIDTH/8, SCREEN_HEIGHT/12), click_shop)
        self.clickbox.append((SCREEN_WIDTH*7/8, SCREEN_HEIGHT*5/6, SCREEN_WIDTH/8, SCREEN_HEIGHT/12), click_back)

        """self.clickbox.append((SCREEN_WIDTH*9/12, SCREEN_HEIGHT*11/12, SCREEN_WIDTH/12, SCREEN_HEIGHT/12), click_ship(0))
        self.clickbox.append((SCREEN_WIDTH*10/12, SCREEN_HEIGHT*11/12, SCREEN_WIDTH/12, SCREEN_HEIGHT/12), click_ship(1))
        self.clickbox.append((SCREEN_WIDTH*11/12, SCREEN_HEIGHT*11/12, SCREEN_WIDTH/12, SCREEN_HEIGHT/12), click_ship(2))"""    # TODO: if you ever decide to resurrect this code (god help you) uncomment these

    def on_switch_in(self):
        self.current_upgrade = None
        self.current_tree = None
        try:
            self.clickbox.remove((UPGRADE_PURCHASE_INDENT+SCREEN_WIDTH*3/4, SCREEN_HEIGHT*2/3-SHOP_PURCH_H-10))
        except IndexError:
            pass
        self.redraw_right_panel()
        self.switch_ship()
