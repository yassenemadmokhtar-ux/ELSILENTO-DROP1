
import os
import pygame

from settings import *
from storage import (
    load_selected_ball,
    save_selected_ball,
    load_selected_background,
    save_selected_background,
    load_selected_gate,
    save_selected_gate
)


class BallShop:
    def __init__(self):
        self.selected_ball = load_selected_ball()
        self.selected_background = load_selected_background()
        self.selected_gate = load_selected_gate()

        self.current_tab = "balls"

        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.name_font = pygame.font.SysFont("arial", 16, bold=True)
        self.small_font = pygame.font.SysFont("arial", 11, bold=True)
        self.button_font = pygame.font.SysFont("arial", 12, bold=True)

        self.back_button = pygame.Rect(25, 735, 120, 43)

        self.tabs = {
            "balls": pygame.Rect(15, 78, 130, 40),
            "backgrounds": pygame.Rect(160, 78, 130, 40),
            "gates": pygame.Rect(305, 78, 130, 40)
        }

        self.balls = [
            {"file": "ball.png", "name": "CLASSIC", "color": (0, 210, 255)},
            {"file": "ball_inferno.png", "name": "INFERNO", "color": (255, 75, 55)},
            {"file": "ball_void.png", "name": "VOID SOUL", "color": (170, 85, 255)},
            {"file": "ball_divine.png", "name": "DIVINE STAR", "color": (255, 205, 90)},
            {"file": "ball_frostbite.png", "name": "FROSTBITE", "color": (90, 210, 255)}
        ]

        self.backgrounds = [
            {"file": "bg_space.png", "name": "DEEP SPACE", "color": (0, 180, 255)},
            {"file": "bg_city.png", "name": "NEON CITY", "color": (170, 85, 255)},
            {"file": "bg_void.png", "name": "DARK VOID", "color": (170, 85, 255)},
            {"file": "bg_inferno.png", "name": "INFERNO", "color": (255, 75, 55)},
            {"file": "bg_ice.png", "name": "FROZEN WORLD", "color": (90, 210, 255)}
        ]

        self.gates = [
            {"file": "CYBER CORE.png", "name": "CYBER CORE", "color": (0, 210, 255)},
            {"file": "DIVINE AEGIS.png", "name": "DIVINE AEGIS", "color": (255, 205, 90)},
            {"file": "FROST GUARD.png", "name": "FROST GUARD", "color": (90, 210, 255)},
            {"file": "INFERNO TITAN.png", "name": "INFERNO TITAN", "color": (255, 75, 55)},
            {"file": "VOID REACTOR.png", "name": "VOID REACTOR", "color": (170, 85, 255)}
        ]

        self.images = {}
        self.buttons = {}

        base_path = os.path.dirname(os.path.abspath(__file__))

        for item in self.balls:
            filename = item["file"]
            path = os.path.join(base_path, filename)

            try:
                image = pygame.image.load(path).convert_alpha()
                self.images[filename] = pygame.transform.smoothscale(
                    image, (72, 72)
                )
            except (pygame.error, OSError):
                self.images[filename] = None

        for item in self.backgrounds:
            filename = item["file"]
            path = os.path.join(base_path, filename)

            try:
                image = pygame.image.load(path).convert()
                self.images[filename] = pygame.transform.smoothscale(
                    image, (125, 80)
                )
            except (pygame.error, OSError):
                self.images[filename] = None

        for item in self.gates:
            filename = item["file"]
            path = os.path.join(base_path, filename)

            try:
                image = pygame.image.load(path).convert_alpha()
                self.images[filename] = pygame.transform.smoothscale(
                    image, (190, 15)
                )
            except (pygame.error, OSError):
                self.images[filename] = None

        for i, item in enumerate(
            self.balls + self.backgrounds + self.gates
        ):
            y = 130 + (i % 5) * 112
            self.buttons[item["file"]] = pygame.Rect(
                WIDTH - 137, y + 31, 95, 38
            )

        self.cards = [
            pygame.Rect(25, 130 + i * 112, WIDTH - 50, 100)
            for i in range(5)
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos

            if self.back_button.collidepoint(mouse):
                return "back"

            for tab, rect in self.tabs.items():
                if rect.collidepoint(mouse):
                    self.current_tab = tab
                    return None

            if self.current_tab == "balls":
                items = self.balls
            elif self.current_tab == "backgrounds":
                items = self.backgrounds
            else:
                items = self.gates

            for item in items:
                filename = item["file"]

                if self.buttons[filename].collidepoint(mouse):
                    if self.current_tab == "balls":
                        save_selected_ball(filename)
                        self.selected_ball = filename

                    elif self.current_tab == "backgrounds":
                        save_selected_background(filename)
                        self.selected_background = filename

                    else:
                        save_selected_gate(filename)
                        self.selected_gate = filename

                    return "equipped"

        return None

    def draw_background(self, screen):
        screen.fill((6, 8, 19))
        grid = (13, 20, 36)

        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, grid, (x, 0), (x, HEIGHT), 1)

        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, grid, (0, y), (WIDTH, y), 1)

    def draw_button(self, screen, text, rect, color):
        hovered = rect.collidepoint(pygame.mouse.get_pos())
        bg = (15, 55, 75) if hovered else (11, 27, 43)

        pygame.draw.rect(screen, bg, rect, border_radius=9)
        pygame.draw.rect(screen, color, rect, 2, border_radius=9)

        label = self.button_font.render(text, True, (245, 250, 255))
        screen.blit(label, label.get_rect(center=rect.center))

    def draw(self, screen):
        self.draw_background(screen)

        title = self.title_font.render(
            "SHOP", True, (0, 215, 255)
        )
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))

        for tab, rect in self.tabs.items():
            active = self.current_tab == tab
            color = (0, 210, 255) if active else (55, 85, 110)

            text = {
                "balls": "BALLS",
                "backgrounds": "BACKGROUNDS",
                "gates": "GATES"
            }[tab]

            self.draw_button(screen, text, rect, color)

        if self.current_tab == "balls":
            items = self.balls
            selected = self.selected_ball
        elif self.current_tab == "backgrounds":
            items = self.backgrounds
            selected = self.selected_background
        else:
            items = self.gates
            selected = self.selected_gate

        for i, item in enumerate(items):
            filename = item["file"]
            name = item["name"]
            color = item["color"]

            card = self.cards[i]
            button = self.buttons[filename]
            equipped = filename == selected

            card_bg = (13, 38, 52) if equipped else (13, 24, 42)
            border = color if equipped else (38, 58, 83)

            pygame.draw.rect(screen, card_bg, card, border_radius=14)
            pygame.draw.rect(screen, border, card, 2, border_radius=14)

            image = self.images.get(filename)

            if self.current_tab == "backgrounds":
                if image:
                    screen.blit(image, (card.x + 10, card.y + 10))
                else:
                    missing = self.small_font.render(
                        "IMAGE NOT FOUND", True, (255, 100, 100)
                    )
                    screen.blit(missing, (card.x + 10, card.y + 40))

                text_x = card.x + 145

            elif self.current_tab == "gates":
                if image:
                    screen.blit(
                        image,
                        (card.x + 10, card.y + 42)
                    )
                else:
                    missing = self.small_font.render(
                        "IMAGE NOT FOUND", True, (255, 100, 100)
                    )
                    screen.blit(missing, (card.x + 10, card.y + 40))

                text_x = card.x + 215

            else:
                if image:
                    screen.blit(image, (card.x + 13, card.y + 14))
                else:
                    missing = self.small_font.render(
                        "NO IMAGE", True, (255, 100, 100)
                    )
                    screen.blit(
                        missing,
                        missing.get_rect(
                            center=(card.x + 49, card.centery)
                        )
                    )

                text_x = card.x + 96

            name_label = self.name_font.render(
                name, True, (240, 245, 255)
            )
            screen.blit(name_label, (text_x, card.y + 28))

            if equipped:
                status = self.small_font.render(
                    "CURRENTLY EQUIPPED", True, color
                )
                screen.blit(status, (text_x, card.y + 53))
                button_text = "SELECTED"
            else:
                button_text = "EQUIP"

            self.draw_button(screen, button_text, button, color)

        self.draw_button(
            screen, "BACK", self.back_button, (0, 190, 230)
        )
