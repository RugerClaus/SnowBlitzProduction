class Endless:
    def __init__(self, progress_bar, player, entitymanager):
        self.progress_bar = progress_bar
        self.player = player
        self.entitymanager = entitymanager

    def run(self):
        self.player.update()
        self.player.draw()
        
        self.entitymanager.update_entities()
        self.entitymanager.draw_entities()  

        self.player.check_collisions(self.entitymanager.get_active_entities()) 
        self.entitymanager.spawn_snowflakes()
        self.entitymanager.spawn_rocks(self.player.current_level)
        self.entitymanager.spawn_multiplier_upgrades()
        self.entitymanager.spawn_speed_boosts()
        self.entitymanager.spawn_powerups(self.player.current_level)
        self.entitymanager.spawn_reducers(self.player.current_level)
        self.entitymanager.check_collisions()

        self.progress_bar.update()
        self.progress_bar.draw()