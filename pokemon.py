import json
import pygame
import random

class Pokemon:
    def __init__(self, id, name, sprite_url, stats, types, resistances, evolution=None):
        self.id = id
        self.name = name
        self.sprite_url = sprite_url
        self.stats = stats
        self.max_hp = stats.get("HP")
        self.types = [t["name"] for t in types] if types else []  
        self.resistances = resistances
        self.evolution = evolution  # Liste des évolutions possibles

        self.normal_attack = {"name" : "Attaque normale",
           "strenght" : 20,
           "type" : "Normal",
           "accuracy" : 80}
        self.special_attack = {"name" : "Attaque spéciale",
           "strenght" : 35,
            "type": random.choice(self.types) if self.types else "Normal",
           "accuracy" : 60}
        self.image = None  # Sprite de l'image, à charger
        self.xp = 0
        self.level = 1

    def load_sprite(self):
        """ Charge l'image à partir du sprite URL """
        try:
            self.image = pygame.image.load(self.sprite_url)  # Charger l'image via URL ou fichier local
        except Exception as e:
            print(f"Erreur de chargement de l'image : {e}")
            self.image = None

    def gain_xp(self, xp):
        """ Gagne de l'expérience """
        self.xp += xp
        if self.xp >= 100:  # Exemple simple pour le niveau
            self.level_up()

    def level_up(self):
        """ Gère l'évolution du niveau """
        self.level += 1
        self.xp = 0  # Réinitialisation de l'XP après un niveau
        
    def attack_target(self, target, attack):
        if random.randint(1, 100) > attack['accuracy']:
            print(f"{self.name} utilise {attack['name']}, mais l'attaque échoue !")
            return
        
        attack_stat = self.stats['attack']
        defense_stat = target.stats['defense']
        base_damage = ((2 * attack_stat / (defense_stat + 1)) * attack['strenght']) / 2
        
        type_multiplier = 1
        for resistance in target.resistances:
            if resistance['name'] == attack['type']:
                type_multiplier = resistance['damage_multiplier']
                break
        
        final_damage = max(1, int(base_damage * type_multiplier))  # Au minimum 1 PV
        
        target.stats['HP'] -= final_damage
        target.stats['HP'] = max(0, target.stats['HP'])  # Éviter les HP négatifs
        
        print(f"{self.name} utilise {attack['name']} sur {target.name} !")
        print(f"Dégâts infligés : {final_damage} (x{type_multiplier} en fonction des résistances)")
        print(f"HP restants de {target.name} : {target.stats['HP']}")
        if target.stats['HP'] == 0:
            print(target.name, "est K.O")
            
    def use_special_attack(self):
        if self.types:
            self.special_attack["type"] = random.choice(self.types)  # Type aléatoire à chaque utilisation

def load_pokemon_from_json(file_path):
    """ Charge les Pokémon depuis un fichier JSON """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    pokemons = []
    for poke_data in data:
        # Créer un objet Pokemon pour chaque Pokémon
        pokemon = Pokemon(
            id=poke_data["id"],
            name=poke_data["name"],
            sprite_url=poke_data["sprite"],  # URL du sprite à charger
            stats=poke_data["stats"],
            types=[type_info["name"] for type_info in poke_data["apiTypes"]],
            evolution=poke_data.get("apiEvolutions", [])
        )
        pokemons.append(pokemon)

    return pokemons

