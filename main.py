from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

#create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 10, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

#create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP.", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP.", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP.", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

#Instantiate People
player_spells = [fire, thunder, blizzard, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]
player1 = Person("Valos:", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick :", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Kate :", 3089, 174, 288, 34, player_spells, player_items)

enemy1 = Person("Imp1  ", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus ", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp2  ", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

def players_actions(player, Enemy = enemies):
    if len(Enemy) == 0:  # if there are no enemies left
        return 0
    player.choose_actions()
    choice = input("    Choose action: ")
    index = int(choice) - 1  # because it shows starting from 1 , but we keep it starting from 0
# using attack
    if index == 0:
        dmg = player.generate_damage()
        target = player.choose_target(enemies)
        if target < 0 or target > len(enemies) - 1:
            print(bcolors.FAIL + "There are no enemies with this number" + bcolors.ENDC)
            return players_actions(player)
        Enemy[target].take_damage(dmg)
        print(bcolors.OKBLUE + "\nYou attacked " + Enemy[target].name.replace(' ', '') + " with " + str(dmg) + " points of damage. " + bcolors.ENDC)
        if Enemy[target].get_hp() == 0:  # if the enemy is defeated, then delete it from "enemies"
            print(bcolors.BOLD + bcolors.OKBLUE + Enemy[target].name.replace(' ', '') + " has died." + bcolors.ENDC)
            del Enemy[target]
# using magic
    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("    Choose magic: ")) - 1
        if magic_choice > len(player.magic) - 1 or magic_choice < 0:
            print(bcolors.FAIL + "there is no spell with this number. Choose another one" + bcolors.ENDC)
            return players_actions(player)

        spell = player.magic[magic_choice]
        current_mp = player.get_mp()

        # need to decide whether player has enough magic points for casting spell
        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough MP. Choose another action\n" + bcolors.ENDC)
            return players_actions(player)

        magic_dmg = spell.generate_damage()
        player.reduce_mp(spell.cost)
    # cure
        if spell.type == 'white':
            player.heal(magic_dmg)
            print(bcolors.OKGREEN + "\n" + spell.name + " heals for " + str(magic_dmg) + " HP." + bcolors.ENDC)
    # attack
        elif spell.type == 'black':
            target = player.choose_target(Enemy)
            if target < 0 or target > len(enemies) - 1:
                print(bcolors.FAIL + "There are no enemies with this number" + bcolors.ENDC)
                return players_actions(player)
            Enemy[target].take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " + Enemy[
                target].name.replace(' ', '') + bcolors.ENDC)
            if Enemy[target].get_hp() == 0:
                print(bcolors.OKBLUE + bcolors.BOLD + Enemy[target].name.replace(' ', '') + " has died." + bcolors.ENDC)
                del Enemy[target]
# using items
    elif index == 2:
        player.choose_items()
        item_choice = int(input("    Choose item: ")) - 1
        if item_choice == -1:  # if input is 0 (nothing is chosen), go back
            return players_actions(player)

        item = player.items[item_choice]["item"]

        if player.items[item_choice]["quantity"] == 0:  # if there are any items left
            print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
            return players_actions(player)

        player.items[item_choice]["quantity"] -= 1  # reduce the number of items
    # potion
        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP." + bcolors.ENDC)
    # elixer
        elif item.type == "elixer":
            if item.name == "MegaElixer":
                for member in players:
                    member.hp = member.maxhp
                    member.mp = member.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP for every member in party." + bcolors.ENDC)
            elif item.name == 'Elixer':
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
    # attack
        elif item.type == "attack":
            target = player.choose_target(enemies)
            if target < 0 or target > len(enemies) - 1:
                print(bcolors.FAIL + "There are no enemies with this number" + bcolors.ENDC)
                return players_actions(player)
            Enemy[target].take_damage(item.prop)
            print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " + Enemy[
                target].name.replace(' ', '') + bcolors.ENDC)
            if Enemy[target].get_hp() == 0:
                print(bcolors.OKBLUE + bcolors.BOLD + Enemy[target].name.replace(' ', '') + " has died." + bcolors.ENDC)
                del Enemy[target]
    else:
        print(bcolors.FAIL + "Choose a proper action. There are no actions with this number" + bcolors.ENDC)
        return players_actions(player)
    return 1

def enemies_actions(enemy, Player = players):
    if len(players) == 0:  # if there is no players left
        return 0
    enemy_choice = random.randrange(0, 2) #only two actions, attack and magic, no items for enemy
    if enemy_choice == 0:
# chose attack
        target = random.randrange(0, len(Player))  # will select 0, 1 or 2, not 3
        enemy_dmg = enemy.generate_damage()
        Player[target].take_damage(enemy_dmg)
        print(bcolors.FAIL + enemy.name.replace(' ', '') + " attacks " + Player[target].name + " " + str(
            enemy_dmg) + " points of damage." + bcolors.ENDC)
        if Player[target].get_hp() == 0:
            print(bcolors.BOLD + bcolors.FAIL + Player[target].name.replace(':', "") + " has died." + bcolors.ENDC)
            del players[target]
    elif enemy_choice == 1:
# chose magic
        #spell = enemy.choose_enemy_spell()
        magic_choice = random.randrange(0, len(enemy.magic))
        spell = enemy.magic[magic_choice]
        pct = enemy.hp / enemy.maxhp * 100  # percent of HP
        if enemy.mp < spell.cost or (spell.type == 'white' and pct > 50):  # no need to use healing when you still have HP
            return enemies_actions(enemy)

        magic_dmg = spell.generate_damage()
        enemy.reduce_mp(spell.cost)
    # cure
        if spell.type == 'white':
            enemy.heal(magic_dmg)
            print(bcolors.OKGREEN + spell.name + " heals " + enemy.name.replace(" ", "") + " for " + str(
                magic_dmg) + " HP." + bcolors.ENDC)
    # attack
        elif spell.type == 'black':
            target = random.randrange(0, len(Player))
            Player[target].take_damage(magic_dmg)
            print(bcolors.FAIL + enemy.name.replace(" ", '') + "'s " + spell.name + " deals " + str(
                magic_dmg) + " points of damage to " +
                  Player[target].name.replace(':', '') + bcolors.ENDC)
            if Player[target].get_hp() == 0:
                print(bcolors.BOLD + bcolors.FAIL + Player[target].name.replace(':', '') + " has died." + bcolors.ENDC)
                del Player[target]
    return 1



running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!!" + bcolors.ENDC) #RED AND BOLD and the end of colors

while running:
    print("====================")
    print("\n\n")
    print("Name                       HP                                                       MP")
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()
    print("\n")

    #players attack phase
    for player in players:
        if players_actions(player) == 0:
            print(bcolors.OKGREEN + bcolors.BOLD + "There are no enemies left" + bcolors.ENDC)

    #if enemies are defeated, then they can not attack players
    if len(enemies) == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "You win!" + bcolors.ENDC)
        running = False

    print(bcolors.FAIL + bcolors.BOLD + "------------------------------------" + bcolors.ENDC)

    # enemies attack phase
    for enemy in enemies:
        if enemies_actions(enemy, players) == 0:
            print(bcolors.FAIL  + "There are no players to attack" + bcolors.ENDC)

    # if players are defeated, they can not attack enemies
    if len(players) == 0:
        print(bcolors.FAIL + bcolors.BOLD + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

