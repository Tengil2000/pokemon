#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" ------------------------------------------------------------------------------------------------
Simulation of catch probability of Pokémon generation 1.
Begun 2016-07-13 Alexander Karlsson
Algorithm source: http://bulbapedia.bulbagarden.net/wiki/Catch_rate
------------------------------------------------------------------------------------------------ """ 
from pokemon_type import PokemonType
from pokemon import Pokemon, State
from pokemon_balls import *
import pokemon_balls
import random
import math


def capture_simulation_gen1(ballType, pokemon):
    """Simulation of catching a Pokémon generation 1"""
    N       = 0 # will become a rand int
    is_free = False
    shakes  = 0

    if ballType == BallType.PokeBall:
        N = random.randint(0,255)
    elif ballType == BallType.GreatBall:
        N = random.randint(0,200)
    elif ballType == BallType.UltraBall or ballType == BallType.SafariBall:
        N = random.randint(0,150)

    if (pokemon.state == (State.asleep or State.frozen)) and N < 25:
        return 1, shakes
    elif (pokemon.state == (State.paralyzed or State.burned or State.poisoned)) and N < 12:
        return 1, shakes 
    else:
        f = 0
        if (N - pokemon.state.value) > pokemon.catch_rate: # catch rates in pokemon.py
            is_free = True
        
        else:
            M = random.randint(0,255)
            ball_value = 8 if ballType == BallType.GreatBall else 12
            f = (pokemon.HP * 255 * 4) / (pokemon.HPcurrent * ball_value)

            if f >= M:
                return 1, shakes
            else:
                is_free = True

    if is_free:
        # Calculate how many times the ball will shake
        d = pokemon.catch_rate * 100 / pokemon_balls.ballCatchRateGen1(ballType)
        
        if d >= 256:
            shakes = 3
        else:
            x = d * f / 255
            if (pokemon.state == (State.asleep or State.frozen)):
                x += 10
            else: 
                x += 5
            
            if x < 10:
                # The ball misses the Pokémon
                shakes = 0
            elif x < 30 and x >= 10:
                shakes = 1
            elif x < 70 and x >= 30:
                shakes = 2
            else:
                shakes = 3
        

    return 0, shakes



def capture_simulation_gen2(wildPokemon, ballType = BallType.PokeBall,  
    myPokemon = Pokemon(PokemonType.NULL_POKEMON), 
    specialEvent = SpecialEvent.null):
    """Simulation of catch rate of generation II"""

    # Modified catch rate for generation II
    ball_rate, cond = pokemon_balls.ballCatchRate(ballType, myPokemon, wildPokemon, 
        specialEvent, nbrOfTurns = 0)

    if ball_rate > 255:
        ball_rate = 255
    if ball_rate < 1:
        ball_rate = 1

    hp_max  = 3 * wildPokemon.HP
    hp_curr = 2 * wildPokemon.HPcurrent
    
    if hp_max > 255:
        hp_max  = math.floor(hp_max / 2)
        hp_max  = math.floor(hp_max / 2)
        hp_curr = math.floor(hp_curr / 2)
        hp_curr = math.floor(hp_curr / 2)

    if wildPokemon.HP > 342:
        hp_max = 342

    hp_max  = 1 if hp_max  == 0 else hp_max
    hp_curr = 1 if hp_curr == 0 else hp_curr

    # Modified catch rate
    a = max(float(hp_max - hp_curr) * float(ball_rate)/float(hp_max), 1)
    a = min(a, 255)

    num = random.randint(0, 255)

    if num <= a: return 1
    
    return 0