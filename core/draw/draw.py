# core/draw/draw.py

import threading

from queue import Queue, Empty
from concurrent.futures import Future

from core.draw.renderer import Renderer
from core.draw.geometry.geometry import Geometry
from core.draw.texture import Texture


gpu_queue = Queue()

renderer = None
window = None
pygame = None

width = None
height = None

def normalize_color(color):
    if len(color) == 3:
        return (
            color[0] / 255.0,
            color[1] / 255.0,
            color[2] / 255.0,
            1.0
        )

    if len(color) == 4:
        return tuple(channel / 255.0 for channel in color)

    raise ValueError("color must contain 3 or 4 channels")

def queue_gpu_task(task):
    future = Future()
    gpu_queue.put((task, future))
    return future


def process_gpu_tasks():
    while True:
        try:
            task, future = gpu_queue.get_nowait()
        except Empty:
            break

        try:
            future.set_result(task())
        except Exception as error:
            future.set_exception(error)


def init(gl, glutils, pygame_api):
    global pygame

    pygame = pygame_api


def set_mode(
    system,
    ww,
    wh,
    title="Distant Realms Window",
    resizable=False,
    fullscreen=False
):
    global renderer
    global window
    global width
    global height

    width = ww
    height = wh

    window = pygame.Window(
        title=title,
        size=(width, height),
        resizable=resizable,
        fullscreen=fullscreen,
        opengl=True
    )

    renderer = Renderer(window)

    Geometry.init(renderer)

    renderer.update_viewport()

    return window


def set_icon(icon):
    window.set_icon(icon)


def clear(color=(0, 0, 0), alpha=None):
    if alpha is None:
        alpha = 255

    color = tuple(channel / 255.0 for channel in color)

    renderer.clear(
        color=(
            color[0],
            color[1],
            color[2],
            alpha / 255.0
        )
    )


def rect(surface, color, rect, width=0, border_radius=None, object=None):
    color = normalize_color(color)
    drawable = Geometry.rect(
        rect.centerx,
        rect.centery,
        rect.width,
        rect.height,
        color
    )

    renderer.render(
        drawable,
        0.0
    )


def circle(a, b, c, d, e):
    pass


def make_surface(system, size, alpha=False):
    flags = pygame.SRCALPHA if alpha else 0

    return pygame.Surface(
        size,
        flags
    )


def upload_surface(surface, pygame_surface):
    return Texture(pygame_surface)


def blit(surface, destination, area=None):
    texture = surface

    if not isinstance(texture, Texture):
        texture = Texture(surface)

    if hasattr(destination, "x"):
        x = destination.centerx
        y = destination.centery
        dest_width = destination.width
        dest_height = destination.height

    else:
        x, y = destination
        dest_width = texture.width
        dest_height = texture.height

    drawable = Geometry.texture(
        x,
        y,
        dest_width,
        dest_height,
        texture,
        renderer.texture_shader
    )

    renderer.render(
        drawable,
        0.0
    )


def surface_fill(surface, color, rect=None, alpha=None):
    if isinstance(color, tuple) and len(color) == 4:
        color, alpha = color[:3], color[3]

    if alpha is None:
        alpha = 255

    color = tuple(channel / 255.0 for channel in color)

    if rect is None:
        surface.fill(
            (*tuple(int(channel * 255) for channel in color), alpha)
        )
        return

    surface.fill(
        (*tuple(int(channel * 255) for channel in color), alpha),
        rect
    )


def flip():
    return window.flip()


def get_screen():
    return window


def quit():
    pygame.quit()