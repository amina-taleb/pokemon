#game

import pygame
import random
from utils import load_sprite, fetch_pokemon, pokemon_choices
from settings import *
from battle import battle
from menu import Menu
from pokedex import pokedex
from players import get_player_name  
from save_manager import load_save, save_game, get_player_pokemon,get_player_level, update_pokedex_encounter
from pokemon import Pokemon
from gif import load_gif_frames
import math

pygame.init()

#Load background 
start_screen_bg = pygame.image.load("assets/images/background/loading.jpg")
start_screen_bg = pygame.transform.scale(start_screen_bg, (WIDTH, HEIGHT))
name_bg = pygame.image.load('assets/images/background/name.jpg')
name_bg = pygame.transform.scale(start_screen_bg, (WIDTH, HEIGHT))
select_bg = pygame.image.load('assets/images/background/choose.jpg')
select_bg= pygame.transform.scale(select_bg, (WIDTH, HEIGHT))
map_bg = pygame.image.load('assets/images/background/map.jpg')
map_bg = pygame.transform.scale(map_bg, (WIDTH, HEIGHT))

#load GIF frames
loading_frames = load_gif_frames("assets/images/gif/loading")

#load sounds :
sound_loading = pygame.mixer.Sound('assets/sounds/loading.mp3')
sound_start = pygame.mixer.Sound('assets/sounds/start.mp3')
sound_Battle = pygame.mixer.Sound('assets/sounds/battle.wav')
sound_Attack = pygame.mixer.Sound('assets/sounds/attack.wav')
sound_Victory = pygame.mixer.Sound('assets/sounds/victory.wav')

sound_loading.play()
def loading_screen():
    frame_index = 0
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.blit(start_screen_bg, (0, 0))

        # Display text "Loading..."
        loading_text = font.render("Loading...", True, WHITE)
        screen.blit(loading_text, (620, 700))

        # Display animation gif
        screen.blit(loading_frames[frame_index], (600, 730))
        frame_index = (frame_index + 1) % len(loading_frames)  # Change frame

        pygame.display.flip()
        clock.tick(10)  # speed (~10 FPS)

        # Stop after 3 seconds
        if pygame.time.get_ticks() - start_time > 3000:
            running = False

        # Handle events (close window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    sound_loading.stop()

sound_start.play()
def select_pokemon(player_name, pokemon_choices):
    """Handles Pokémon selection."""
    global player_pokemon
    current_index = 0
    running = True

    # Get all available Pokémon (initial + won Pokémon)
    available_pokemon = get_player_pokemon(player_name, pokemon_choices)
    float_offset = 0  # Initial offset for floating effect

    while running:
        screen.blit(select_bg, (0, 0))
        draw_text("Select Your Pokémon", WIDTH // 2, 50)

        # Show current Pokémon selection
        pokemon = available_pokemon[current_index]
        sprite = load_sprite(pokemon)

        if sprite:
            sprite = pygame.transform.scale(sprite, (300, 300))
            screen.blit(sprite, (WIDTH // 2 - 100, HEIGHT // 2 - 100 + float_offset))  # Apply floating effect

        # Display Pokémon info
        draw_text(f"{pokemon['name']} (#{pokemon['id']})", WIDTH // 2, HEIGHT // 2 + 120)
        draw_text("← / → : Navigate  |  ENTER : Select  |  ESC : Back", WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()

        # Update the floating effect
        float_offset = 10 * math.sin(pygame.time.get_ticks() / 500)  # Use math.sin instead of pygame.math.sin

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_index = (current_index + 1) % len(available_pokemon)
                elif event.key == pygame.K_LEFT:
                    current_index = (current_index - 1) % len(available_pokemon)
                elif event.key == pygame.K_RETURN:
                    player_pokemon = pokemon  # Set the selected Pokémon as player's Pokémon
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

    return player_pokemon

def intro_battle_screen(player_pokemon, enemy_pokemon):
    """Show an introduction screen with both Pokémon before the battle."""
    screen.fill(WHITE)  
    draw_text("Get ready for battle!", WIDTH // 2, HEIGHT // 2 - 200)
    draw_text("Use arrow keys to move your Pokémon", WIDTH // 2, HEIGHT // 2 + 150)
    draw_text("Press ENTER to start the battle", WIDTH // 2, HEIGHT // 2 + 200)

    # Load sprites for both Pokémon
    player_sprite = load_sprite(player_pokemon)
    player_sprite = pygame.transform.scale(player_sprite, (100, 100))
    enemy_sprite = load_sprite(enemy_pokemon)
    enemy_sprite = pygame.transform.scale(enemy_sprite, (100, 100))

    # Set initial positions
    player_x = WIDTH // 2 - 75
    player_y = HEIGHT // 2 + 300
    enemy_x = WIDTH // 2 
    enemy_y = HEIGHT // 2 - 75

    float_offset_player = 0
    float_offset_enemy = 0

    # Set movement speed (Reduced for slower movement)
    player_speed = 2  

    # Pygame clock for frame rate control
    clock = pygame.time.Clock()

    # Animation loop
    running = True
    while running:
        screen.blit(map_bg, (0, 0))

        # Draw Pokémon sprites
        screen.blit(player_sprite, (player_x, player_y + float_offset_player))
        screen.blit(enemy_sprite, (enemy_x, enemy_y + float_offset_enemy))

        # Floating effect
        float_offset_player = 5 * math.sin(pygame.time.get_ticks() / 500)
        float_offset_enemy = 5 * math.sin(pygame.time.get_ticks() / 500 + 3.14)  

        # Display introductory text
        draw_text("Get ready for battle!", WIDTH // 2, HEIGHT // 2 - 200)
        draw_text("Use arrow keys to move your Pokémon", WIDTH // 2, HEIGHT // 2 + 150)
        draw_text("Press ENTER to start the battle", WIDTH // 2, HEIGHT // 2 + 200)

        pygame.display.flip()

        # Get all pressed keys
        keys = pygame.key.get_pressed()

        # Movement control for player Pokémon (Slower movement)
        if keys[pygame.K_LEFT]:
            player_x -= player_speed  
        if keys[pygame.K_RIGHT]:
            player_x += player_speed  
        if keys[pygame.K_UP]:
            player_y -= player_speed  
        if keys[pygame.K_DOWN]:
            player_y += player_speed  

        # Check if player is close enough and press Enter
        if keys[pygame.K_RETURN] and abs(player_x - enemy_x) < 100 and abs(player_y - enemy_y) < 100:
            running = False  # Exit to start the battle

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Limit the frame rate to 60 FPS for smooth movement
        clock.tick(60)

    # Proceed to the battle
    return player_pokemon, enemy_pokemon


# Main Game Loop
def start_game():
    # Loading screen
    loading_screen()

    # Get player name screen
    player_name = get_player_name()

    # Select Pokémon screen
    pokemon_list = fetch_pokemon()

    player_level = get_player_level(player_name)

    # Load existing save if available
    saved_data = load_save(player_name)
    if player_name in saved_data:
        saved_pokemon_list = saved_data[player_name].get("pokemon_won", [])
        if saved_pokemon_list:
            saved_pokemon = saved_pokemon_list[-1]  # Get the last Pokémon the player won
            print(f"✅ Loaded {player_name}'s profile!")
            if isinstance(saved_pokemon, dict):
                print(f"Saved Pokémon Name: {saved_pokemon['name']}")
            else:
                print("Error: The saved Pokémon format is incorrect.")
        else:
            saved_pokemon = None

    menu = Menu(player_name)
    option = None

    while option != 2:
        menu.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            option = menu.handle_event(event)

            if option == 1:
                pokedex()  # Display Pokedex
            elif option == 0:
                available_pokemon = get_player_pokemon(player_name, pokemon_list)
                player_pokemon = select_pokemon(player_name, pokemon_list)
                sound_start.stop()
                # Load and create the playable player Pokémon
                for pokemon in pokemon_list: 
                    if pokemon.get('id') == player_pokemon.get('id'):
                        playable_player_pokemon = Pokemon(
                            pokemon.get('id'), pokemon.get('name'), pokemon.get('sprite'),
                            pokemon.get('stats'), pokemon.get('apiTypes'), pokemon.get('apiResistances')
                        )

                # Keep battling until the player loses
                while True:
                    # Generate a random enemy Pokémon
                    enemy_id = random.randint(1, 150)
                    enemy_pokemon_data = next((p for p in pokemon_list if p["id"] == enemy_id), None)

                    if not enemy_pokemon_data:
                        print("⚠️ Error: Could not find enemy Pokémon!")
                        break

                    playable_enemy_pokemon = Pokemon(
                        enemy_pokemon_data.get('id'), enemy_pokemon_data.get('name'), enemy_pokemon_data.get('sprite'),
                        enemy_pokemon_data.get('stats'), enemy_pokemon_data.get('apiTypes'), enemy_pokemon_data.get('apiResistances')
                    )

                    # Show intro battle screen before each fight
                    player_pokemon, enemy_pokemon = intro_battle_screen(playable_player_pokemon, playable_enemy_pokemon)

                    # Start battle
                    winner = battle(playable_player_pokemon, [enemy_pokemon], player_name, playable_player_pokemon, playable_enemy_pokemon)

                    if winner == playable_player_pokemon:
                        print(f"🎉 {player_name} won with {playable_player_pokemon.name}!")
                        sound_Battle.stop()
                        sound_Victory.play()

                        # Save defeated Pokémon
                        save_game(player_name, enemy_pokemon_data["name"], player_level)

                    else:
                        print(f"💥 {player_name} lost with {playable_player_pokemon.name}!")
                        break  # Stop if the player loses

    pygame.quit()


