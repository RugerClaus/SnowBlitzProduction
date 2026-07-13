from core.state.ApplicationLayer.GameMode.TutorialLayer.state import TUTORIALSTATE


class TutorialManager:

    def __init__(
        self,
        system,
        prompts,
        controls,
        entitymanager,
        player,
        progress_bar,
        state
    ):

        self.system = system
        self.prompts = prompts
        self.controls = controls
        self.entitymanager = entitymanager
        self.player = player
        self.progress_bar = progress_bar
        self.state = state


    def reset(self):

        self.prompts.player_has_moved = False
        self.prompts.player_has_continued = False

        self.entitymanager.reset_entities()
        self.player.reset()

        self.state.set_state(
            TUTORIALSTATE.RESET
        )


    def update_entities(self):

        self.entitymanager.spawn_snowflakes()
        self.entitymanager.update_entities()


    def update_survival(self):

        self.player.update()

        self.entitymanager.spawn_snowflakes()
        self.entitymanager.spawn_rocks(
            self.player.current_level
        )
        self.entitymanager.spawn_powerups(
            self.player.current_level
        )
        self.entitymanager.spawn_reducers(
            self.player.current_level
        )

        self.entitymanager.update_entities()

        self.entitymanager.check_collisions()


    def draw_survival(self):

        self.player.draw()

        self.entitymanager.draw_entities()

        self.progress_bar.draw()


    def update(self):

        if self.state.is_state(TUTORIALSTATE.MOVEMENT_PROMPT):

            self.prompts.movement_trigger()

            if self.prompts.player_has_moved:
                self.state.set_state(
                    TUTORIALSTATE.BEGIN
                )


        elif self.state.is_state(TUTORIALSTATE.BEGIN):

            self.player.update()

            self.entitymanager.spawn_snowflakes()
            self.entitymanager.update_entities()

            for snowflake in self.entitymanager.entities["snowflakes"]:
                if snowflake.y >= self.system.window.get_height() // 4:
                    self.state.set_state(
                        TUTORIALSTATE.SNOW_PROMPT
                    )


        elif self.state.is_state(TUTORIALSTATE.SNOW_PROMPT):

            self.prompts.handle_continue_input()

            if self.prompts.player_has_continued:

                self.prompts.player_has_continued = False

                self.state.set_state(
                    TUTORIALSTATE.SNOW
                )


        elif self.state.is_state(TUTORIALSTATE.SNOW):

            self.player.update()

            self.entitymanager.spawn_snowflakes()
            self.entitymanager.spawn_speed_boosts(
                self.player.current_level
            )

            self.entitymanager.update_entities()
            self.entitymanager.check_collisions()

            for boost in self.entitymanager.entities["speedboosts"]:
                if boost.y >= self.system.window.get_height() // 4:
                    self.state.set_state(
                        TUTORIALSTATE.SPEED_BOOST_PROMPT
                    )


        elif self.state.is_state(TUTORIALSTATE.SPEED_BOOST_PROMPT):

            self.prompts.handle_continue_input()

            if self.prompts.player_has_continued:

                self.prompts.player_has_continued = False

                self.state.set_state(
                    TUTORIALSTATE.SPEED_BOOST
                )


        elif self.state.is_state(TUTORIALSTATE.SPEED_BOOST):

            self.player.update()

            self.entitymanager.spawn_snowflakes()
            self.entitymanager.spawn_speed_boosts(
                self.player.current_level
            )
            self.entitymanager.spawn_rocks(
                self.player.current_level
            )

            self.entitymanager.update_entities()
            self.entitymanager.check_collisions()

            for rock in self.entitymanager.entities["rocks"]:
                if rock.y >= self.system.window.get_height() // 4:
                    self.state.set_state(
                        TUTORIALSTATE.ROCKS_PROMPT
                    )


        elif self.state.is_state(TUTORIALSTATE.ROCKS_PROMPT):

            self.prompts.handle_continue_input()

            if self.prompts.player_has_continued:

                self.prompts.player_has_continued = False

                self.state.set_state(
                    TUTORIALSTATE.ROCKS
                )


        elif self.state.is_state(TUTORIALSTATE.ROCKS):

            self.player.update()

            self.entitymanager.spawn_snowflakes()
            self.entitymanager.spawn_rocks(
                self.player.current_level
            )
            self.entitymanager.spawn_speed_boosts(
                self.player.current_level
            )
            self.entitymanager.spawn_powerups(
                self.player.current_level
            )

            self.entitymanager.update_entities()
            self.entitymanager.check_collisions()

            for powerup in self.entitymanager.entities["powerups"]:
                if powerup.y >= self.system.window.get_height() // 4:
                    self.state.set_state(
                        TUTORIALSTATE.POWERUPS_PROMPT
                    )


        elif self.state.is_state(TUTORIALSTATE.POWERUPS_PROMPT):

            self.prompts.handle_continue_input()

            if self.prompts.player_has_continued:

                self.prompts.player_has_continued = False

                self.state.set_state(
                    TUTORIALSTATE.POWERUPS
                )


        elif self.state.is_state(TUTORIALSTATE.POWERUPS):

            self.update_survival()

            for reducer in self.entitymanager.entities["level_reducers"]:
                if reducer.y >= self.system.window.get_height() // 4:
                    self.state.set_state(
                        TUTORIALSTATE.LEVEL_REDUCER_PROMPT
                    )


        elif self.state.is_state(TUTORIALSTATE.LEVEL_REDUCER_PROMPT):

            self.prompts.handle_continue_input()

            if self.prompts.player_has_continued:

                self.prompts.player_has_continued = False

                self.state.set_state(
                    TUTORIALSTATE.LEVEL_REDUCERS
                )


        elif self.state.is_state(TUTORIALSTATE.LEVEL_REDUCERS):

            self.update_survival()

            if self.player.current_level >= 20:

                print("you win")

                self.state.set_state(
                    TUTORIALSTATE.WIN
                )


        elif self.state.is_state(TUTORIALSTATE.RESET):

            self.prompts.player_has_moved = False
            self.prompts.player_has_continued = False

            self.entitymanager.reset_entities()
            self.player.reset()

            self.state.set_state(
                TUTORIALSTATE.MOVEMENT_PROMPT
            )


        self.progress_bar.update()


    def draw(self):

        if self.state.is_state(TUTORIALSTATE.MOVEMENT_PROMPT):

            self.player.draw()
            self.progress_bar.draw()
            self.prompts.movement_prompt()


        elif self.state.is_state(TUTORIALSTATE.BEGIN):

            self.player.draw()
            self.entitymanager.draw_entities()
            self.progress_bar.draw()


        elif self.state.is_state(TUTORIALSTATE.SNOW_PROMPT):

            self.player.draw()
            self.entitymanager.draw_entities()
            self.progress_bar.draw()
            self.prompts.snow_prompt()


        elif self.state.is_state(TUTORIALSTATE.SNOW):

            self.draw_survival()


        elif self.state.is_state(TUTORIALSTATE.SPEED_BOOST_PROMPT):

            self.player.draw()
            self.entitymanager.draw_entities()
            self.progress_bar.draw()
            self.prompts.speed_boost_prompt()


        elif self.state.is_state(TUTORIALSTATE.SPEED_BOOST):

            self.draw_survival()


        elif self.state.is_state(TUTORIALSTATE.ROCKS_PROMPT):

            self.player.draw()
            self.entitymanager.draw_entities()
            self.progress_bar.draw()
            self.prompts.rock_prompt()


        elif self.state.is_state(TUTORIALSTATE.ROCKS):

            self.draw_survival()


        elif self.state.is_state(TUTORIALSTATE.POWERUPS_PROMPT):

            self.player.draw()
            self.entitymanager.draw_entities()
            self.progress_bar.draw()
            self.prompts.powerup_prompt()


        elif self.state.is_state(TUTORIALSTATE.POWERUPS):

            self.draw_survival()


        elif self.state.is_state(TUTORIALSTATE.LEVEL_REDUCER_PROMPT):

            self.player.draw()
            self.entitymanager.draw_entities()
            self.progress_bar.draw()
            self.prompts.reducer_prompt()


        elif self.state.is_state(TUTORIALSTATE.LEVEL_REDUCERS):

            self.draw_survival()