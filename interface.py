
import pygame
from settings import *


class Interface:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 25, bold=True)
        self.big_font = pygame.font.SysFont("arial", 43, bold=True)
        self.score_font = pygame.font.SysFont("arial", 29, bold=True)
        self.small_font = pygame.font.SysFont("arial", 13, bold=True)
        self.button_font = pygame.font.SysFont("arial", 17, bold=True)

        self.restart_button = pygame.Rect(
            WIDTH // 2 - 112, 510, 224, 56
        )
        self.menu_button = pygame.Rect(
            WIDTH // 2 - 112, 580, 224, 56
        )

        self.home_game_button = pygame.Rect(WIDTH - 88, 15, 34, 34)
        self.pause_button = pygame.Rect(WIDTH - 45, 15, 34, 34)

        self.resume_button = pygame.Rect(
            WIDTH // 2 - 112, 450, 224, 56
        )
        self.pause_home_button = pygame.Rect(
            WIDTH // 2 - 112, 520, 224, 56
        )

    def text(self, screen, message, font, color, y):
        image = font.render(str(message), True, color)
        rect = image.get_rect(center=(WIDTH // 2, y))
        screen.blit(image, rect)

    def draw_panel(self, screen, rect, border=(35, 65, 95)):
        pygame.draw.rect(
            screen, (10, 16, 31), rect, border_radius=18
        )
        pygame.draw.rect(
            screen, border, rect, 1, border_radius=18
        )

    def draw_button(self, screen, text, rect, color):
        hovered = rect.collidepoint(pygame.mouse.get_pos())

        bg = (20, 53, 75) if hovered else (13, 24, 42)
        border = color if hovered else (48, 75, 105)
        text_color = (255, 255, 255) if hovered else (205, 220, 240)

        pygame.draw.rect(
            screen, (3, 5, 13), rect.move(0, 4),
            border_radius=12
        )
        pygame.draw.rect(screen, bg, rect, border_radius=12)
        pygame.draw.rect(
            screen, border, rect, 2, border_radius=12
        )

        label = self.button_font.render(
            text, True, text_color
        )
        screen.blit(label, label.get_rect(center=rect.center))

    def draw_icon_button(self, screen, rect, icon, color):
        hovered = rect.collidepoint(pygame.mouse.get_pos())

        bg = (22, 46, 67) if hovered else (10, 18, 34)
        border = color if hovered else (42, 70, 100)

        pygame.draw.rect(screen, bg, rect, border_radius=10)
        pygame.draw.rect(screen, border, rect, 1, border_radius=10)

        cx, cy = rect.center

        if icon == "pause":
            pygame.draw.rect(
                screen, color, (cx - 6, cy - 7, 4, 14),
                border_radius=1
            )
            pygame.draw.rect(
                screen, color, (cx + 2, cy - 7, 4, 14),
                border_radius=1
            )

        elif icon == "home":
            pygame.draw.polygon(
                screen, color,
                [
                    (cx - 9, cy),
                    (cx, cy - 9),
                    (cx + 9, cy),
                    (cx + 7, cy + 2),
                    (cx - 7, cy + 2)
                ]
            )
            pygame.draw.rect(
                screen, color,
                (cx - 6, cy + 1, 12, 8),
                border_radius=1
            )
            pygame.draw.rect(
                screen, bg, (cx - 1, cy + 4, 3, 5)
            )

    def draw_hud(self, screen, score, best):
        # Compact score card at the top
        card = pygame.Rect(WIDTH // 2 - 48, 12, 96, 55)

        pygame.draw.rect(
            screen, (9, 17, 31), card, border_radius=12
        )
        pygame.draw.rect(
            screen, (0, 115, 150), card, 1, border_radius=12
        )

        label = self.small_font.render(
            "SCORE", True, (105, 150, 180)
        )
        screen.blit(
            label, label.get_rect(center=(WIDTH // 2, 23))
        )

        score_image = self.score_font.render(
            str(score), True, (240, 250, 255)
        )
        screen.blit(
            score_image,
            score_image.get_rect(center=(WIDTH // 2, 46))
        )

        # Best score on the left
        best_text = self.small_font.render(
            f"BEST {best}", True, CYAN
        )
        screen.blit(best_text, (12, 29))

        # Controls on the right
        self.draw_icon_button(
            screen, self.home_game_button, "home", PURPLE
        )
        self.draw_icon_button(
            screen, self.pause_button, "pause", CYAN
        )

    def draw_menu(self, screen):
        self.text(screen, "ELSILENTO", self.big_font, CYAN, 300)
        self.text(screen, "DROP", self.big_font, PURPLE, 365)
        self.text(screen, "TAP TO START", self.font, WHITE, 480)

    def draw_pause(self, screen):
        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((3, 5, 15, 220))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(35, 315, WIDTH - 70, 300)
        self.draw_panel(screen, panel, (0, 155, 195))

        self.text(screen, "PAUSED", self.big_font, CYAN, 375)

        subtitle = self.small_font.render(
            "TAKE A BREATH", True, (125, 150, 180)
        )
        screen.blit(
            subtitle,
            subtitle.get_rect(center=(WIDTH // 2, 410))
        )

        self.draw_button(
            screen, "RESUME", self.resume_button, CYAN
        )
        self.draw_button(
            screen, "MAIN MENU", self.pause_home_button, PURPLE
        )

    def draw_game_over(self, screen, score, best):
        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((3, 5, 15, 225))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(35, 235, WIDTH - 70, 430)
        self.draw_panel(screen, panel, (135, 55, 85))

        self.text(screen, "GAME OVER", self.big_font, RED, 295)

        score_label = self.small_font.render(
            "YOUR SCORE", True, (130, 150, 175)
        )
        screen.blit(
            score_label,
            score_label.get_rect(center=(WIDTH // 2, 355))
        )

        self.text(screen, score, self.score_font, WHITE, 400)

        best_label = self.small_font.render(
            f"PERSONAL BEST  {best}", True, CYAN
        )
        screen.blit(
            best_label,
            best_label.get_rect(center=(WIDTH // 2, 450))
        )

        self.draw_button(
            screen, "PLAY AGAIN", self.restart_button, CYAN
        )
        self.draw_button(
            screen, "MAIN MENU", self.menu_button, PURPLE
        )
