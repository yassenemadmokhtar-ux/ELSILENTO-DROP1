
import random
import pygame

from settings import *


class Effects:
    def __init__(self):
        self.stars = []

        for _ in range(55):
            self.stars.append([
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.uniform(15, 45)
            ])

    def update(self, dt):
        for star in self.stars:
            star[1] += star[2] * dt

            if star[1] > HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, WIDTH)

    def draw(self, screen):
        # لا تمسح الشاشة هنا؛ الخلفية مرسومة بالفعل

        for x, y, speed in self.stars:
            pygame.draw.circle(
                screen,
                (45, 65, 100),
                (int(x), int(y)),
                1
            )

        pygame.draw.line(
            screen,
            (35, 45, 75),
            (0, CEILING_Y),
            (WIDTH, CEILING_Y),
            2
        )

        pygame.draw.line(
            screen,
            PURPLE,
            (0, FLOOR_Y),
            (WIDTH, FLOOR_Y),
            3
        )
