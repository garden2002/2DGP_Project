class Goal:
    def __init__(self, x, y,x_size ,y_size, stage):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.stage = stage

    def draw(self):
        pass

    def get_bb(self):
        return self.x - self.x_size, self.y - self.y_size, self.x + self.x_size, self.y + self.y_size

    def handle_collision(self, group, other):
        pass
