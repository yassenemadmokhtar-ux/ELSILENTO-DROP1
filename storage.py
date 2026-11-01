
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILE_NAME = os.path.join(BASE_DIR, "best_score.txt")
BALL_FILE = os.path.join(BASE_DIR, "selected_ball.txt")
BACKGROUND_FILE = os.path.join(BASE_DIR, "selected_background.txt")
GATE_FILE = os.path.join(BASE_DIR, "selected_gate.txt")

DEFAULT_BALL = "ball.png"
DEFAULT_BACKGROUND = "bg_space.png"
DEFAULT_GATE = "CYBER CORE.png"

AVAILABLE_BALLS = [
    "ball.png",
    "ball_inferno.png",
    "ball_void.png",
    "ball_divine.png",
    "ball_frostbite.png"
]

AVAILABLE_BACKGROUNDS = [
    "bg_space.png",
    "bg_city.png",
    "bg_void.png",
    "bg_inferno.png",
    "bg_ice.png"
]

AVAILABLE_GATES = [
    "CYBER CORE.png",
    "DIVINE AEGIS.png",
    "FROST GUARD.png",
    "INFERNO TITAN.png",
    "VOID REACTOR.png"
]


def load_best():
    try:
        with open(FILE_NAME, "r") as file:
            return int(file.read().strip() or 0)
    except:
        return 0


def save_best(score):
    with open(FILE_NAME, "w") as file:
        file.write(str(score))


def load_selected_ball():
    try:
        with open(BALL_FILE, "r") as file:
            selected = file.read().strip()

        if selected in AVAILABLE_BALLS:
            if os.path.exists(os.path.join(BASE_DIR, selected)):
                return selected
    except:
        pass

    return DEFAULT_BALL


def save_selected_ball(filename):
    if filename not in AVAILABLE_BALLS:
        return

    if not os.path.exists(os.path.join(BASE_DIR, filename)):
        return

    with open(BALL_FILE, "w") as file:
        file.write(filename)


def load_selected_background():
    try:
        with open(BACKGROUND_FILE, "r") as file:
            selected = file.read().strip()

        if selected in AVAILABLE_BACKGROUNDS:
            if os.path.exists(os.path.join(BASE_DIR, selected)):
                return selected
    except:
        pass

    if os.path.exists(os.path.join(BASE_DIR, DEFAULT_BACKGROUND)):
        return DEFAULT_BACKGROUND

    return None


def save_selected_background(filename):
    if filename not in AVAILABLE_BACKGROUNDS:
        return

    if not os.path.exists(os.path.join(BASE_DIR, filename)):
        return

    with open(BACKGROUND_FILE, "w") as file:
        file.write(filename)


def load_selected_gate():
    try:
        with open(GATE_FILE, "r") as file:
            selected = file.read().strip()

        if selected in AVAILABLE_GATES:
            if os.path.exists(os.path.join(BASE_DIR, selected)):
                return selected
    except:
        pass

    return DEFAULT_GATE


def save_selected_gate(filename):
    if filename not in AVAILABLE_GATES:
        return

    if not os.path.exists(os.path.join(BASE_DIR, filename)):
        return

    with open(GATE_FILE, "w") as file:
        file.write(filename)
