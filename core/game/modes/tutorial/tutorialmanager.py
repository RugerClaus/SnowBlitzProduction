from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE

class TutorialManager:
    def __init__(self, board_surface, prompts, controls, entitymanager, player, progress_bar,state):
        self.board_surface = board_surface
        self.prompts = prompts
        self.controls = controls
        self.entitymanager = entitymanager
        self.player = player
        self.progress_bar = progress_bar

        self.state = state

    def wait(self):
        self.player.draw_wait()
        self.progress_bar.update()
        self.progress_bar.draw()
        self.entitymanager.draw_entities()

    def final(self):
        self.player.update()
        self.player.draw()
        self.progress_bar.update()
        self.progress_bar.draw()
        self.entitymanager.spawn_snowflakes()
        self.entitymanager.spawn_rocks(self.player.current_level)
        self.entitymanager.spawn_multiplier_upgrades()
        self.entitymanager.spawn_powerups(self.player.current_level)
        self.entitymanager.spawn_reducers(self.player.current_level)
        self.entitymanager.update_entities()
        self.entitymanager.draw_entities()
        self.entitymanager.spawn_rocks(self.player.current_level)
        self.player.check_collisions(self.entitymanager.get_active_entities())

    def update(self):

        if self.state.is_state(TUTORIALSTATE.MOVEMENT_PROMPT):
            self.player.draw_wait()
            self.progress_bar.update()
            self.progress_bar.draw()
            self.prompts.movement_prompt()
            self.prompts.handle_movement_input(self.controls)
            if self.prompts.player_has_moved:
                self.state.set_state(TUTORIALSTATE.BEGIN)

        elif self.state.is_state(TUTORIALSTATE.BEGIN):
            self.player.update()
            self.player.draw()
            self.progress_bar.update()
            self.progress_bar.draw()
            self.entitymanager.spawn_snowflakes()
            self.entitymanager.update_entities()
            self.entitymanager.draw_entities()
            for snowflake in self.entitymanager.entities["snowflakes"]:
                if snowflake.y >= self.board_surface.get_height() // 4:
                    self.state.set_state(TUTORIALSTATE.SNOW_PROMPT)

        elif self.state.is_state(TUTORIALSTATE.SNOW_PROMPT):
            self.wait()
            self.prompts.snow_prompt()
            self.prompts.handle_continue_input()
            if self.prompts.player_has_continued:
                self.prompts.player_has_continued = False
                self.state.set_state(TUTORIALSTATE.SNOW)

        elif self.state.is_state(TUTORIALSTATE.SNOW):
            self.player.update()
            self.player.draw()
            self.progress_bar.update()
            self.progress_bar.draw()
            self.entitymanager.update_entities()
            self.entitymanager.draw_entities()
            self.entitymanager.spawn_snowflakes()
            self.entitymanager.spawn_rocks(self.player.current_level)
            self.entitymanager.check_collisions()
            self.player.check_collisions(self.entitymanager.get_active_entities())

            for rock in self.entitymanager.entities["rocks"]:
                if rock.y >= self.board_surface.get_height() // 4:
                    self.state.set_state(TUTORIALSTATE.ROCKS_PROMPT)

        elif self.state.is_state(TUTORIALSTATE.ROCKS_PROMPT):
            self.wait()
            self.prompts.rock_prompt()
            self.prompts.handle_continue_input()
            if self.prompts.player_has_continued:
                self.prompts.player_has_continued = False
                self.state.set_state(TUTORIALSTATE.ROCKS)

        elif self.state.is_state(TUTORIALSTATE.ROCKS):
            self.player.update()
            self.player.draw()
            self.progress_bar.update()
            self.progress_bar.draw()
            self.entitymanager.spawn_snowflakes()
            self.entitymanager.spawn_rocks(self.player.current_level)
            self.entitymanager.spawn_multiplier_upgrades(self.player.current_level,True)
            self.entitymanager.update_entities()
            self.entitymanager.draw_entities()
            self.entitymanager.spawn_rocks(self.player.current_level)
            self.player.check_collisions(self.entitymanager.get_active_entities())

            for multiplierupgrade in self.entitymanager.entities["multiplierupgrades"]:
                if multiplierupgrade.y >= self.board_surface.get_height() // 4:
                    self.state.set_state(TUTORIALSTATE.MULTIPLIER_UPGRADES_PROMPT)

        elif self.state.is_state(TUTORIALSTATE.MULTIPLIER_UPGRADES_PROMPT):
            self.wait()
            self.prompts.multiplier_upgrades_prompt()
            self.prompts.handle_continue_input()
            if self.prompts.player_has_continued:
                self.prompts.player_has_continued = False
                self.state.set_state(TUTORIALSTATE.MULTIPLIER_UPGRADES)
        
        elif self.state.is_state(TUTORIALSTATE.MULTIPLIER_UPGRADES):
            self.player.update()
            self.player.draw()
            self.progress_bar.update()
            self.progress_bar.draw()
            self.entitymanager.spawn_snowflakes()
            self.entitymanager.spawn_rocks(self.player.current_level)
            self.entitymanager.spawn_multiplier_upgrades()
            self.entitymanager.spawn_powerups(self.player.current_level)
            self.entitymanager.update_entities()
            self.entitymanager.draw_entities()
            self.entitymanager.spawn_rocks(self.player.current_level)
            self.player.check_collisions(self.entitymanager.get_active_entities())

            for powerup in self.entitymanager.entities["powerups"]:
                if powerup.y >= self.board_surface.get_height() // 4:
                    self.state.set_state(TUTORIALSTATE.POWERUPS_PROMPT)

        elif self.state.is_state(TUTORIALSTATE.POWERUPS_PROMPT):
            self.wait()
            self.prompts.powerup_prompt()
            self.prompts.handle_continue_input()
            if self.prompts.player_has_continued:
                self.prompts.player_has_continued = False
                self.state.set_state(TUTORIALSTATE.POWERUPS)

        elif self.state.is_state(TUTORIALSTATE.POWERUPS):
            self.final()
            for reducer in self.entitymanager.entities["level_reducers"]:
                if reducer.y >= self.board_surface.get_height() // 4:
                    self.state.set_state(TUTORIALSTATE.LEVEL_REDUCER_PROMPT)

        elif self.state.is_state(TUTORIALSTATE.LEVEL_REDUCER_PROMPT):
            self.wait()
            self.prompts.reducer_prompt()
            self.prompts.handle_continue_input()
            if self.prompts.player_has_continued:
                self.prompts.player_has_continued = False
                self.state.set_state(TUTORIALSTATE.LEVEL_REDUCERS)

        elif self.state.is_state(TUTORIALSTATE.LEVEL_REDUCERS):
            self.final()

            if self.player.current_level > 20:
                self.state.set_state(TUTORIALSTATE.WIN)

        elif self.state.is_state(TUTORIALSTATE.RESET):
            self.prompts.player_has_moved = False
            self.prompts.player_has_continued = False
            self.entitymanager.reset_entities()
            self.player.reset()
            self.state.set_state(TUTORIALSTATE.MOVEMENT_PROMPT)
        
        self.entitymanager.check_collisions()