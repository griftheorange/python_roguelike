import tcod as libtcod
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item

from entity import Entity
from game_messages import Message
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from render_functions import RenderOrder
from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level
    
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room):
       
       rooms = []
       num_rooms = 0

       for r in range(max_rooms):
           # random width and height
           w = randint(room_min_size, room_max_size)
           h = randint(room_min_size, room_max_size)
           #random position without going OOB
           x = randint(0, map_width - w - 1)
           y = randint(0, map_height - h - 1)

           # Rect class provides support for working with our rooms
           new_room = Rect(x, y, w, h)

           #Check to see if room intersects with another
           for other_room in rooms:
               if new_room.intersect(other_room):
                   break
           else:
               #no intersections, valid room
               # draw the room
               self.create_room(new_room)
               (new_x, new_y) = new_room.center()

               if num_rooms == 0:
                   # puts player in first room
                   player.x = new_x
                   player.y = new_y
               else:
                   #for all rooms after first, need to connect via tunnels
                   #center coords of prev room
                   (prev_x, prev_y) = rooms[num_rooms - 1].center()

                   # flip a coin
                   if randint(0, 1) == 1:
                       # first move horizontally, then vertical
                       self.create_h_tunnel(prev_x, new_x, prev_y)
                       self.create_v_tunnel(prev_y, new_y, new_x)
                   else:
                       # first move vertical, than horizontal
                       self.create_v_tunnel(prev_y, new_y, prev_x)
                       self.create_h_tunnel(prev_x, new_x, new_y)
                    
               self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)
               #append new room to room list
               rooms.append(new_room)
               num_rooms += 1
       print(len(rooms))

    def create_room(self, room):
        # makes all tiles within room dimensions passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].dig()

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) +1):
            self.tiles[x][y].dig()
    
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].dig()

    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        # Get random number for this room's monsters
        number_mons = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_mons):
            # Choose random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                
                entities.append(monster)
        
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_chance = randint(0, 100)

                if item_chance < 70:
                    item_component = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
                elif item_chance < 80:
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=12, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM, item=item_component)
                elif item_chance < 90:
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM, item=item_component)
                else:
                    item_component = Item(use_function=cast_lightning, damage=20, maximum_range=5)
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM, item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False