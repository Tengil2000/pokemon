#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" -----------------------------------------------------------------------
Main objects and functions for creating Pokémon objects.
Begun 2016-07-15 Alexander Karlsson
----------------------------------------------------------------------- """
import csv
import sqlite3
from pokemon_type import PokemonType
from enum import Enum
import matplotlib.pyplot as plt
from numpy import floor, ceil, sqrt

class PokemonClass(Enum):
    """Class (Type) of Pokémon"""
    null     = 1000
    Bug      = 1100
    Dark     = 1110
    Dragon   = 1120
    Electric = 1130
    Fighting = 1140
    Fire     = 1150
    Flying   = 1160
    Ghost    = 1170
    Grass    = 1180
    Ground   = 1190
    Ice      = 1200
    Normal   = 1210
    Poison   = 1220
    Psychic  = 1230
    Rock     = 1240
    Steel    = 1250
    Water    = 1260



class State(Enum):
    """Pokemon state that will affect the result"""
    asleep    = 25
    frozen    = 25
    paralyzed = 12
    burned    = 12
    poisoned  = 12
    normal    = 100


class Pokemon:
    """Pokémon object"""

    def __init__(self, pokemontype, state = State.normal):
        feats = get_pokemon_from_sql(pokemontype)
        # Assign features to Pokémon creature
        if pokemontype != PokemonType.NULL_POKEMON:
            self.pokemontype     = pokemontype
            self.name            = feats[0]                 # Pokemon name e.g. Pikachu
            self.nat             = feats[1]
            
            self.HP              = feats[2]            # Maximum HP
            self.HP_base         = feats[2]            # Base HP, never to be changed
            self.HPcurrent       = feats[2]            # HP decreases as Pokémon gets attacked
            self.HP_IV           = 0
            self.HP_EV           = 0

            self.attack          = feats[3]
            self.attack_base     = feats[3]            # Base Attack value, never to be changed
            self.attack_IV       = 0
            self.attack_EV       = 0
        
            self.defense         = feats[4]
            self.defense_base    = feats[4]            # Base defense value, never to be changed
            self.defense_IV      = 0
            self.defense_EV      = 0
    
            self.sp_attack       = feats[5]
            self.sp_attack_base  = feats[5]            # Base Sp.Attack value, never to be change    
            self.sp_defense      = feats[6]
            self.sp_defense_base = feats[6]            # Base Sp.Defense value, never to be changed
            self.sp_IV           = 0
            self.sp_EV           = 0

            self.speed           = feats[7] 
            self.speed_base      = feats[7]            # Base speed, never to be changed
            self.speed_IV        = 0
            self.speed_EV        = 0
        
            self.total           = feats[8]
            self.total_base      = feats[8]            # Base total, never to be changed
            self.total_IV        = 0
            self.total_EV        = 0
        
            self.class1          = PokemonClass[feats[9]] 
            self.class2          = PokemonClass[feats[10]]  # can be "null" in text
            self.ability1        = feats[11]
            self.ability2        = feats[12]                # can be "null" in text
            self.hidden_ability  = feats[13]                # can be "null" in text
            self.mass_kilo       = feats[14]
            self.mass_lbs        = feats[15]
            self.color           = feats[16]
            self.gender          = feats[17]
            self.catch_rate      = feats[18]

            self.state           = state 
            self.level           = 1


def get_pokemon_from_sql(pokemontpye):
    """Reads data from a sqlite3 database"""
    conn = sqlite3.connect('pokemon/pokemon_sql.db')
    poke_name = pokemontpye.name + "%"

    cursor = conn.execute("SELECT * FROM POKEMON WHERE name LIKE ?", (poke_name,))
    feats = cursor.fetchone()
    conn.close()

    return feats



class PokemonAttribute(Enum):
    natIdxLessThan      = 100
    natIdxEquals        = 101
    natIdxGreaterThan   = 102
    
    hpLessThan          = 300
    hpEquals            = 301
    hpGreaterThan       = 302

    attackLessThan      = 400
    attackEquals        = 401
    attackGreaterThan   = 402

    defenseLessThan     = 500
    defenseEquals       = 501
    defenseGreaterThan  = 502

    spAttackLessThan    = 600
    spAttackEquals      = 601
    spAttackGreaterThan = 602




def find_pokemons_with_attributes(attribute, value):
    """Finds Pokémons with the valid attributes"""
    pokemons = []

    with open('pokemon/pokedex.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for feats in reader:
            natIdx    = float(feats[1])
            hpVal     = int(feats[3])
            attackVal = int(feats[4])
            defense   = int(feats[5])

            tests = {
                    PokemonAttribute.natIdxLessThan.name:     natIdx < value,
                    PokemonAttribute.natIdxEquals.name:       natIdx == value,
                    PokemonAttribute.natIdxGreaterThan.name:  natIdx > value,
                    PokemonAttribute.hpLessThan.name:         hpVal < value,
                    PokemonAttribute.hpEquals.name:           hpVal == value,
                    PokemonAttribute.hpGreaterThan.name:      hpVal > value,
                    PokemonAttribute.attackLessThan.name:     attackVal < value,
                    PokemonAttribute.attackEquals.name:       attackVal == value,
                    PokemonAttribute.attackGreaterThan.name:  attackVal > value,
                    PokemonAttribute.defenseLessThan.name:    defense < value,
                    PokemonAttribute.defenseEquals.name:      defense == value,
                    PokemonAttribute.defenseGreaterThan.name: defense > value,
                    }
            
            if tests[attribute.name]:
                pokemons.append(Pokemon(PokemonType(natIdx), State.normal))

    return pokemons



def find_pokemons_by_class(class_type):
    """Returns one or several pokemons by PokemonClass"""
    pokemons = []

    conn = sqlite3.connect('pokemon/pokemon_sql.db')
    name = class_type.name

    cursor = conn.execute("SELECT * FROM POKEMON WHERE class1 LIKE ?", (name,))
    for row in cursor:
        pokemons.append(Pokemon(PokemonType(row[1])))

    cursor = conn.execute("SELECT * FROM POKEMON WHERE class2 LIKE ?", (name,))
    for row in cursor:
        pokemons.append(Pokemon(PokemonType(row[2])))

    conn.close()

    return pokemons



def update_pokemon_gen2(poke):
    """Updates a pokemon with skill points, valid formulas up to generation 2"""
    p = poke

    def formula(base, iv, ev, level):
        return floor((2*(base + iv) + floor(ceil(sqrt(ev))/4))*level/100) + 5

    # Calculate total HP
    hp = floor(((2*(p.HP_base + p.HP_IV) + 
        floor(ceil(sqrt(p.HP_EV))/4))*p.level)/100) + p.level + 10
    
    attack     = formula(p.attack_base, p.attack_IV, p.attack_EV, p.level)
    defense    = formula(p.defense_base, p.defense_IV, p.defense_EV, p.level)
    sp_attack  = formula(p.sp_attack_base, p.sp_IV, p.sp_EV, p.level)
    sp_defense = formula(p.sp_defense_base, p.sp_IV, p.sp_EV, p.level)

    poke.HP         = hp
    poke.attack     = attack
    poke.defense    = defense
    poke.sp_attack  = sp_attack
    poke.sp_defense = sp_defense




def getAvatar(pokemonType):
    """Returns the avatar for a Pokémon, if it exists"""
    try:
        im_file = str(pokemonType.value) + ".png"
        im = plt.imread('pokemon/sprites/sugimori/'+im_file)
        return im
    except:
        print "file does not exist"



