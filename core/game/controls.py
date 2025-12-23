class Controls:
    def __init__(self):
        self.move_left = None
        self.move_right = None

    def set_controls(self, move_left, move_right):
        self.move_left = move_left
        self.move_right = move_right