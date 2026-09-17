#__init__.py

from OpenGL import GL, GLU
from . import backcompat

def init():
    backcompat.init(GL,GLU)