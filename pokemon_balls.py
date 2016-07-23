#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" -----------------------------------------------------------------------
Objects representing POKéMON balls. Different catch rate depending on
generation, type race and so on.
Begun 2016-07-16 Alexander Karlsson
----------------------------------------------------------------------- """
from pokemon_type import PokemonType
from pokemon import Pokemon, State, PokemonClass
from enum import Enum
import abc


class SpecialEvent(Enum):
    null           = 0
    isFishing      = 100
    isNotFishing   = 101
    isInPokedex    = 200
    isNotInPokedex = 201
    isSurfing      = 300
    isUnderWater   = 400
    isInCave       = 500
    isAtNight      = 600


class BallType(Enum):
    PokeBall    = 0
    GreatBall   = 1
    UltraBall   = 2
    MasterBall  = 3
    SafariBall  = 4

    LevelBall   = 10
    Lureball    = 11
    MoonBall    = 12
    FriendBall  = 13
    LoveBall    = 14    
    HeavyBall   = 15
    FastBall    = 16
    SportBall   = 17
    
    PremierBall = 20
    RepeatBall  = 21
    TimerBall   = 22
    NestBall    = 23
    NetBall     = 24
    DiveBall    = 25
    LuxuryBall  = 26

    HealBall    = 30
    QuickBall   = 31
    Duskball    = 32
    CherishBall = 33
    ParkBall    = 34

    DreamBall   = 40



def ballCatchRateGen1(ballType = BallType.PokeBall):
    """Only to be used for in Generation I simluations."""
    if ballType == BallType.PokeBall:
        return 255
    if ballType == BallType.GreatBall:
        return 200
    if ballType == BallType.UltraBall or ballType == BallType.SafariBall:
        return 150


def ballCatchRate(ballType, myPokemon, wildPokemon, specialEvent, nbrOfTurns):
    """Returns the catch rate given a ball. The returned value can depend on
    special event, pokemons currently battling and number of turns in battle. 
    If there is no such info set the params to null such as
    
    myPokemon    = Pokemon(PokemonType.NULL_POKEMON),
    wildPokemon  = Pokemon(PokemonType.NULL_POKEMON),
    specialEvent = SpecialEvent.null
    nbrOfTurns   = 0
    """

    """ -------------------------------------------------------------------
    Pokemon balls introduced in generation I
    ------------------------------------------------------------------- """
    
    if ballType == BallType.PokeBall:
        return 1, True

    if ballType == BallType.GreatBall or ballType == BallType.SafariBall:
        return 1.5, True

    if ballType == BallType.UltraBall:
        return 2.5, True

    if ballType == BallType.MasterBall:
        return 255, True

    """ -------------------------------------------------------------------
    Pokemon balls introduced in generation II
    ------------------------------------------------------------------- """

    if ballType == BallType.LevelBall:
        if myPokemon.level <= wildPokemon.level:
            return 1, True
        elif myPokemon.level > wildPokemon.level and myPokemon.level <= 2*wildPokemon.level:
            return 2, True
        elif myPokemon.level > 2*wildPokemon.level and myPokemon.level <= 4*wildPokemon.level:
            return 4, True
        
        return 8, True


    if ballType == BallType.Lureball:
        if specialEvent == SpecialEvent.isFishing:
            return 3, True
        return 1, True


    if ballType == BallType.MoonBall:
        pt = wildPokemon.pokemontype
        if (pt ==  PokemonType.Nidoran_Male or pt == PokemonType.Nidoran_Female or 
            pt == PokemonType.Clefairy or pt == PokemonType.Jigglypuff or 
            pt == PokemonType.Skitty):
            return 4, True
        else:
            return 1, True


    if ballType == BallType.FriendBall:
        return 1, True


    if ballType == BallType.LoveBall:
        """Returns catch rate depending on race and gender"""
        if (myPokemon.class1 == wildPokemon.class1 or
            myPokemon.class1 == wildPokemon.class2 or
            myPokemon.class2 == wildPokemon.class1):
            return 8, True
        else:
            return 1, True

    if ballType == BallType.HeavyBall:
        if wildPokemon.mass_lbs < 225.8:
            return -20, False
        if wildPokemon.mass_lbs >= 451.5 and wildPokemon.mass_lbs <= 677.3:
            return 20, False
        if wildPokemon.mass_lbs > 677.3 and wildPokemon.mass_lbs <= 903.0:
            return 30, False
        if wildPokemon.mass_lbs > 903.0:
            return 40, False
        
        return 0, False

    
    if ballType == BallType.FastBall:
        if (wildPokemon.pokemontype == PokemonType.Magnemite or
            wildPokemon.pokemontype == PokemonType.Grimer or
            wildPokemon.pokemontype == PokemonType.Tangela):
            return 4, True

        elif wildPokemon.speed_base >= 100:
            return 4, True

        return 1, True


    if ballType == BallType.SportBall:
        return 1.5, True

    """ -------------------------------------------------------------------
    Pokemon Balls introduced in generation III
    ------------------------------------------------------------------- """
    
    if ballType == BallType.PremierBall or ballType == BallType.LuxuryBall:
        return 1, True

    if ballType == BallType.RepeatBall:
        if specialEvent == SpecialEvent.isInPokedex:
            return 3, True
        
        return 1, True


    if ballType == BallType.TimerBall:
        rate = min((nbrOfTurns*10)/10, 4)
        return rate, True
    

    if ballType == BallType.NestBall:
        rate = max((40 - wildPokemon.level)/10, 1)
        return rate, True


    if ballType == BallType.NetBall:
        if (wildPokemon.class1 == PokemonClass.Bug or 
            wildPokemon.class1 == PokemonClass.Water or
            wildPokemon.class2 == PokemonClass.Bug or
            wildPokemon.class2 == PokemonClass.Water):
            return 3, True

        return 1, True


    if ballType == BallType.DiveBall:
        if (specialEvent == SpecialEvent.isFishing or 
            specialEvent == SpecialEvent.isUnderWater or
            specialEvent == SpecialEvent.isSurfing):
            return 3.5, True
        return 1


    if ballType == BallType.LuxuryBall:
        return 1, True

    """ -------------------------------------------------------------------
    Pokemon Balls introduced in generation IV
    ------------------------------------------------------------------- """
    if ballType == BallType.HealBall or ballType == BallType.CherishBall:
        return 1, True

    if ballType == BallType.QuickBall:
        if nbrOfTurns == 1:
            return 5, True
        return 1, True

    
    if ballType == BallType.Duskball:
        if (specialEvent == SpecialEvent.isAtNight or
            specialEvent == SpecialEvent.isInCave):
            return 3.5, True
        return 1, True


    if ballType == BallType.ParkBall:
        return 255, True

    """ -------------------------------------------------------------------
    Pokemon Balls introduced in generation V
    ------------------------------------------------------------------- """
    
    if ballType == BallType.DreamBall:
        return 255, True
