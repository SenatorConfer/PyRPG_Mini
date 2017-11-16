import random
import Armor
import Item
import Shield
import Weapon
import dbsetup
import Game


class Hero:
    def __init__(self, heroclass, herolevel, herohp, heroatk, herodefn, heronextlevel, herododge):
        # name
        self.name = ''
        # instance vars
        self.ourclass = heroclass
        self.level = herolevel
        self.maxhp = herohp
        self.hp = self.maxhp
        self.baseatk = heroatk
        self.atk = self.baseatk
        self.basedef = herodefn
        self.defn = self.basedef
        self.nextlevel = heronextlevel
        self.basedodge = herododge
        self.dodge = self.basedodge
        # game-created vars
        self.gold = 0
        self.items = []
        self.gear = []
        self.activeitem = 0
        self.xp = 0
        self.isbattling = False
        self.hpaug = 0
        self.dodgeaug = 0
        self.defaug = 0
        self.atkaug = 0
        self.levelupaug = 0
        self.battlecount = 0
        self.regentimer = 0
        self.hastetimer = 0

        # equip objects
        ourweapon = Weapon.Weapon(0, 0, 0, 0, 0, 0, 0)
        ourarmor = Armor.Armor(0, 0, 0, 0, 0, 0)
        ourshield = Shield.Shield(0, 0, 0, 0, 0, 0)
        ouritem = Item.Item(0, 0, 0, 0, 0)

    def isalive(self):
        if self.hp > 0:
            return True
        else:
            return False

    def heroperks(self):
        if self.ourclass == 'warrior':
            # more HP
            self.hpaug = 15
            # slower
            self.dodgeaug = 2
            # more def
            self.defaug = 12
            # low atk
            self.atkaug = 2
            # regular leveling
            self.levelupaug = 1
        elif self.ourclass == 'mage':
            # glass cannon
            self.hpaug = 5
            # med dodge
            self.dodgeaug = 5
            # low DEF
            self.defaug = 6
            # lor atk
            self.atkaug = 12
            self.levelupaug = .6
        elif self.ourclass == 'hunter':
            self.hpaug = 10
            self.dodgeaug = 8
            self.defaug = 8
            self.atkaug = 6
            self.levelupaug = .8
        self.maxhp += self.hpaug
        self.hp += self.hpaug
        self.dodge += self.dodgeaug
        self.basedef += self.defaug
        self.defn += self.defaug
        self.nextlevel = int(self.nextlevel * self.levelupaug)
        self.baseatk += self.atkaug
        self.atk += self.atkaug

    def printheroinfodetail(self):
        Game.marqueeprint('Hero Data:')
        Game.leftprint('\tClass:\t\t' + str(self.ourclass))
        Game.leftprint('\tName:\t\t' + str(self.name))
        Game.leftprint('\tLevel:\t\t' + str(self.level))
        Game.leftprint('\tMax HP:\t\t' + str(self.maxhp))
        Game.leftprint('\tCurrent HP:\t' + str(self.hp))
        Game.leftprint('\tGold:\t\t' + str(self.gold))
        Game.leftprint('\tAtk:\t\t' + str(self.atk))
        Game.leftprint('\tDefense:\t' + str(self.defn))
        Game.leftprint('\tDodge:\t\t' + str(self.dodge))
        Game.leftprint('\tXP:\t\t\t' + str(self.xp))
        Game.leftprint('\tNextLvl:\t' + str(self.nextlevel))
        Game.leftprint('\tbattles fought\t' + str(self.battlecount))

    def levelup(self):
        newdb = dbsetup.dbsetup()
        Game.marqueeprint('LEVEL UP!')
        self.printheroinfodetail()
        self.level += 1
        if self.level > 15:
            Game.marqueeprint('MAX LEVEL! YOU WIN!')
            Game.marqueeprint('THANKS FOR PLAYING')
            self.printheroinfodetail()
            quit()
        newdb.conn.execute('SELECT * FROM levelnotes WHERE level = ' + str(self.level) + ';')
        rows = newdb.conn.fetchall()
        new_hero_data = rows[0]
        self.maxhp = new_hero_data[1] + self.hpaug
        self.hp = self.maxhp + self.hpaug
        self.atk = new_hero_data[2]
        self.defn = new_hero_data[3] + self.defaug
        self.nextlevel += int(new_hero_data[4] * self.levelupaug)
        self.dodge = new_hero_data[5] + self.dodgeaug
        self.printheroinfodetail()

    def newweapon(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM weapons WHERE "level" = ? AND "class" = ? ;',
                           (str(self.level), str(self.ourclass),))
        rows = newdb.conn.fetchall()
        new_weapon_data = rows[0]
        ournewweapon = Weapon.Weapon(new_weapon_data[0], new_weapon_data[1], new_weapon_data[2], new_weapon_data[3],
                                     new_weapon_data[4], new_weapon_data[5], new_weapon_data[6])
        return ournewweapon

    def newarmor(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM armor WHERE "level" = ? AND "class" = ? ;',
                           (str(self.level), str(self.ourclass),))
        rows = newdb.conn.fetchall()
        new_armor_data = rows[0]
        ournewarmor = Armor.Armor(new_armor_data[0], new_armor_data[1], new_armor_data[2], new_armor_data[3],
                                  new_armor_data[4], new_armor_data[5])
        return ournewarmor

    def newshield(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM shields WHERE "level" = ? AND "class" = ? ;',
                           (str(self.level), str(self.ourclass),))
        rows = newdb.conn.fetchall()
        new_shield_data = rows[0]
        ournewshield = Shield.Shield(new_shield_data[0], new_shield_data[1], new_shield_data[2], new_shield_data[3],
                                     new_shield_data[4], new_shield_data[5])
        return ournewshield

    def newitem(self):
        newdb = dbsetup.dbsetup()
        newdb.conn.execute('SELECT * FROM items WHERE "level" = ? ;', (self.level,))
        rows = newdb.conn.fetchall()
        new_item_data = random.choice(rows)
        ournewitem = Item.Item(new_item_data[0], new_item_data[1], new_item_data[2], new_item_data[3], new_item_data[4])
        return ournewitem

    def applyequip(self):
        self.atk = int(self.baseatk + self.ourweapon.baseatk)
        self.defn = int(self.basedef + self.ourarmor.defn + self.ourshield.defn)
