import math,pygame
from random import randint
from core.game.raycaster.settings import *
from core.game.entities.entity import Entity
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Movement.Move.statemanager import PlayerMoveStateManager
from core.state.GameLayer.Entities.Player.Movement.Turn.statemanager import PlayerTurnStateManager

class Player(Entity):
    def __init__(self,surface):
        super().__init__(surface.get_width()/2, surface.get_height()/2, radius=6, speed=2.5)
        self.surface = surface
        self.rotation_speed = 2 * (math.pi/180)
        self.move_intent = PlayerMoveStateManager(initial_state=PLAYER_INTENT_STATE.IDLE_MOVE)
        self.turn_intent = PlayerTurnStateManager(initial_state=PLAYER_INTENT_STATE.IDLE_TURN)
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.map_x = WINDOW_WIDTH / 4
        self.map_y = WINDOW_HEIGHT / 4
        self.radius = 6
        self.turn_direction = 0 # -1 left 1 right 0 center float
        self.walk_direction = 0 # 1 player moving forward -1 player move backward
        self.speed = 2.5
        self.rotation_speed = 2 * (math.pi/180)
        self.rotation_angle = -45*(math.pi/180)
        self.level = 1

    def find_safe_spawn(self, game_map):
        for _ in range(150):
            random_col = randint(0, COLS - 1)
            random_row = randint(0, ROWS - 1)

            # Check if the tile is empty (0)
            if game_map.map_grid[random_row][random_col] == 0:
                # Ensure the surrounding tiles are also empty (not walls)
                # Check surrounding tiles: top, bottom, left, right (if within bounds)
                if (random_row > 0 and game_map.map_grid[random_row - 1][random_col] == 0) and \
                (random_row < ROWS - 1 and game_map.map_grid[random_row + 1][random_col] == 0) and \
                (random_col > 0 and game_map.map_grid[random_row][random_col - 1] == 0) and \
                (random_col < COLS - 1 and game_map.map_grid[random_row][random_col + 1] == 0):
                    # Spawn the player at this location (convert tile index to pixel)
                    self.x = random_col * TILE_SIZE
                    self.y = random_row * TILE_SIZE
                    self.walk_direction = 0
                    self.turn_direction = 0
                    return  # Exit once a valid spawn point is found

        # If no valid spot was found after 102 tries, default to the center of the map
        self.x = (COLS // 2) * TILE_SIZE
        self.y = (ROWS // 2) * TILE_SIZE

                    
    def will_collide(self, new_x, new_y, game_map):
        #check all cardinal directions. this idea should have been obvious for circle collision and I can just use math.pi to calculate 
        # the trajectory of every angle around the player and determine if the player hits a wall that way
        # das is good
        for angle in (0, math.pi/2, math.pi, 3*math.pi/2):
            check_x = new_x + math.cos(angle) * self.radius
            check_y = new_y + math.sin(angle) * self.radius

            if game_map.has_wall_at(check_x, check_y) == 1:
                return True
            elif game_map.has_wall_at(check_x,check_y) == 2:
                self.level += 1
                self.find_safe_spawn(game_map)
                return True
        return False

    def update(self,game_map):

        self.walk_direction = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.walk_direction = 1
            self.move_intent.set_state(PLAYER_INTENT_STATE.MOVE_FORWARD)
        elif keys[pygame.K_s]:
            self.walk_direction = -1
            self.move_intent.set_state(PLAYER_INTENT_STATE.MOVE_BACKWARD)
        
        self.turn_direction = 0
        if keys[pygame.K_a]:
            self.turn_direction = -1
            self.turn_intent.set_state(PLAYER_INTENT_STATE.TURN_LEFT)
        elif keys[pygame.K_d]:
            self.turn_direction = 1
            self.turn_intent.set_state(PLAYER_INTENT_STATE.TURN_RIGHT)

        move_step = self.walk_direction * self.speed

        self.rotation_angle += self.turn_direction * self.rotation_speed
        new_x = self.x + math.cos(self.rotation_angle) * move_step
        new_y = self.y + math.sin(self.rotation_angle) * move_step


        if not self.will_collide(new_x, new_y, game_map):
            self.x = new_x
            self.y = new_y

        #handle player on minimap

        self.map_x = max(0, min((self.x / WINDOW_WIDTH) * (WINDOW_WIDTH // 4), WINDOW_WIDTH // 4))
        self.map_y = max(0, min((self.y / WINDOW_HEIGHT) * (WINDOW_HEIGHT // 4), WINDOW_HEIGHT // 4))

    def draw(self, display):


        pygame.draw.circle(display,GREEN,(self.map_x,self.map_y), self.radius)

        pygame.draw.line(display,RED,(self.map_x,self.map_y), (self.map_x + math.cos(self.rotation_angle)*(self.radius*2),self.map_y+math.sin(self.rotation_angle)*(self.radius*2)))

    