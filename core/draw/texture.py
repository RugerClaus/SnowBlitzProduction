import pygame
import OpenGL.GL as gl

class Texture:
    def __init__(self,surface):
        self.surface = surface
        self.width, self.height = surface.get_size()
        self.id = None
        self.alpha = 255

        self.create()


    def create(self):

        data = pygame.image.tostring(
            self.surface,
            "RGBA",
            True
        )

        self.id = gl.glGenTextures(1)

        gl.glBindTexture(
            gl.GL_TEXTURE_2D,
            self.id
        )

        gl.glTexParameteri(
            gl.GL_TEXTURE_2D,
            gl.GL_TEXTURE_MIN_FILTER,
            gl.GL_LINEAR
        )

        gl.glTexParameteri(
            gl.GL_TEXTURE_2D,
            gl.GL_TEXTURE_MAG_FILTER,
            gl.GL_LINEAR
        )

        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            self.width,
            self.height,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            data
        )

        gl.glBindTexture(
            gl.GL_TEXTURE_2D,
            0
        )

    def update(self, surface):

        self.surface = surface
        self.width, self.height = surface.get_size()

        data = pygame.image.tostring(
            self.surface,
            "RGBA",
            True
        )

        gl.glBindTexture(
            gl.GL_TEXTURE_2D,
            self.id
        )

        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            self.width,
            self.height,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            data
        )

        gl.glBindTexture(
            gl.GL_TEXTURE_2D,
            0
        )

    def get_size(self):
        return self.width, self.height

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_rect(self, **kwargs):
        rect = pygame.Rect(
            0,
            0,
            self.width,
            self.height
        )

        for attribute, value in kwargs.items():
            setattr(rect, attribute, value)

        return rect

    def scale(self, width, height):
        surface = pygame.transform.scale(
            self.surface,
            (width, height)
        )

        return Texture(surface)

    def set_alpha(self, alpha):
        self.alpha = alpha

    def copy(self):
        return Texture(
            self.surface.copy()
        )
        

    def subsurface(self, *args):
        return Texture(
            self.surface.subsurface(*args)
        )

    def rotate(self, angle):
        return Texture(
            pygame.transform.rotate(
                self.surface,
                angle
            )
        )