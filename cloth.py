import numpy as np
import config

class Point:
    def __init__(self, x, y, locked=False):
        self.pos = np.array([x, y], dtype=float)
        self.old_pos = np.array([x, y], dtype=float)
        self.locked = locked

    def update(self):
        if self.locked:
            return
        velocity = self.pos - self.old_pos
        self.old_pos = self.pos.copy()
        self.pos += velocity
        self.pos[1] += config.GRAVITY

        # Giới hạn biên
        self.pos[0] = np.clip(self.pos[0], 0, config.WIDTH)
        self.pos[1] = np.clip(self.pos[1], 0, config.HEIGHT)

class Stick:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = np.linalg.norm(p1.pos - p2.pos)
        self.broken = False

    def update(self):
        if self.broken:
            return
        delta = self.p2.pos - self.p1.pos
        dist = np.linalg.norm(delta)
        diff = (self.length - dist) / dist * 0.5
        offset = delta * diff
        if not self.p1.locked:
            self.p1.pos -= offset
        if not self.p2.locked:
            self.p2.pos += offset

class Cloth:
    def __init__(self, width, height, spacing):
        self.points = []
        self.sticks = []
        for y in range(height):
            row = []
            for x in range(width):
                p = Point(x * spacing + 100, y * spacing + 50, locked=(y == 0))
                row.append(p)
                self.points.append(p)
                # nối với điểm bên trái
                if x > 0:
                    self.sticks.append(Stick(row[x-1], row[x]))
                # nối với điểm phía trên
                if y > 0:
                    self.sticks.append(Stick(self.points[(y-1)*width + x], p))
        self.width = width
        self.height = height

    def update(self):
        for p in self.points:
            p.update()
        for _ in range(config.ITERATIONS):
            for s in self.sticks:
                s.update()

    def cut(self, pos):
        for s in self.sticks:
            if s.broken:
                continue
            mid = (s.p1.pos + s.p2.pos) / 2
            if np.linalg.norm(mid - pos) < config.CUT_RADIUS:
                s.broken = True
