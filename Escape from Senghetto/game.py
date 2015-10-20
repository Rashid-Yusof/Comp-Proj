from map import rooms
from player import *
from finalItems import *
from gameparser import *
from beggar import *
from shop import *
from Descriptions import *
import string
global bathroom_locked
global item_bacon
game_loop = True
sense = True
bathroom_locked = True

#changes: inventory 6, clothes inventory, check self
""" nEw changes , move function, Line 342-348, bathroom lock
bathroom_locked line 7
cook bacon function line 26
done bathroom lock
bacon trick
"""

""" To do: 
1) Locks
2) Shop
3) Alley Boss
4) Endings
5) Bacon trick
6) sell laptop
"""

def print_shop_menu():
    print("\nItem\tPrice")
    for item in ware:
        if ware[item] == True:
            print(item+"\t£"+str(prices[item]))
    if ware["water"] is False and ware["wand"] is False:
        print("There is nothing to buy.\n")
        return
    else:
        print("What do you want to buy?")
        user_input = normalise_input(input('\n> '))
        buy_item(user_input)
        
def buy_item(user_input):
    global money
    print()
    if ware[user_input]:
        if money >= prices[user_input]:
            money -= prices[user_input]
            if user_input == "wand":
                inventory.append(item_wand)
                ware["wand"] =False
                print("a wand is added to your inventory. You have £"+str(money)+" left.")
            elif user_input == "water":
                player["health"] = 100
                ware["water"] = False
                print("Health is 100% now. You have £"+str(money)+" left.")
        else:
            print("You don't have enough money.")
    else:
        print("Item is out of stock.")
        
def go_outside():
    global current_room
    if (item_top in wearing) and (item_boxers in wearing) and (item_trousers in wearing):
        current_room = rooms["Outside"]
    else:
        print("You are not wearing all of your clothes.")    

def bacon_usage(item):
    global item_bacon
    global bathroom_locked
    if item['usage'] == True:
        bathroom_locked = False
        
def laptop_usage(item):
    global item_laptop
    global money
    if item['usage'] == True:
        money += 100
        
#def laptop_usage(item):
    #if laptop_usage == True:
        #pass

def print_usage(item):
    global item_bacon
    global bathroom_locked
    for thing in inventory:
        if thing['id'] == item:
            if thing['room_to_use'] == current_room['name']:
                thing['usage'] = True
                print (thing['item_effect'])
                print ()
                inventory.remove(thing)
                bacon_usage(thing)
                laptop_usage(thing)
                return
            else:
                print ("You try to use", thing['id'] + '... ', "It fails to do whatever ludicrous idea you had for it.")
                print()

        
def check_self(thing):
    global wearing
    if wearing != []:
        print ('You are wearing:')
        for item in wearing:
            print (item['name'])
    else:
        print ('You are naked, other than that everthing seems normal.')
        print ()

def list_of_items(items):
    """This function takes a list of items (see items.py for the definition) and
    returns a comma-separated list of item names (as a string). For example:
    >>> list_of_items([item_pen, item_handbook])
    'a pen, a student handbook'
    >>> list_of_items([item_id])
    'id card'
    >>> list_of_items([])
    ''
    >>> list_of_items([item_money, item_handbook, item_laptop])
    'money, a student handbook, laptop'
    """
    new_list = []
    for item in items:
        new_list.append(item['name'])
    if new_list == []:
        return ''
    return ', '.join(new_list)


def print_room_items(room):
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names. For example:
    >>> print_room_items(rooms["Reception"])
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>
    >>> print_room_items(rooms["Office"])
    There is a pen here.
    <BLANKLINE>
    >>> print_room_items(rooms["Admins"])
    (no output)
    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    if len(list_of_items(room['items'])) > 0:
        print ('There is' ,list_of_items(room['items']), 'here.')
        print ('')


def print_inventory_items(items):
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:
    >>> print_inventory_items(inventory)
    You have id card, laptop, money.
    <BLANKLINE>
    """
    if list_of_items(items) != (""):
        print ('You have',list_of_items(items) + '.')
        print ('')
    else:
        print ('You have no items.')
        print ()
        


def print_room(room):
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this). For example:
    >>> print_room(rooms["Office"])
    <BLANKLINE>
    THE GENERAL OFFICE
    <BLANKLINE>
    You are standing next to the cashier's till at
    30-36 Newport Road. The cashier looks at you with hope
    in their eyes. If you go west you can return to the
    Queen's Buildings.
    <BLANKLINE>
    There is a pen here.
    <BLANKLINE>
    >>> print_room(rooms["Reception"])
    <BLANKLINE>
    RECEPTION
    <BLANKLINE>
    You are in a maze of twisty little passages, all alike.
    Next to you is the School of Computer Science and
    Informatics reception. The receptionist, Matt Strangis,
    seems to be playing an old school text-based adventure
    game on his computer. There are corridors leading to the
    south and east. The exit is to the west.
    <BLANKLINE>
    There is a pack of biscuits, a student handbook here.
    <BLANKLINE>
    >>> print_room(rooms["Admins"])
    <BLANKLINE>
    MJ AND SIMON'S ROOM
    <BLANKLINE>
    You are leaning agains the door of the systems managers'
    room. Inside you notice Matt "MJ" John and Simon Jones. They
    ignore you. To the north is the reception.
    <BLANKLINE>
    Note: <BLANKLINE> here means that doctest should expect a blank line.
    """
    if sense == True:
        print('')
        print(room["name"].upper())
        print('')
        print(room["description"])
        print('')
        print_room_items(room)

def exit_leads_to(exits, direction):
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads. For example:
    >>> exit_leads_to(rooms["Reception"]["exits"], "south")
    "MJ and Simon's room"
    >>> exit_leads_to(rooms["Reception"]["exits"], "east")
    "your personal tutor's office"
    >>> exit_leads_to(rooms["Tutor"]["exits"], "west")
    'Reception'
    """
    room_id = exits[direction]
    room = rooms[room_id]
    return(room['name'])

def print_exit(direction, leads_to):
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:
    GO <EXIT NAME UPPERCASE> to <where it leads>.
    For example:
    >>> print_exit("east", "you personal tutor's office")
    GO EAST to you personal tutor's office.
    >>> print_exit("south", "MJ and Simon's room")
    GO SOUTH to MJ and Simon's room.
    """
    print("GO " + direction.upper() + " to go to the " + leads_to + ".")


def print_menu(exits, room_items, inv_items):
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print
    "TAKE <ITEM ID> to take <item name>."
    and for each item in the inventory print
    "DROP <ITEM ID> to drop <item name>."
    For example, the menu of actions available at the Reception may look like this:
    You can:
    GO EAST to your personal tutor's office.
    GO WEST to the parking lot.
    GO SOUTH to MJ and Simon's room.
    TAKE BISCUITS to take a pack of biscuits.
    TAKE HANDBOOK to take a student handbook.
    DROP ID to drop your id card.
    DROP LAPTOP to drop your laptop.
    DROP MONEY to drop your money.
    What do you want to do?
    """
    print ('You can:')
    
    for key in exits:
        print_exit(key, exit_leads_to(exits, key))
    for item in room_items:
        print ('TAKE',item['id'].upper(),'to take',item['name'].upper())
    for item in inv_items:
        print ('DROP', item['id'].upper(),'to drop',item['name'].upper())
    for item in inv_items:
        print ('USE', item['id'].upper(),'to use',item['name'].upper())
    if current_room is rooms["Shop"]:
        print("SHOW MENU to show the menu")
    print ('CHECK SELF to check what you are wearing')
    print('What do you want to do?')
    print ()


def is_valid_exit(exits, chosen_exit):
    """This function checks, given a dictionary "exits" (see map.py) and
    a players's choice "chosen_exit" whether the player has chosen a valid exit.
    It returns True if the exit is valid, and False otherwise. Assume that
    the name of the exit has been normalised by the function normalise_input().
    For example:
    >>> is_valid_exit(rooms["Reception"]["exits"], "south")
    True
    >>> is_valid_exit(rooms["Reception"]["exits"], "up")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "west")
    False
    >>> is_valid_exit(rooms["Parking"]["exits"], "east")
    True
    """
    return chosen_exit in exits
    
def check_item(item):
    for thing in inventory:
        if thing['id'] == item:
            return thing


def execute_beat():
    global inventory
    global player
    global current_room
    while player["alive"] is True and constitution["alive"] is True:
        if inventory == []:
            print ('You have no usable items. The tramp beats you to death')
            return
        else:
            print_inventory_items(inventory)
            user_input = input("Which item do you want to use? ")
            item = normalise_input(user_input)
            thing = check_item(item)
            constitution["Health"]-= thing['damage_beggar']
            player["health"] -= thing['damage_player']
            inventory.remove(thing)
            print("Your health: ", player["health"], "\t\tBeggar's health: ", constitution["Health"])
            if constitution["Health"] <= 0:
                constitution["alive"] = False
            if player["health"] <= 0:
                player["alive"] = False
    if player["alive"] and not constitution["alive"]:
        print("The beggar falls to the floor in a mess of blood.")
        current_room = rooms["Alley_After"]
        return True
    else:
        print("You feel yourself feel weak as the beggar beats you to the floor. ")
        print("You have been bested by Senghetto")
        return False
        
def beggar_fight():
    global current_room
    global description
    if current_room == rooms["Alley"]:
        print (descriptions["angry homeless man"])
        while True:
            user_input = input("Do you wish to pay the beggar? ")
            yes_no = normalise_input(user_input)
            if yes_no == 'yes':
            #take away money
                print ("The beggar accepts the money and scrurries away.")
                return
            if yes_no == 'no': 
                if execute_beat() == True:
                    return True
                else:
                    return False
            else:
                print ("Pardon?")


def execute_go(direction):
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room
    if direction in current_room['exits']:
        if current_room is rooms["Exit"] and direction == "east":
            go_outside()
        else:
            roomid = current_room['exits'][direction]
            if rooms[roomid] != rooms['Bathroom']:
                current_room = rooms[roomid]
            elif bathroom_locked == False:
                current_room = rooms[roomid]
            else:
                print ("Horrendous singing is coming from inside the bathroom. You'd rather not go in, you don't want to relive 'The Accident'.")
                print ()
    else:
        print ("You cannot go there.")
        print ()


def execute_take(item_id):
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """
    global inventory
    global current_room
    for item in current_room['items']:
        if item_id == item['id']:
            global clothes
            for garment in clothes:
                if item_id == garment['id']:
                    wearing.append(garment)
                    current_room['items'].remove(garment)
                    print(garment['description'])
                    print("You proceed to wear it.")
                    print()
                    return
            if len(inventory) < 6:
                inventory.append(item)
                current_room['items'].remove(item)
                print(item['description'])
                print()
                return
            else:
                print ('You can only carry 6 items!')
                print()
                return
    print ('You cannot take that')
    print ()
    

def execute_drop(item_id):
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    global inventory
    global current_room
    for item in inventory:
        if item_id == item['id']:
            inventory.remove(item)
            current_room['items'].append(item)
            return
        
    print ('You cannot drop that.')    
    print ()
    

def execute_command(command):
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.
    """

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")
            
    elif command[0] == 'check':
        if command[1] == 'self':
            check_self(wearing)
    
    elif command[0] == 'use':
        if len(command) > 1:
            print_usage(command[1])
            
    elif command[0] == 'show':
        if command[1] == 'menu':
            print_shop_menu()
            
    else:
        print("This makes no sense.")


def menu(exits, room_items, inv_items):
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned.
    """
    print_menu(exits, room_items, inv_items)
    answer = normalise_input(input('> '))
    return answer


def move(exits, direction):
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction". For example:
    >>> move(rooms["Reception"]["exits"], "south") == rooms["Admins"]
    True
    >>> move(rooms["Reception"]["exits"], "east") == rooms["Tutor"]
    True
    >>> move(rooms["Reception"]["exits"], "west") == rooms["Office"]
    False
    """
    #return rooms[exits[direction]] , rooms["Bathroom"]
    pass

def win_lose():

    global game_loop
    if current_room == rooms["Bus Stop"]:
        print_room(rooms["Bus Stop"])

        while True:
            user_input = input("Do you want to board the bus? ")
            board_bus = normalise_input(user_input)
            if board_bus == "yes":
                if money < 1.80:
                    print(descriptions["insufficient funds"])
                    return
                else:

                    if constitution["alive"] == False: #Player killed the beggar

                        if ware["wand"] == False: #Player bought the wand
                            if rooms["Alley"]["items"] != item_beggar: #Player hid the beggar's dead body
                                print (descriptions["hogwarts end credits"])
                                game_loop = False
                                return
                            else: #Player did NOT hide the beggar's body
                                print(descriptions["hogwarts alt credits"])
                                game_loop = False
                                return
                        else: #Player did NOT buy the wand
                            if rooms["Alley"]["items"] != item_beggar: #Player hid the beggar's dead body
                                print(descriptions["common credits"])
                                game_loop = False
                                return
                            else: #Player did NOT hide the beggar's body
                                print(descriptions["murder charge credits"])
                                game_loop = False
                                return
                    else: #Player did NOT kill the beggar
                        if ware["wand"] == False: #Player bought the wand
                            print (descriptions["hogwarts end credits"])
                            game_loop = False
                            return
                        else:
                            print(descriptions["common credits"]) #Player didn't buy the wand
                            game_loop = False
                            return
            else:
                pass
    


# This is the entry point of our program
def main():
    global sense
    global game_loop
    
    while game_loop == True:
        roomfirst = current_room
        print_room(current_room)
        print_inventory_items(inventory)
        command = menu(current_room["exits"], current_room["items"], inventory)
        command = command.split()
        execute_command(command)
        if beggar_fight() == False:
            return
        if roomfirst == current_room:
            sense = False
        else:
            sense = True
        win_lose()


if __name__ == "__main__":
    main()