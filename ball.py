
import math
import os
import pygame
from settings import *
from storage import load_selected_ball

START_GATE_SPEED = 260
MAX_GATE_SPEED = 380
GATE_ACCELERATION = 1.5


class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = FLOOR_Y - 100
        self.vx = 0.0
        self.vy = 0.0

        self.radius = BALL_RADIUS
        self.visual_size = 34

        self.hit_floor = False
        self.trail = []
        self.elapsed_time = 0.0
        self.current_speed = BALL_SPEED

        self.load_image()

    def load_image(self):
        filename = load_selected_ball()

        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            filename
        )

        original_image = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.smoothscale(
            original_image,
            (self.visual_size, self.visual_size)
        )

    def update_speed(self):
        gate_speed = min(
            START_GATE_SPEED + self.elapsed_time * GATE_ACCELERATION,
            MAX_GATE_SPEED
        )

        multiplier = gate_speed / START_GATE_SPEED
        self.current_speed = BALL_SPEED * multiplier

    def launch(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        if math.hypot(dx, dy) < 15:
            return

        self.update_speed()

        if abs(dx) >= abs(dy):
            self.vx = self.current_speed if dx > 0 else -self.current_speed
            self.vy = 0.0
        else:
            self.vx = 0.0
            self.vy = self.current_speed if dy > 0 else -self.current_speed

        self.hit_floor = False

    def stop_horizontal(self):
        self.vx = 0.0

    def stop_vertical(self):
        self.vy = 0.0

    def update(self, dt):
        self.elapsed_time += dt
        self.update_speed()

        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x - self.radius < 0:
            self.x = self.radius
            self.stop_horizontal()
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.stop_horizontal()

        if self.y - self.radius < CEILING_Y:
            self.y = CEILING_Y + self.radius
            self.stop_vertical()

        if self.y + self.radius > FLOOR_Y:
            self.y = FLOOR_Y - self.radius
            self.stop_vertical()
            self.hit_floor = True

        self.trail.append((self.x, self.y))
        self.trail = self.trail[-12:]

    def draw(self, screen):
        for i, position in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)

            pygame.draw.circle(
                screen,
                (20, int(100 * alpha), int(150 * alpha)),
                (int(position[0]), int(position[1])),
                max(2, int(self.radius * alpha * 0.65))
            )

        screen.blit(
            self.image,
            (
                int(self.x - self.visual_size / 2),
                int(self.y - self.visual_size / 2)
            )
        )
