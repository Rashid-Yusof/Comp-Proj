from map import rooms
import string

def display_room(room):
    print('')
    print(room['name'].upper())
    print('')
    print(room['description'])
    print('')
    
#display_room(rooms['Office'])

def print_menu_line(direction, leads_to):
    print('Go', direction.upper(), 'to', leads_to.upper())
    
#print_menu_line('east', 'Bathroom')

def exit_leads_to(exits, direction):
    room_id = exits[direction]
    room = rooms[room_id]
    return(room['name'])
        
#exit_leads_to(rooms['Reception']['exits'], 'south')

def print_menu(exits):
    print ('You can:')
    for key in exits:
        print_menu_line(key, exit_leads_to(exits, key))
    print('Where do you want to go?')

#print_menu(rooms['Reception']['exits'])

def menu(exits):
    while True:
        print_menu(exits)
        answer = normalise_input(input())
        validity = is_valid_exit(exits, answer)
        if validity == True:
            return answer
            break
        else:
            print ('\n**Please choose one of the directions given!**\n')
        

def move(exits, direction):
    return rooms[exits[direction]]
    
        
#move(rooms['Reception']['exits'],'east')
        
def is_valid_exit(exits, user_input):
    if user_input in exits:
        return True
    else:
        return False
        
def remove_punct(text):
    for c in string.punctuation:
        text = text.replace(c, '')
    return text

#print (remove_punct('Hello, I am Rashid.@#$'))

def remove_spaces(text):
    text = text.lstrip()
    text = text.rstrip()
    return text
    
def normalise_input(user_input):
    user_input = remove_punct(user_input)
    user_input = remove_spaces(user_input)
    return user_input.lower()
        
def main():
    current_room = rooms["Reception"]
    
    while True:
        display_room(current_room)
        exits = current_room["exits"]
        direction = menu(exits)
        current_room = move(exits, direction)     

main()