import tcod as libtcod

# Number of spaces a player increments per move
SPEED = 1
def handle_keys(key):
    # Player Movement
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -SPEED)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, SPEED)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-SPEED, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (SPEED, 0)}

    # Non-Movement
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter toggles fullscreen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}
    
    # No press
    return {}