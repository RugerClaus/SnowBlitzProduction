class Endless:
    def __init__(self, progress_bar, player, entitymanager):
        self.progress_bar = progress_bar
        self.player = player
        self.entitymanager = entitymanager
        
    def update(self):
        
        self.player.update()
        
        self.entitymanager.update_entities()
         
        self.entitymanager.spawn_snowflakes()
        self.entitymanager.spawn_rocks(self.player.current_level)
        self.entitymanager.spawn_speed_boosts()
        self.entitymanager.spawn_powerups(self.player.current_level)
        self.entitymanager.spawn_reducers(self.player.current_level)
        self.entitymanager.check_collisions()
        self.progress_bar.update()
        

        
    def draw(self):
        self.player.draw()
        self.entitymanager.draw_entities() 
        self.progress_bar.draw()