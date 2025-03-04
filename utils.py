# utils.py

import os
import json
import pygame
import requests
from io import BytesIO

# Constants
DATA_DIR = "data"
SPRITE_DIR = os.path.join(DATA_DIR, "sprites")
POKEMON_FILE = os.path.join(DATA_DIR, "pokemon.json")

# Manually define the three Pokémon (Carapuce, Salamèche, Bulbizarre)
pokemon_choices = [
    {"name": "Bulbizarre", "id": 1, "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"},
    {"name": "Salamèche", "id": 4, "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"},
    {"name": "Carapuce", "id": 7, "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png"}
]

# Fetch Pokémon from API (Fallback to Local Data)
def fetch_pokemon():
    api_url = "https://pokebuildapi.fr/api/v1/pokemon/generation/1"
    
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            with open(POKEMON_FILE, "w") as f:
                json.dump(data, f, indent=4)
            return data
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching Pokémon data online: {e}")

    return load_pokemon()

# Load Pokémon Data Locally
def load_pokemon():
    if not os.path.exists(POKEMON_FILE):
        print("❌ No Pokémon data found locally. Run online fetch first.")
        return []
    with open(POKEMON_FILE, "r") as f:
        return json.load(f)

# Load sprite (URL first, fallback to local file)
def load_sprite(pokemon):
    if type(pokemon) is dict:
        sprite_url = pokemon.get("sprite")
        local_sprite_path = os.path.join(SPRITE_DIR, f"{pokemon['id']}.png")

    else:
        sprite_url = pokemon.sprite_url
        local_sprite_path = os.path.join(SPRITE_DIR, f"{pokemon.id}.png")

    if sprite_url and sprite_url.startswith("http"):
        try:
            response = requests.get(sprite_url, timeout=5)
            if response.status_code == 200:
                return pygame.image.load(BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Error loading {pokemon['name']} sprite from URL: {e}")

    if os.path.exists(local_sprite_path):
        return pygame.image.load(local_sprite_path)

    print(f"❌ Sprite not found for {pokemon['name']}")
    return None
