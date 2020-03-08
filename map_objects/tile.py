class Tile:
    """
    A tile on a map. It may or may be blocked/transparent
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # By default, blocked tiles also block sight
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight
    
    def dig(self):
        self.blocked = False
        self.block_sight = False