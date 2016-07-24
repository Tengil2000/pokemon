#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" -----------------------------------------------------------------------
Main objects and functions for creating Pokémon objects.
Begun 2016-07-15 Alexander Karlsson
----------------------------------------------------------------------- """
import sqlite3
from pokemon_type import PokemonType
from enum import Enum
import matplotlib.pyplot as plt
from numpy import floor, ceil, sqrt
import numpy as np

class PokemonClass(Enum):
    """Class (Type) of Pokémon"""
    null     = -1
    Normal   = 0
    Fire     = 1
    Water    = 2
    Electric = 3
    Grass    = 4
    Ice      = 5
    Fighting = 6
    Poison   = 7
    Ground   = 8
    Flying   = 9
    Psychic  = 10
    Bug      = 11
    Rock     = 12
    Ghost    = 13
    Dragon   = 14
    Dark     = 15
    Steel    = 16
    Fairy    = 17



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



class PokeLogic(Enum):
    lessThan       = '<'
    equals         = '='
    largerThan     = '>'

class PokeAttribute(Enum):
    id             = 'id'
    hp             = 'hp'
    attack         = 'attack'
    defense        = 'defense'
    sp_attack      = 'sp_attack'
    sp_defense     = 'sp_defense'
    speed          = 'speed'
    total          = 'total'
    class1         = 'class1'
    class2         = 'class2'
    ability1       = 'ability1'
    ability2       = 'ability2'
    hidden_ability = 'hidden_ability'
    mass_kilo      = 'mass_kilo'
    mass_lbs       = 'mass_lbs'
    color          = 'color'
    gender         = 'gender'
    catch_rate     = 'catch_rate' 




def find_pokemons_by(attribute, logic, value):
    """Finds Pokémons with the valid attributes"""
    pokemons = []

    if isinstance(value, PokemonClass):
        value = value.name

    conn = sqlite3.connect('pokemon/pokemon_sql.db')
    exe =  str("SELECT * FROM POKEMON WHERE ") + str(attribute.value) + " " + logic.value + " ?"
    cursor = conn.execute(exe, (value, ))
    
    for row in cursor:
        pokemons.append(Pokemon(PokemonType(row[1])))

    conn.close()
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

 


class PokemonMatrix():
    """ A matrix that represents strengths and weaknesses of the various pokemon types
        This matrix is for generation 6. There should not be much different in the
        generations, only additional pokemon types in the higher generations. 
        For instance Fairy is not present in a generation 2-5 matrix.
    """
    def __init__(self):
        #   Nor Fir Wat Ele Gra ice Fig Poi Gro Fly Psy Bug Roc Gho Dra Dar Ste Fai
        # |----> Defense
        # |
        # V Attack
        self.mat = np.matrix([ 
            [1, 1,  1,  1,  1,	1,	1,	1,	1,	1,	1,	.5,	0,	1,	1,	.5,	1,  1],
            [1, .5, .5,	1,  2,	2,	1,	1,	1,	1,	1,	2,	.5,	1,	.5,	1,	2,	1],
            [1, 2,  .5,	1,  .5,	2,	1,	1,	2,	1,	1,	1,	2,	1,	.5,	1,	2,	1],
            [1, 1,  2,  .5, .5,	1,	1,	1,	0,	2,	1,	1,	1,	1,	.5,	1,	1,	1],
            [1, .5, 2,  1,  .5,	1,	1,	.5,	2,	.5,	1,	.5,	2,	1,	.5,	1,	.5,	1],
            [1, .5, .5, 1,  2,	.5,	1,	1,	2,	2,	1,	1,	1,	1,	2,	1,	.5,	1],
            [2, 1,  1,  1,  1,	2,	1,	.5,	1,	.5,	.5,	.5,	2,	0,	1,	2,	2,	.5],
            [1, 1,  1,  1,	2,	1,	1,	.5,	.5,	1,	1,	1,	.5,	.5,	1,	1,	0,	2],
            [1, 2,  1,  2,	.5,	1,	1,	2,	1,	0,	1,	.5,	2,	1,	1,	1,	2,	1],
            [1, 1,  1,  .5,	2,	1,	2,	1,	1,	1,	1,	2,	.5,	1,	1,	1,	.5,	1],
            [1, 1,  1,  1,	1,	1,  2,	2,	1,	1,	.5,	1,	1,	1,	1,	0,	.5,	1],
            [1, .5,	1,  1,	2,	1,	.5,	.5,	1,	.5,	2,	1,	1,	.5, 1,	2,	.5,	.5],
            [1, 2,  1,  1,	1,	2,	.5,	1,	.5,	2,	1,	2,	1,	1,	1,	1,	.5,	1],
            [0, 1,  1,  1,	1,	1,	1,	1,	1,	1,	2,	1,	1,	2,	1,	.5,	1,	1],
            [1, 1,  1,  1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,  2,	1,	.5,	0],
            [1, 1,  1,  1,  1,	1,  .5,	1,	1,	1,	2,	1,	1,	2,	1,	.5,	1,	.5],
            [1, .5, .5, .5,	1,	2,	1,	1,	1,	1,	1,	1,	2,	1,	1,	1,	.5,	2],
            [1, .5, 1,  1,	1,	1,	2,	.5,	1,	1,	1,	1,	1,	1,	2,	2,	.5,	1] ])


    def getAttack(self, attackClass, defendClass):
        print self.mat[attackClass.value, defendClass.value]

    def getDefense(self, attackClass, defendClass):
        print self.mat[attackClass.value, defendClass.value]
