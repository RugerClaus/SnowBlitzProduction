class Camera:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.zoom = 0.05
        self.target = None

    def follow(self, entity):
        self.target = entity

    def update(self):
        if self.target is None:
            return

        self.x = self.target.world_x
        self.y = self.target.world_y

    def get_view(self):
        width = 1 / self.zoom
        height = 1 / self.zoom

        return (
            self.x - width / 2,
            self.y - height / 2,
            width,
            height
        )