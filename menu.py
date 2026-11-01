
import math
import random
import pygame

from settings import *


class MainMenu:
    def __init__(self):
        self.time = 0.0
        self.settings_open = False

        self.logo_font = pygame.font.SysFont("arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.drop_font = pygame.font.SysFont("arial", 54, bold=True)
        self.button_font = pygame.font.SysFont("arial", 18, bold=True)
        self.small_font = pygame.font.SysFont("arial", 12, bold=True)
        self.tiny_font = pygame.font.SysFont("arial", 10, bold=True)

        cx = WIDTH // 2

        self.buttons = {
            "PLAY": pygame.Rect(cx - 112, 458, 224, 48),
            "SHOP": pygame.Rect(cx - 112, 518, 224, 48),
            "SETTINGS": pygame.Rect(cx - 112, 578, 224, 48),
            "EXIT": pygame.Rect(cx - 112, 638, 224, 48)
        }

        self.back_button = pygame.Rect(cx - 100, 510, 200, 48)

        self.particles = []

        for _ in range(65):
            self.particles.append({
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "speed": random.uniform(12, 38),
                "size": random.choice([1, 1, 2]),
                "phase": random.uniform(0, math.tau)
            })

        self.background = self.create_background()

    def create_background(self):
        bg = pygame.Surface((WIDTH, HEIGHT))

        top = (3, 5, 16)
        bottom = (10, 13, 32)

        for y in range(HEIGHT):
            t = y / HEIGHT
            color = (
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t)
            )
            pygame.draw.line(bg, color, (0, y), (WIDTH, y))

        # Background grid
        for x in range(0, WIDTH, 30):
            pygame.draw.line(bg, (12, 23, 42), (x, 0), (x, HEIGHT), 1)

        for y in range(0, HEIGHT, 30):
            pygame.draw.line(bg, (12, 23, 42), (0, y), (WIDTH, y), 1)

        # Dark side panels
        pygame.draw.rect(bg, (5, 9, 22), (0, 0, 18, HEIGHT))
        pygame.draw.rect(bg, (5, 9, 22), (WIDTH - 18, 0, 18, HEIGHT))

        return bg

    def update(self, dt):
        self.time += dt

        for p in self.particles:
            p["y"] += p["speed"] * dt

            if p["y"] > HEIGHT:
                p["y"] = -5
                p["x"] = random.randint(0, WIDTH)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not self.settings_open:
                return "play"

            if event.key == pygame.K_ESCAPE:
                if self.settings_open:
                    self.settings_open = False
                else:
                    return "exit"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = event.pos

            if self.settings_open:
                if self.back_button.collidepoint(mouse):
                    self.settings_open = False
                return None

            if self.buttons["PLAY"].collidepoint(mouse):
                return "play"

            if self.buttons["SHOP"].collidepoint(mouse):
                return "shop"

            if self.buttons["SETTINGS"].collidepoint(mouse):
                self.settings_open = True

            elif self.buttons["EXIT"].collidepoint(mouse):
                return "exit"

        return None

    def draw_background(self, screen):
        screen.blit(self.background, (0, 0))

        # Animated particles
        for p in self.particles:
            pulse = (math.sin(self.time * 2.5 + p["phase"]) + 1) / 2
            brightness = int(70 + pulse * 150)

            pygame.draw.circle(
                screen,
                (0, brightness, min(255, brightness + 35)),
                (int(p["x"]), int(p["y"])),
                p["size"]
            )

        # Neon side rails
        rail_pulse = int(90 + (math.sin(self.time * 2) + 1) * 45)

        pygame.draw.line(
            screen, (0, rail_pulse, 190),
            (18, 0), (18, HEIGHT), 1
        )

        pygame.draw.line(
            screen, (90, 35, 180),
            (WIDTH - 18, 0), (WIDTH - 18, HEIGHT), 1
        )

    def draw_portal(self, screen):
        cx = WIDTH // 2
        cy = 300

        pulse = (math.sin(self.time * 2.2) + 1) / 2
        rotation = self.time * 0.5

        # Soft glow
        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        pygame.draw.circle(
            glow, (0, 160, 255, 25),
            (cx, cy), int(120 + pulse * 15)
        )

        pygame.draw.circle(
            glow, (100, 30, 220, 18),
            (cx, cy), int(155 + pulse * 10)
        )

        screen.blit(glow, (0, 0))

        # Portal rings
        pygame.draw.ellipse(
            screen, (0, 95, 145),
            (cx - 112, cy - 65, 224, 130), 2
        )

        pygame.draw.ellipse(
            screen, (0, 200, 245),
            (cx - 96, cy - 53, 192, 106), 3
        )

        pygame.draw.ellipse(
            screen, (85, 45, 190),
            (cx - 80, cy - 42, 160, 84), 2
        )

        # Rotating energy segments
        for i in range(12):
            angle = rotation + i * math.tau / 12

            x1 = cx + math.cos(angle) * 103
            y1 = cy + math.sin(angle) * 58

            x2 = cx + math.cos(angle + 0.12) * 115
            y2 = cy + math.sin(angle + 0.12) * 65

            color = (0, 190 + (i % 3) * 20, 255)

            pygame.draw.line(
                screen, color,
                (int(x1), int(y1)),
                (int(x2), int(y2)), 3
            )

        # Center energy core
        pygame.draw.ellipse(
            screen, (5, 17, 37),
            (cx - 65, cy - 31, 130, 62)
        )

        pygame.draw.ellipse(
            screen, (0, 175, 220),
            (cx - 65, cy - 31, 130, 62), 2
        )

        pygame.draw.circle(
            screen, (0, 220, 255),
            (cx, cy), int(9 + pulse * 4)
        )

        pygame.draw.circle(
            screen, (220, 250, 255),
            (cx, cy), 3
        )

        # Energy rays
        for i in range(8):
            angle = rotation * 1.4 + i * math.tau / 8

            x1 = cx + math.cos(angle) * 125
            y1 = cy + math.sin(angle) * 72

            x2 = cx + math.cos(angle) * 142
            y2 = cy + math.sin(angle) * 83

            pygame.draw.line(
                screen, (0, 105, 165),
                (int(x1), int(y1)),
                (int(x2), int(y2)), 2
            )

    def draw_title(self, screen):
        cx = WIDTH // 2

        # Brand label
        brand = self.small_font.render(
            "E L S I L E N T O   S T U D I O",
            True, (105, 155, 185)
        )

        screen.blit(
            brand,
            brand.get_rect(center=(cx, 65))
        )

        # Main title
        title = self.title_font.render(
            "ELSILENTO", True, (245, 250, 255)
        )

        title_rect = title.get_rect(center=(cx, 130))

        shadow = self.title_font.render(
            "ELSILENTO", True, (0, 155, 220)
        )

        shadow.set_alpha(100)

        screen.blit(shadow, title_rect.move(0, 4))
        screen.blit(title, title_rect)

        drop = self.drop_font.render(
            "DROP", True, (0, 215, 255)
        )

        screen.blit(
            drop,
            drop.get_rect(center=(cx, 184))
        )

        subtitle = self.small_font.render(
            "ONE FALL. ONE CHANCE. SURVIVE.",
            True, (135, 165, 195)
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(center=(cx, 225))
        )

        # Small separator
        pygame.draw.line(
            screen, (0, 170, 215),
            (cx - 45, 245), (cx + 45, 245), 2
        )

    def draw_button(self, screen, text, rect, primary=False):
        hovered = rect.collidepoint(pygame.mouse.get_pos())

        if primary:
            bg = (7, 62, 88) if hovered else (5, 39, 60)
            border = (0, 235, 255) if hovered else (0, 170, 220)
            text_color = (255, 255, 255)
            accent = (0, 220, 255)
        else:
            bg = (20, 30, 54) if hovered else (11, 18, 36)
            border = (0, 170, 210) if hovered else (42, 68, 100)
            text_color = (245, 250, 255) if hovered else (170, 195, 220)
            accent = (0, 180, 220)

        # Shadow
        shadow = rect.move(0, 4)

        pygame.draw.rect(
            screen, (1, 3, 10),
            shadow, border_radius=10
        )

        # Button body
        pygame.draw.rect(
            screen, bg,
            rect, border_radius=10
        )

        pygame.draw.rect(
            screen, border,
            rect, 2, border_radius=10
        )

        # Left neon stripe
        pygame.draw.rect(
            screen, accent,
            (rect.left + 2, rect.top + 9, 3, rect.height - 18),
            border_radius=2
        )

        # Text
        label = self.button_font.render(
            text, True, text_color
        )

        screen.blit(
            label,
            label.get_rect(center=rect.center)
        )

        # Right indicator
        pygame.draw.circle(
            screen,
            accent if hovered or primary else (65, 95, 125),
            (rect.right - 18, rect.centery),
            3
        )

    def draw_settings(self, screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((2, 4, 14, 238))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(28, 220, WIDTH - 56, 340)

        pygame.draw.rect(
            screen, (10, 19, 39),
            panel, border_radius=20
        )

        pygame.draw.rect(
            screen, (0, 190, 230),
            panel, 2, border_radius=20
        )

        title = self.title_font.render(
            "SETTINGS", True, (0, 220, 255)
        )

        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, 290))
        )

        info = self.small_font.render(
            "MORE OPTIONS COMING SOON",
            True, (145, 175, 200)
        )

        screen.blit(
            info,
            info.get_rect(center=(WIDTH // 2, 370))
        )

        note = self.tiny_font.render(
            "YOUR GAME EXPERIENCE WILL BE CUSTOMIZABLE",
            True, (90, 120, 155)
        )

        screen.blit(
            note,
            note.get_rect(center=(WIDTH // 2, 410))
        )

        self.draw_button(
            screen, "BACK",
            self.back_button, True
        )

    def draw(self, screen):
        self.draw_background(screen)

        if self.settings_open:
            self.draw_settings(screen)
            return

        self.draw_title(screen)
        self.draw_portal(screen)

        # Menu panel
        panel = pygame.Rect(54, 440, WIDTH - 108, 258)

        pygame.draw.rect(
            screen, (5, 11, 25),
            panel, border_radius=18
        )

        pygame.draw.rect(
            screen, (35, 65, 95),
            panel, 1, border_radius=18
        )

        # Panel heading
        heading = self.tiny_font.render(
            "MAIN MENU",
            True, (95, 145, 175)
        )

        screen.blit(
            heading,
            heading.get_rect(center=(WIDTH // 2, 447))
        )

        for name, rect in self.buttons.items():
            self.draw_button(
                screen,
                name,
                rect,
                primary=(name == "PLAY")
            )

        # Footer
        footer = self.tiny_font.render(
            "ELSILENTO DROP  |  VERSION 1.0",
            True, (85, 110, 145)
        )

        screen.blit(
            footer,
            footer.get_rect(center=(WIDTH // 2, 755))
        )

        hint = self.tiny_font.render(
            "PRESS ENTER TO PLAY",
            True, (65, 95, 125)
        )

        screen.blit(
            hint,
            hint.get_rect(center=(WIDTH // 2, 775))
        )
