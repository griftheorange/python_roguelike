from random import randint

from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
    
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
       
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
                            self.create_v_tunner(prev_y, new_y, new_x)
                        else:
                            # first move vertical, than horizontal
                            self.create_v_tunner(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)
                    
                    #append new room to room list
                    rooms.append(new_room)
                    num_rooms += 1

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

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False