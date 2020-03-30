from random_utils import from_dungeon_level

def get_monster_chances(game_map):
    return {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], game_map.dungeon_level)
        }

def get_item_chances(game_map):
    return {
            'healing_potion': 35,
            'sword': from_dungeon_level([[5, 4]], game_map.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], game_map.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], game_map.dungeon_level), 
            'fireball_scroll': from_dungeon_level([[25, 6]], game_map.dungeon_level), 
            'confusion_scroll': from_dungeon_level([[10, 2]], game_map.dungeon_level)
        }