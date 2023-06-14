from pygame.math import Vector2

# Definicion de parametros:
## screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
TITLE_SIZE = 64

# overlay positions
OVERLAY_POSITIONS = {
    'tool' : (40, SCREEN_HEIGHT-15),
    'seed' : (80, SCREEN_HEIGHT-5)
}

"""Orden en el que se sobrepondran las cosas"""
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
}
