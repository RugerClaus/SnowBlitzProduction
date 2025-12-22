class Endless:
    def __init__(self,surface,player):
        self.surface = surface
        self.player = player

    def run(self):
        self.player.update()
        self.player.draw()