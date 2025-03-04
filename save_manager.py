import json
from utils import fetch_pokemon

def load_save(player_name=None):
    try:
        with open("save_data.json", "r") as file:
            saved_data = json.load(file)
    except FileNotFoundError:
        saved_data = {}

    if player_name and player_name not in saved_data:
        print(f"👤 Nouveau joueur détecté : {player_name}. Création du profil...")
        saved_data[player_name] = {
            "pokemon_won": [],
            "level": 1,
            "encountered_pokemon": {}
        }
        with open("save_data.json", "w") as file:
            json.dump(saved_data, file, indent=4)

    return saved_data


def save_game(player_name, defeated_pokemon_name, player_level):
    saved_data = load_save()

    if player_name not in saved_data:
        saved_data[player_name] = {
            "pokemon_won": [],
            "level": player_level,
            "encountered_pokemon": {}
        }

    if "encountered_pokemon" not in saved_data[player_name]:
        saved_data[player_name]["encountered_pokemon"] = {}

    pokemon_id = get_pokemon_id_by_name(defeated_pokemon_name)
    if pokemon_id is None:
        print(f"⚠ Erreur : Impossible de trouver l'ID de {defeated_pokemon_name}")
        return  

    if not any(p["id"] == pokemon_id for p in saved_data[player_name]["pokemon_won"]):
        saved_data[player_name]["pokemon_won"].append({"name": defeated_pokemon_name, "id": pokemon_id})

    saved_data[player_name]["level"] = player_level

    with open("save_data.json", "w") as file:
        json.dump(saved_data, file, indent=4)

    print(f"✅ {defeated_pokemon_name} a été ajouté aux Pokémon gagnés de {player_name} !")


# ✅ Mise à jour des Pokémon rencontrés (déplacée ici depuis `pokedex.py`)
def update_pokedex_encounter(player_name, pokemon_id):
    saved_data = load_save()

    if player_name not in saved_data:
        saved_data[player_name] = {
            "pokemon_won": [],
            "level": 1,
            "encountered_pokemon": {}
        }

    if "encountered_pokemon" not in saved_data[player_name]:
        saved_data[player_name]["encountered_pokemon"] = {}

    if str(pokemon_id) not in saved_data[player_name]["encountered_pokemon"]:
        saved_data[player_name]["encountered_pokemon"][str(pokemon_id)] = 0

    saved_data[player_name]["encountered_pokemon"][str(pokemon_id)] += 1

    with open("save_data.json", "w") as file:
        json.dump(saved_data, file, indent=4)

# ✅ Fonction pour obtenir un ID de Pokémon par son nom
def get_pokemon_id_by_name(name):
    pokemon_list = fetch_pokemon()
    for pokemon in pokemon_list:
        if pokemon['name'].lower() == name.lower():
            return pokemon['id']
    return None

# ✅ Récupérer les Pokémon du joueur
def get_player_pokemon(player_name, pokemon_choices):
    saved_data = load_save()
    if player_name in saved_data:
        return pokemon_choices[:3] + saved_data[player_name].get("pokemon_won", [])
    else:
        return pokemon_choices[:3]

# ✅ Récupérer le niveau du joueur
def get_player_level(player_name):
    saved_data = load_save()
    return saved_data[player_name].get("level", 0) if player_name in saved_data else 0
