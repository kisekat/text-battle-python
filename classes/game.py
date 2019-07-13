import random
from classes.magic import Spell

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'  #red
    ENDC = '\033[0m'   #end of colors
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = "\033[97m"


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        '''hp - health points, mp - magic points, atk - attack, df - defense'''
        self.maxhp = hp #for keeping the maximum of health points, in order to not overheal the person
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name


    def generate_damage(self):
        return random.randrange(self.atkl,self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self,dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_actions(self):
        i = 1
        print("\n" + bcolors.BOLD + "    " +self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ".", item)
            i +=1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            if spell.type == 'black':
                print("        " + str(i) + ".", spell.name,"(damage: " + str(spell.dmg) +", cost: ",str(spell.cost) + ")")
            elif spell.type == 'white':
                print("        " + str(i) + ".", spell.name, "(cure: " + str(spell.dmg) + ", cost: ", str(spell.cost) + ")")
            i += 1

    def choose_items(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name, ": ", item["item"].description, "(x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1
        enemy = int(input("    Choose target: ")) - 1
        return enemy

    def get_stats(self):
        len_symb = len(bcolors.WHITE + "█" + bcolors.ENDC) # == 10, the length of every painted symbol is 10

        #creating a bar for HP
        hp_bar = ""
        hp_bar_ticks = int((self.hp / self.maxhp) * 100 / 4)
        while hp_bar_ticks > 0:
            hp_bar += bcolors.OKGREEN + "█" + bcolors.ENDC
            hp_bar_ticks -= 1
        while len(hp_bar)/len_symb < 25:
            hp_bar +=bcolors.WHITE + "█" + bcolors.ENDC

        str_hp = str(self.hp) + "/" + str(self.maxhp) + ' '
        while len(str_hp) < 16: # filling up the space between the name and the HP bar
            str_hp = ' ' + str_hp


        #creating a bar for MP
        mp_bar = ""
        mp_bar_ticks = int((self.mp / self.maxmp) * 100 / 10)
        while mp_bar_ticks > 0:
            mp_bar += bcolors.OKBLUE + "█" + bcolors.ENDC
            mp_bar_ticks -= 1
        while len(mp_bar)/len_symb < 10:
            mp_bar += bcolors.WHITE + "█" + bcolors.ENDC

        str_mp = ' ' + str(self.mp) + "/" + str(self.maxmp) + ' '
        while len(str_mp) < 21: # filling up the space between the HP bar and the MP bar
            str_mp = ' ' + str_mp


        #printing the result
        print(bcolors.BOLD + self.name + str_hp + "|" + hp_bar + bcolors.ENDC +
              bcolors.BOLD + "|" + str_mp + "|" + mp_bar + bcolors.BOLD + "|" + bcolors.ENDC)


    def get_enemy_stats(self):
        len_symb = len(bcolors.WHITE + "█" + bcolors.ENDC)  # == 10, the length of every painted symbol is 10

        # creating a bar for HP
        hp_bar = ""
        hp_bar_ticks = int((self.hp / self.maxhp) * 100 / 2)
        while hp_bar_ticks > 0:
            hp_bar += bcolors.FAIL + "█" + bcolors.ENDC
            hp_bar_ticks -= 1
        while len(hp_bar) / len_symb < 50:
            hp_bar += bcolors.WHITE + "█" + bcolors.ENDC

        str_hp = str(self.hp) + "/" + str(self.maxhp) + ' '
        while len(str_hp) < 16:  # filling up the space between the name and the HP bar
            str_hp = ' ' + str_hp

        # printing the result
        print(bcolors.BOLD + self.name + str_hp + "|" + hp_bar + bcolors.ENDC + bcolors.BOLD + "|" + bcolors.ENDC)




