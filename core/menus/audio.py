from core.menus.centertext import CenterText

class Audio(CenterText):
    def __init__(self,board_surface):
        super().__init__(board_surface)

    def draw(self,volume):
        self._draw_centered_text(f"{int(volume*10)}")
    

