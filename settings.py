#settings 

import pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Battle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font setup
font = pygame.font.Font("assets/fonts/pokemon.ttf", 50)

#constants
current_index = 0
player_pokemon = None
enemy_pokemon = None

# Asset paths
IMAGE_PATH = "assets/images/"
SOUND_PATH = "assets/sounds/"

#Display text
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y))