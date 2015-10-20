from items import *
from finalItems import *
from map import rooms

player = {"health": 40, "alive": True}

inventory = [item_laptop]

wearing = []

money = 5.0
  
# Start game at the reception
current_room = rooms["Bedroom"]
