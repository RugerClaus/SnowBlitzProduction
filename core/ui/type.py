from enum import Enum,auto

class WIDGET(Enum):
    QUERY = auto()
    TEXTBOX = auto()
    LABEL = auto()
    BUTTON = auto()
    FORM = auto()

class COMPOSABLE(Enum):
    FORM = auto()