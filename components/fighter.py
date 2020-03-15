class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
    
    def take_damage(self, amount):
        self.hp -= amount
        print('{0} has {1} hitpoints left.'.format(self.owner.name, str(self.hp)))
    
    def attack(self, target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            print('{0} attacks {1} for {2} hit points!'.format(self.owner.name.capitalize(), target.name, str(damage)))
        else:
            print('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name))