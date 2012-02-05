class UpgradeFactory(object):
    DAMAGE = 1
    MOVEMENT = 2
    SPECIAL = 3
    created = []
    def __new__(_, idd):
        if created.contains(idd):
            return thetokentoidd
        if idd == UpgradeFactory.DAMAGE:
            foo = [ALL THE SHIT]
            foo = [UpgradeFactory(f) for f in foo]
            return Upgrade("Poop","Allows you to poop","Everybody poops and if they don't they're an android.",[],[],"nope",50,"../img/yellow_sub.png")
        if idd == UpgradeFactory.MOVEMENT:
            foo = [ALL THE SHIT]
            foo = [UpgradeFactory(f) for f in foo]
            return Upgrade(loc, (2,2), "../img/yellow_sub.png", Unit.OFFENSE)
        if idd == UpgradeFactory.SPECIAL:
            foo = [ALL THE SHIT]
            foo = [UpgradeFactory(f) for f in foo]
            return Upgrade(loc, (1,1), "../img/bullet.png", Unit.BULLET)
        raise ValueError("Unknown unit id "+str(idd))

class Upgrade:
    def __init__(self, name, desc, flavor, prereqs, unlocks, effect, cost, img):
        self.name = name
        self.description = desc
        self.flavor = flavor
        self.prereqs = prereqs
        self.unlocks = unlocks
        self.game_effect = effect
        self.cost = cost
        self.img = pygame.image.load(img)
