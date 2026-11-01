
import os
import random
import pygame

from settings import *
from storage import load_selected_gate

# Difficulty settings
SPACING = 175
GATE_COUNT = 6
GATE_MOVE_SPEED = 260
GATE_MAX_SPEED = 380
GATE_ACCELERATION = 1.5
GATE_GAP_WIDTH = 125

# Visual settings
GATE_VISUAL_HEIGHT = 34

GATE_COLORS = {
    "CYBER CORE.png": (0, 210, 255),
    "DIVINE AEGIS.png": (255, 205, 90),
    "FROST GUARD.png": (90, 210, 255),
    "INFERNO TITAN.png": (255, 75, 55),
    "VOID REACTOR.png": (170, 85, 255)
}


class Gate:
    def __init__(self, y, image, edge_color):
        self.y = float(y)
        self.previous_y = float(y)
        self.image = image
        self.edge_color = edge_color

        self.gap_x = random.randint(
            GATE_GAP_WIDTH // 2 + BALL_RADIUS + 5,
            WIDTH - GATE_GAP_WIDTH // 2 - BALL_RADIUS - 5
        )

        self.scored = False

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + GATE_HEIGHT

    def update(self, dt, speed):
        self.previous_y = self.y
        self.y += speed * dt

    def push_ball(self, ball, dt, speed):
        r = BALL_RADIUS

        left_edge = self.gap_x - GATE_GAP_WIDTH // 2
        right_edge = self.gap_x + GATE_GAP_WIDTH // 2

        solids = [
            (0.0, float(left_edge)),
            (float(right_edge), float(WIDTH))
        ]

        old_x = ball.x - ball.vx * dt
        old_y = ball.y - ball.vy * dt

        for solid_left, solid_right in solids:
            overlap_x = (
                ball.x + r > solid_left
                and ball.x - r < solid_right
            )

            overlap_y = (
                ball.y + r > self.top
                and ball.y - r < self.bottom
            )

            if not (overlap_x and overlap_y):
                continue

            old_bottom = old_y + r
            old_top = old_y - r
            old_right = old_x + r
            old_left = old_x - r

            if (
                old_bottom <= self.previous_y + 2
                and ball.vy >= 0
            ):
                ball.y = self.top - r
                ball.vy = speed

            elif (
                old_top >= self.previous_y + GATE_HEIGHT - 2
                and ball.vy <= 0
            ):
                ball.y = self.bottom + r
                ball.vy = 0

            elif old_right <= solid_left + 2:
                ball.x = solid_left - r
                ball.vx = 0

            elif old_left >= solid_right - 2:
                ball.x = solid_right + r
                ball.vx = 0

            else:
                ball.y = self.top - r
                ball.vy = speed

            if ball.y + r >= FLOOR_Y:
                return True

        return False

    def draw(self, screen):
        draw_y = int(
            self.y - (GATE_VISUAL_HEIGHT - GATE_HEIGHT) / 2
        )

        left_edge = self.gap_x - GATE_GAP_WIDTH // 2
        right_edge = self.gap_x + GATE_GAP_WIDTH // 2

        if left_edge > 0:
            screen.blit(
                self.image,
                (0, draw_y),
                pygame.Rect(
                    0, 0,
                    left_edge,
                    GATE_VISUAL_HEIGHT
                )
            )

        if right_edge < WIDTH:
            screen.blit(
                self.image,
                (right_edge, draw_y),
                pygame.Rect(
                    right_edge, 0,
                    WIDTH - right_edge,
                    GATE_VISUAL_HEIGHT
                )
            )

        pygame.draw.line(
            screen,
            self.edge_color,
            (left_edge - 1, draw_y + 7),
            (left_edge - 1, draw_y + GATE_VISUAL_HEIGHT - 7),
            2
        )

        pygame.draw.line(
            screen,
            self.edge_color,
            (right_edge, draw_y + 7),
            (right_edge, draw_y + GATE_VISUAL_HEIGHT - 7),
            2
        )


class GateManager:
    def __init__(self):
        self.gates = []
        self.elapsed_time = 0

        base_path = os.path.dirname(os.path.abspath(__file__))

        selected_gate = load_selected_gate()
        image_path = os.path.join(base_path, selected_gate)

        try:
            original_image = pygame.image.load(
                image_path
            ).convert_alpha()

        except (pygame.error, OSError):
            fallback_path = os.path.join(base_path, "gate.png")
            original_image = pygame.image.load(
                fallback_path
            ).convert_alpha()

        self.gate_image = pygame.transform.smoothscale(
            original_image,
            (WIDTH, GATE_VISUAL_HEIGHT)
        )

        self.edge_color = GATE_COLORS.get(
            selected_gate,
            (0, 210, 255)
        )

        for i in range(GATE_COUNT):
            y = -GATE_HEIGHT - (i * SPACING)

            self.gates.append(
                Gate(y, self.gate_image, self.edge_color)
            )

    def update(self, dt, ball):
        self.elapsed_time += dt

        current_speed = min(
            GATE_MOVE_SPEED + self.elapsed_time * GATE_ACCELERATION,
            GATE_MAX_SPEED
        )

        points = 0
        crushed = False

        for gate in self.gates:
            gate.update(dt, current_speed)

            if gate.push_ball(ball, dt, current_speed):
                crushed = True

            if (
                not gate.scored
                and gate.top > ball.y + BALL_RADIUS
            ):
                gate.scored = True
                points += 1

        self.gates = [
            gate for gate in self.gates
            if gate.top <= HEIGHT
        ]

        while len(self.gates) < GATE_COUNT:
            highest_y = min(
                gate.y for gate in self.gates
            )

            new_y = highest_y - SPACING

            self.gates.append(
                Gate(
                    new_y,
                    self.gate_image,
                    self.edge_color
                )
            )

        self.gates.sort(key=lambda gate: gate.y)

        return points, crushed

    def draw(self, screen):
        for gate in self.gates:
            gate.draw(screen)
