import pygame
import json
from settings import *
from utils import fetch_pokemon, load_sprite, pokemon_choices
from save_manager import load_save, save_game

#Load background 
background = pygame.image.load("assets/images/background/poke.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def load_encounter_data():
    save_data = load_save()
    return save_data.get("encountered_pokemon", {})

def save_encounter_data(encounter_data):
    save_data = load_save()
    save_data["encountered_pokemon"] = encounter_data
    with open("save_data.json", "w") as file:
        json.dump(save_data, file, indent=4)

def display_pokemon_info(pokemon, player_name):

    save_data = load_save()

    # ✅ Vérifier si le joueur existe
    if player_name not in save_data:
        print(f"⚠ Erreur : Joueur {player_name} introuvable.")
        return

    # ✅ Récupérer les Pokémon gagnés et vérifier si le Pokémon est un starter
    won_pokemon = {str(p['id']) for p in save_data[player_name].get("pokemon_won", [])}
    pokemon_id = str(pokemon['id'])
    is_starter = any(starter["id"] == int(pokemon_id) for starter in pokemon_choices)

    screen.blit(background, (0, 0))

    if pokemon_id in won_pokemon or is_starter:
        # ✅ Affichage complet si Pokémon gagné ou starter
        draw_text("Pokémon Info", WIDTH // 2, 50)

        sprite = load_sprite(pokemon)
        if sprite:
            sprite = pygame.transform.scale(sprite, (200, 200))
            screen.blit(sprite, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

        draw_text(f"{pokemon['name']} (#{pokemon['id']})", WIDTH // 2, HEIGHT // 2 + 120)
        draw_text(f"Type: {', '.join([t['name'] for t in pokemon['apiTypes']])}", WIDTH // 2, HEIGHT // 2 + 150)
        draw_text(f"HP: {pokemon['stats']['HP']} | ATK: {pokemon['stats']['attack']} | DEF: {pokemon['stats']['defense']}", WIDTH // 2, HEIGHT // 2 + 180)
    else:
        # ✅ Message si Pokémon non encore gagné
        draw_text("Ce Pokémon est encore inconnu...", WIDTH // 2, HEIGHT // 2)

    draw_text("Press ESC to return", WIDTH // 2, HEIGHT - 50)
    pygame.display.flip()

    # ✅ Attente que le joueur ferme l'interface
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def pokedex(player_name):
    save_data = load_save()

    # ✅ Vérifier si le joueur existe
    if player_name not in save_data:
        print(f"⚠ Erreur : Joueur {player_name} introuvable dans la sauvegarde.")
        return

    # ✅ Récupération des Pokémon rencontrés et gagnés
    encountered_pokemon = save_data[player_name].get("encountered_pokemon", {})
    won_pokemon = {str(p['id']) for p in save_data[player_name].get("pokemon_won", [])}
    pokemon_list = fetch_pokemon()

    # ✅ Ajout automatique des starters comme Pokémon visibles
    for starter in pokemon_choices:
        won_pokemon.add(str(starter["id"]))

    current_index = 0
    running = True

    while running:
        screen.blit(background, (0, 0))
        draw_text("Pokédex", WIDTH // 2, 50)

        if pokemon_list:
            pokemon = pokemon_list[current_index]
            pokemon_id = str(pokemon['id'])
            encounters = encountered_pokemon.get(pokemon_id, 0)

            # ✅ Afficher le nom si gagné ou si c'est un starter, sinon juste l'ID
            if pokemon_id in won_pokemon:
                sprite = load_sprite(pokemon)
                if sprite:
                    sprite = pygame.transform.scale(sprite, (200, 200))
                    screen.blit(sprite, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
                
                draw_text(f"{pokemon['name']} (#{pokemon['id']})", WIDTH // 2, HEIGHT // 2 + 120)
            else:
                draw_text(f"??? (#{pokemon['id']})", WIDTH // 2, HEIGHT // 2 + 120)

            # ✅ Toujours afficher le nombre de fois rencontré
            draw_text(f"Rencontré: {encounters} fois", WIDTH // 2, HEIGHT // 2 + 150)

        draw_text("← / → : Naviguer  |  ESC : Quitter  |  ENTER : Voir Infos", WIDTH // 2, HEIGHT - 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    current_index = (current_index + 1) % len(pokemon_list)
                elif event.key == pygame.K_LEFT:
                    current_index = (current_index - 1) % len(pokemon_list)
                elif event.key == pygame.K_RETURN:
                    display_pokemon_info(pokemon, player_name)

    return None