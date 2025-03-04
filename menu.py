import pygame
from settings import *
from pokedex import pokedex
from save_manager import load_save

# Load background and icons
background = pygame.image.load('assets/images/background/menu_bis.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
play_icon = pygame.image.load('assets/images/icons/play.png')
pokedex_icon = pygame.image.load('assets/images/icons/pokedex.png')
quit_icon = pygame.image.load('assets/images/icons/quit.png')

class Menu:
    def __init__(self, player_name):
        self.options = [
            play_icon,
            pokedex_icon,
            quit_icon
        ]
        self.player_name = player_name 
        self.button_rects = []
        self.positions = [
            (500, 400),  # Play button position
            (700, 400),  # Pokédex button position
            (900, 400)   # Quit button position
        ]

    def draw(self):
        screen.blit(background, (0, 0))
        self.button_rects.clear()
        
        for i, icon in enumerate(self.options):
            icon = pygame.transform.scale(icon, (100, 100))
            icon_rect = icon.get_rect(center=self.positions[i])
            screen.blit(icon, icon_rect)
            self.button_rects.append(icon_rect)
        
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, icon_rect in enumerate(self.button_rects):
                if icon_rect.collidepoint(mouse_pos):
                    if i == 1:  # View Pokédex
                        pokedex(self.player_name)
                        return None  # Prevent immediate return to menu
                    return i
        return None
