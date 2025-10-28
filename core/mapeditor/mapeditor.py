import pygame
from core.state.TileMapEditorLayer.state import TILE_EDITOR_MASTER_STATE
from core.state.TileMapEditorLayer.statemanager import TileEditorMasterStateManager
from core.menus.pause import Pause

class TileMapEditor:
    def __init__(self, window,sound,menu_callback,quit_callback):
        self.state = TileEditorMasterStateManager()
        self.window = window
        self.surface = window.make_surface(window.get_screen().get_width(), window.get_screen().get_height(), True)
        self.pause_menu = Pause(window,self.toggle_pause,self.quit_to_menu,self.quit,None)
        self.sound = sound
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        # self.camera = Camera(self.surface.get_width(), self.surface.get_height())
        # self.tilemap = TileMap()  # Your tile grid/manager
        # self.tool_manager = ToolManager()  # Subsystems for brush, selection, layers, etc.

    def toggle_pause(self):
        if not self.state.is_state(TILE_EDITOR_MASTER_STATE.PAUSED):
            self.state.set_state(TILE_EDITOR_MASTER_STATE.PAUSED)
        else:
            self.state.set_state(TILE_EDITOR_MASTER_STATE.ACTIVE)

    def handle_event(self, event, input):
        input.handle_event(event,True)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
        if self.state.is_state(TILE_EDITOR_MASTER_STATE.ACTIVE):
            if event.type == pygame.KEYDOWN:
                pass

        elif self.state.is_state(TILE_EDITOR_MASTER_STATE.PAUSED):
            self.pause_menu.handle_event(event)

    def update(self):
        if self.state.is_state(TILE_EDITOR_MASTER_STATE.ACTIVE):
            pass
            # self.tool_manager.update()
            # self.tilemap.update()
            # self.camera.update()

    def draw(self):
        self.surface.fill('green')
        self.window.blit(self.surface, (0,0))

        if self.state.is_state(TILE_EDITOR_MASTER_STATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()

    def run(self):
        self.update()
        self.draw()

    def quit_to_menu(self):
        self.menu_callback()

    def quit(self):
        self.quit_callback()