class UpgradeFactory(object):
    DAMAGE = 1
    MOVEMENT = 2
    SPECIAL = 3
    
    created = {}
    def __new__(_, idd):
        if idd in created:
            return created[idd]
        if idd == UpgradeFactory.DAMAGE:
            foo = ["MORTAR", "JNAUT", "TORPEDO"]    # tokens
            foo = [UpgradeFactory(f) for f in foo]  # values
            val = Upgrade("Damage","The Base Damage class, should be invisible.","o",foo,"nope",50,"../img/yellow_sub.png")
            created[idd] = val
            return val
        if idd == UpgradeFactory.MOVEMENT:
            return 1
        if idd == UpgradeFactory.SPECIAL:
            return 2
        if idd == "MORTAR":
            val = Upgrade("Mortar", "The Mortar class, I'm possibly invisible too?", "FLAVA FLAAAAV", [], "nope", 50, "../img/yellow_sub.png")
        if idd == "JNAUT":
            val = Upgrade("Juggernaut", "The Jaunt class", "So jaunt", [], "nope", 50, "../img/yellow_sub.png")
        if idd == "TORPEDO":
            val = Upgrade("Torpedo", "The Torpedo class", "Torp", [], "nope", 50, "../img/yellow_sub.png")
        raise ValueError("Unknown unit id "+str(idd))

class Upgrade:
    def __init__(self, name, desc, flavor, unlocks, effect, cost, img):
        self.name = name
        self.description = desc
        self.flavor = flavor
        self.unlocks = unlocks
        self.game_effect = effect
        self.cost = cost
        self.img = pygame.image.load(img)
