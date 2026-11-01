
import pygame
import sys
import os

from settings import *
from ball import Ball
from gates import GateManager
from effects import Effects
from interface import Interface
from storage import (
    load_best,
    save_best,
    load_selected_background
)
from menu import MainMenu
from shop import BallShop


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ELSILENTO DROP")

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ball = Ball()
gates = GateManager()
effects = Effects()
ui = Interface()
menu = MainMenu()
shop = BallShop()

game_background = None

best_score = load_best()
score = 0

state = "menu"
touch_start = None


def load_game_background():
    global game_background

    game_background = None
    filename = load_selected_background()

    if not filename:
        return

    path = os.path.join(BASE_DIR, filename)

    try:
        image = pygame.image.load(path).convert()
        game_background = pygame.transform.smoothscale(
            image, (WIDTH, HEIGHT)
        )
    except (pygame.error, OSError):
        game_background = None
        print("Could not load background:", path)


def reset_game():
    global ball, gates, score, touch_start, effects

    ball = Ball()
    gates = GateManager()
    effects = Effects()

    load_game_background()

    score = 0
    touch_start = None


def finish_game():
    global state, best_score

    state = "gameover"

    if score > best_score:
        best_score = score
        save_best(best_score)


running = True

while running:
    dt = min(clock.tick(FPS) / 1000, 0.03)

    if state == "menu":
        menu.update(dt)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            continue

        if state == "menu":
            action = menu.handle_event(event)

            if action == "play":
                reset_game()
                state = "playing"

            elif action == "shop":
                state = "shop"

            elif action == "exit":
                running = False

        elif state == "shop":
            action = shop.handle_event(event)

            if action == "back":
                state = "menu"

        elif state == "playing":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "paused"
                    touch_start = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = event.pos

                    if ui.pause_button.collidepoint(mouse):
                        state = "paused"
                        touch_start = None

                    elif ui.home_game_button.collidepoint(mouse):
                        state = "menu"
                        touch_start = None

                    else:
                        touch_start = mouse

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and touch_start:
                    touch_end = event.pos
                    ball.launch(touch_start, touch_end)
                    touch_start = None

        elif state == "paused":

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "playing"

                elif event.key == pygame.K_m:
                    state = "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = event.pos

                    if ui.resume_button.collidepoint(mouse):
                        state = "playing"

                    elif ui.pause_home_button.collidepoint(mouse):
                        state = "menu"

        elif state == "gameover":

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = event.pos

                    if ui.restart_button.collidepoint(mouse):
                        reset_game()
                        state = "playing"

                    elif ui.menu_button.collidepoint(mouse):
                        state = "menu"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    state = "playing"

                elif event.key == pygame.K_m:
                    state = "menu"

    if state == "playing":
        effects.update(dt)
        ball.update(dt)

        gained_points, crushed = gates.update(dt, ball)
        score += gained_points

        if crushed:
            finish_game()

    # Draw the selected background only during gameplay screens.
    screen.fill((7, 9, 22))

    if state == "menu":
        menu.draw(screen)

    elif state == "shop":
        shop.draw(screen)

    else:
        if game_background:
            screen.blit(game_background, (0, 0))

        effects.draw(screen)
        gates.draw(screen)

        if state == "playing":
            ball.draw(screen)
            ui.draw_hud(screen, score, best_score)

        elif state == "paused":
            ball.draw(screen)
            ui.draw_pause(screen)

        elif state == "gameover":
            ball.draw(screen)
            ui.draw_game_over(screen, score, best_score)

    pygame.display.flip()


pygame.quit()
sys.exit()
