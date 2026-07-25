from enum import Enum, auto
from core.ui.font import FontEngine


class SizeBar(Enum):
    BOTTOM = auto()
    TOP = auto()


class PlayerUIManager:
    def __init__(self, system, player):
        self.system = system
        self.player = player

        self.location = SizeBar.BOTTOM
        self.normalized_y = 1.0

        self.bar_width = 0
        self.bar_height = 20
        self.surface = None
        self.rect_position = (0,0)

        self.font = FontEngine(30).font
        self.score_font = FontEngine(50).font

        self.last_reset_time = self.system.time.get_current_time()

        self.scale()
        self.update()

    def toggle(self):
        if self.location == SizeBar.BOTTOM:
            self.location = SizeBar.TOP
        else:
            self.location = SizeBar.BOTTOM

        self.update()

    def scale(self):
        self.bar_width = self.system.window.get_width()
        self.surface = self.system.window.make_surface(self.bar_width,self.bar_height,True)

    def update(self):
        self.bar_width = self.system.window.get_width()

        if self.location == SizeBar.BOTTOM:
            self.normalized_y = 1.0
        else:
            self.normalized_y = 0.0

        y = int((self.system.window.get_height() - self.bar_height) * self.normalized_y)
        self.rect_position = (0,y)

    def draw_player_info(self):
        now = self.system.time.get_current_time()
        elapsed_ms = now - self.last_reset_time

        seconds = (elapsed_ms // 1000) % 60
        minutes = elapsed_ms // 60000

        time_surface = self.font.render(f"Time: {minutes:02}:{seconds:02}",True,(255,255,255))
        size_surface = self.font.render(f"Size: {round(self.player.diam)}",True,(255,255,255))
        level_size_surface = self.font.render(f"Size to level up: {self.player.level_up_size}",True,(255,255,255))

        if self.location == SizeBar.TOP:
            y = self.rect_position[1] + self.bar_height + 10
            scoreboxy = y
        else:
            y = self.rect_position[1] - 70
            scoreboxy = y + 30

        high_score_surface = self.score_font.render(f"High Score: {self.player.current_high_score}",True,(255,74,128))
        score_surface = self.score_font.render(f"Score: {self.player.score} x{self.player.multiplier}",True,(255,255,0))
        level_surface = self.score_font.render(f"Level: {self.player.current_level}",True,(255,255,255))

        high_rect = high_score_surface.get_rect(right=self.system.window.get_width()-5,top=scoreboxy)
        score_rect = score_surface.get_rect(right=high_rect.left-10,top=scoreboxy)
        level_rect = level_surface.get_rect(right=score_rect.left-10,top=scoreboxy)

        self.system.window.blit(time_surface,(10,y))
        self.system.window.blit(size_surface,(10,y+20))
        self.system.window.blit(level_size_surface,(10,y+40))

        self.system.window.blit(high_score_surface,high_rect)
        self.system.window.blit(score_surface,score_rect)
        self.system.window.blit(level_surface,level_rect)

    def draw(self):
        self.surface.fill((0,0,0))

        progress = min(self.player.diam / self.player.level_up_size,1.0)
        fill_width = max(int(self.bar_width * progress),1)

        outline = self.system.window.Rect(0,0,self.bar_width,self.bar_height)

        fill_color = (
            int(255 * (1-progress)),
            int(255 * progress),
            0
        )

        fill_rect = self.system.window.Rect(2,2,fill_width-4,self.bar_height-4)

        self.system.window.draw_rect(self.surface,fill_color,fill_rect,object="UI manager")
        self.system.window.draw_rect(self.surface,(255,255,255),outline,2,object="UI manager")

        self.system.window.blit(self.surface,self.rect_position)

        self.draw_player_info()

    def reset_timer(self):
        self.last_reset_time = self.system.time.get_current_time()