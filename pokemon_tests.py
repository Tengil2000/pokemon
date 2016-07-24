#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" -----------------------------------------------------------------------
Various tests for the Pokémon code.
Begun 2016-07-15 Alexander Karlsson
----------------------------------------------------------------------- """
from pokemon import Pokemon, State, PokemonAttribute, PokemonClass
import pokemon
from pokemon_type import PokemonType
import numpy as np
from pokemon_capture import *
import matplotlib.pyplot as plt
from pokemon_balls import PokemonType
import unittest
import pokemon_balls
import pokemon_plot

def test_pokemon_capture_gen1():
    """Test simulation of capturing Pokémons of catch algorithm generation 1"""
    pokemon    = Pokemon(PokemonType.Pikachu, State.asleep)
    HPmax      = pokemon.HP
    catch_arr  = []
    shakes_arr = np.zeros(HPmax-1)
    hp_arr     = [i for i in range(1,HPmax)]

    # Simulate
    for i in range(1,HPmax):

        catch_sum = 0
        shake_sum = 0
        pokemon.HPcurrent = i

        for j in range(400):
            a, b = capture_simulation_gen1(BallType.UltraBall, pokemon)
            catch_sum += float(a/4.0)

        catch_arr.append(catch_sum)

    fig, ax = plt.subplots()
    fig.suptitle('Pokemon gen1 simulation', fontsize=17, fontweight='bold')
    ax.set_title(pokemon.name, fontsize=16)
    ax.plot(hp_arr, catch_arr, label="Catch Probability")
    ax.set_xlabel('Current HP', fontsize=15)
    ax.set_ylabel('Ratio', fontsize=15)
    legend = ax.legend()

    plt.show()



def test_pokemon_capture_gen2():
    """Test simulation of capture Pokémons of generation II"""
    pokemon = Pokemon(PokemonType.Electabuzz)
    catch_arr = []
    HPmax = pokemon.HP
    hp_arr = [i for i in range(1, HPmax)]

    # Simulate
    for i in range(1, HPmax):
        catch_sum = 0
        pokemon.HPcurrent = i

        for j in range(1000):
            a = capture_simulation_gen2(pokemon, BallType.MasterBall)
            catch_sum += a

        catch_arr.append(catch_sum/10)


    fig, ax = plt.subplots()
    fig.suptitle('Pokemon gen2 simulation', fontsize=17, fontweight='bold')
    ax.set_title(pokemon.name, fontsize=16)
    ax.plot(hp_arr, catch_arr, label="Catch Probability", color='m')
    ax.set_xlabel('Current HP', fontsize=15)
    ax.set_ylabel('Ratio', fontsize=15)
    legend = ax.legend()

    plt.show()



def test_plotPokemon():
    """Tests the function for plotting the stats of a Pokémon"""
    pokemon = Pokemon(PokemonType.Electabuzz)
    pokemon_plot.plotPokemons([pokemon])


def test_plotPokemons():
    """Tests the function for plotting multiple Pokémons"""
    pokemon1 = Pokemon(PokemonType.Bulbasaur, State.asleep)
    pokemon2 = Pokemon(PokemonType.Squirtle, State.asleep)
    pokemon3 = Pokemon(PokemonType.Charmander, State.asleep)

    pokemonList = [pokemon1, pokemon2, pokemon3]
    pokemon_plot.plotPokemons(pokemonList)


def test_compare_classes():
    """Plots the mean values of two classes"""
    pokemon_plot.compare_classes([PokemonClass.Grass, PokemonClass.Electric])


def test_show_avatar():
    """Shows a Pokémon avatar"""
    im = pokemon.getAvatar(PokemonType.Pikachu)
    plt.imshow(im)
    plt.show()


def test_plotSinglePokemon():
    p = Pokemon(PokemonType.Electabuzz, State.normal)
    pokemon_plot.plotPokemon(p)
    #p = Pokemon(PokemonType.Charizard, State.normal)
    #pokemon_plot.plotPokemon(p)
    #p = Pokemon(PokemonType.Ekans, State.normal)
    #pokemon_plot.plotPokemon(p)



class PokemonUnitTests(unittest.TestCase):

    """ ------------------------------------------------------------------------------
    Test getting pokemons from file defined by some attribute
    ------------------------------------------------------------------------------ """
    def test_natIdxLessTan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.natIdxLessThan, 10)
        self.assertTrue(pokemons[0].pokemontype == PokemonType.Bulbasaur)

    def test_natIdxEquals(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.natIdxEquals, 50)
        self.assertTrue(len(pokemons) == 1)

    def test_natIdxGreaterThan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.natIdxGreaterThan, 648.5)
        self.assertTrue(pokemons[0].pokemontype == PokemonType.Genesect and len(pokemons) == 1)

    def test_hpLessThan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.hpLessThan, 20)
        self.assertTrue(len(pokemons) == 2 and pokemons[0].HP < 20)

    def test_hpEquals(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.hpEquals, 20)
        self.assertTrue(len(pokemons) == 6 and pokemons[0].HP == 20)

    def test_hpGreaterThan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.hpGreaterThan, 170)
        self.assertTrue(len(pokemons) == 3 and pokemons[0].HP > 170)

    def test_attackLessThan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.attackLessThan, 10)
        self.assertTrue(len(pokemons) == 2 and pokemons[0].attack < 10)

    def test_attackEquals(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.attackEquals, 10)
        self.assertTrue(len(pokemons) == 3 and pokemons[0].attack == 10)

    def test_attackGreaterThan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.attackGreaterThan, 160)
        self.assertTrue(len(pokemons) == 2 and pokemons[0].attack > 160)

    def test_defenseLessThan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.defenseLessThan, 10)
        self.assertTrue(len(pokemons) == 2 and pokemons[0].defense < 10)

    def test_defenseEquals(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.defenseEquals, 15)
        self.assertTrue(len(pokemons) == 4 and pokemons[0].defense == 15)

    def test_defenseGreaterThan(self):
        pokemons = pokemon.find_pokemons_with_attributes(PokemonAttribute.defenseGreaterThan, 180)
        self.assertTrue(len(pokemons) == 3 and pokemons[0].defense > 180)

    def test_classBelonging(self):
        pokemons = pokemon.find_pokemons_by_class(PokemonClass.Steel)
        self.assertTrue(len(pokemons) == 38 and pokemons[0].class1 == PokemonClass.Steel)


    """ ------------------------------------------------------------------------------
    Test Update pokemon stats
    ------------------------------------------------------------------------------ """
    def test_update_pokemon_gen12(self):
        """Test updating special skills of a Pokémon"""
        p            = Pokemon(PokemonType.Pikachu, State.normal)
        p.level      = 81
        p.HP_IV      = 7
        p.HP_EV      = 22850
        p.attack_IV  = 8
        p.attack_EV  = 23140
        p.defense_IV = 13
        p.defense_EV = 17280
        p.sp_IV      = 9
        p.sp_EV      = 19625

        pokemon.update_pokemon_gen2(p)
        self.assertTrue(p.HP == 189.0 and p.attack == 137.0 and p.defense == 101.0
            and p.sp_attack == 128.0 and p.sp_defense == 112.0)

    """ ------------------------------------------------------------------------------
    Test balls
    ------------------------------------------------------------------------------ """

    # -----------------------------------------------------------------------------------
    def catchRate(self, ballType, my = Pokemon(PokemonType.NULL_POKEMON),
        wild = Pokemon(PokemonType.NULL_POKEMON), ev = SpecialEvent.null, nbrOfTurns = 0):
        return pokemon_balls.ballCatchRate(ballType, my, wild, ev, nbrOfTurns)
    # -----------------------------------------------------------------------------------

    def test_pokeball(self):
        self.assertEqual(ballCatchRateGen1(BallType.PokeBall) == 255
            and self.catchRate(BallType.PokeBall), (1, True))

    def test_ultraball(self):
        self.assertEqual(ballCatchRateGen1(BallType.UltraBall) == 150
            and self.catchRate(BallType.UltraBall), (2.5, True))

    def test_masterball(self):
        self.assertEqual(self.catchRate(BallType.MasterBall), (255, True))

    def test_safariball(self):
        self.assertTrue(ballCatchRateGen1(BallType.SafariBall)== 150
        and self.catchRate(BallType.SafariBall) == (1.5, True))

    def test_levelball(self):
        # Example pokemons
        a = Pokemon(PokemonType.Abomasnow, State.normal)
        b = Pokemon(PokemonType.Abra, State.normal)

        a.level = 1
        b.level = 2
        self.assertEqual(self.catchRate(BallType.LevelBall, a, b), (1, True))
        a.level = 3
        self.assertEqual(self.catchRate(BallType.LevelBall, a, b), (2, True))
        a.level = 5
        self.assertEqual(self.catchRate(BallType.LevelBall, a, b), (4, True))
        a.level = 9
        self.assertEqual(self.catchRate(BallType.LevelBall, a, b), (8, True))

    def test_lureBall(self):
        self.assertTrue(self.catchRate(BallType.Lureball, ev=SpecialEvent.isFishing), (3, True))
        self.assertTrue(self.catchRate(BallType.Lureball), (1, True))

    def test_moonBall(self):
        self.assertEqual(self.catchRate(BallType.MoonBall, wild = Pokemon(PokemonType.Nidoran_Male)), (4, True))
        self.assertEqual(self.catchRate(BallType.MoonBall, wild = Pokemon(PokemonType.Nidoran_Female)), (4, True))
        self.assertEqual(self.catchRate(BallType.MoonBall, wild = Pokemon(PokemonType.Clefairy)), (4, True))
        self.assertEqual(self.catchRate(BallType.MoonBall, wild = Pokemon(PokemonType.Jigglypuff)), (4, True))
        self.assertEqual(self.catchRate(BallType.MoonBall, wild = Pokemon(PokemonType.Skitty)), (4, True))
        self.assertEqual(self.catchRate(BallType.MoonBall, wild = Pokemon(PokemonType.Happiny)), (1, True))
        self.assertNotEqual(self.catchRate(BallType.MoonBall, wild = Pokemon(PokemonType.Clefairy)), (1, True))

    def test_LoveBall(self):
        poks1 = pokemon.find_pokemons_by_class(PokemonClass.Dragon)
        poks2 = pokemon.find_pokemons_by_class(PokemonClass.Electric)
        self.assertEqual(self.catchRate(BallType.LoveBall, poks1[0], poks1[1]), (8,True))
        self.assertEqual(self.catchRate(BallType.LoveBall, poks2[0], poks2[1]), (8,True))
        self.assertEqual(self.catchRate(BallType.LoveBall, poks1[0], poks2[0]), (1,True))

    def test_heavyBall(self):
        pok1 = Pokemon(PokemonType.Meganium)
        self.assertEqual(self.catchRate(BallType.HeavyBall, wild = pok1), (-20, False))
        pok2 = Pokemon(PokemonType.Registeel)
        self.assertEqual(self.catchRate(BallType.HeavyBall, wild = pok2), (20, False))
        pok3 = Pokemon(PokemonType.Hippowdon)
        self.assertEqual(self.catchRate(BallType.HeavyBall, wild = pok3), (20, False))
        pok4 = Pokemon(PokemonType.Torterra)
        self.assertEqual(self.catchRate(BallType.HeavyBall, wild = pok4), (30, False))
        pok5 = Pokemon(PokemonType.Steelix)
        self.assertEqual(self.catchRate(BallType.HeavyBall, wild = pok5), (30, False))
        pok6 = Pokemon(PokemonType.Regigigas)
        self.assertEqual(self.catchRate(BallType.HeavyBall, wild = pok6), (40, False))
        pok7 = Pokemon(PokemonType.Rampardos)
        self.assertEqual(self.catchRate(BallType.HeavyBall, wild = pok7), (0, False))

    def test_fastBall(self):
        pok1 = Pokemon(PokemonType.Magnemite)
        self.assertEqual(self.catchRate(BallType.FastBall, wild = pok1), (4, True))
        pok2 = Pokemon(PokemonType.Grimer)
        self.assertEqual(self.catchRate(BallType.FastBall, wild = pok2), (4, True))
        pok3 = Pokemon(PokemonType.Tangela)
        self.assertEqual(self.catchRate(BallType.FastBall, wild = pok3), (4, True))
        # Base speed at least 100
        pok4 = Pokemon(PokemonType.Jirachi)
        self.assertEqual(self.catchRate(BallType.FastBall, wild = pok4), (4, True))
        pok5 = Pokemon(PokemonType.Genesect)
        self.assertEqual(self.catchRate(BallType.FastBall, wild = pok5), (1, True))

    def test_sportBall(self):
        self.assertEqual(self.catchRate(BallType.SportBall), (1.5, True))

    def test_premierBall(self):
        self.assertEqual(self.catchRate(BallType.PremierBall), (1, True))

    def test_repeatBall(self):
        self.assertEqual(self.catchRate(BallType.RepeatBall, ev = SpecialEvent.isInPokedex), (3, True))
        self.assertEqual(self.catchRate(BallType.RepeatBall), (1, True))

    def test_nestball(self):
        pok = Pokemon(PokemonType.Audino)
        pok.level = 29.999999
        rate, cond = self.catchRate(BallType.NestBall, wild = pok)
        self.assertTrue(rate > 1)
        pok.level = 40
        self.assertEqual(self.catchRate(BallType.NestBall, wild = pok), (1,True))

    def test_netBall(self):
        poks1 = pokemon.find_pokemons_by_class(PokemonClass.Bug)
        poks2 = pokemon.find_pokemons_by_class(PokemonClass.Water)
        poks3 = pokemon.find_pokemons_by_class(PokemonClass.Dark)
        self.assertEqual(self.catchRate(BallType.NetBall, wild = poks1[0]), (3, True))
        self.assertEqual(self.catchRate(BallType.NetBall, wild = poks2[0]), (3, True))
        self.assertEqual(self.catchRate(BallType.NetBall, wild = poks3[0]), (1, True))

    def test_diveBall(self):
        self.assertTrue(self.catchRate(BallType.DiveBall, ev = SpecialEvent.isFishing), (3.5, True))
        self.assertTrue(self.catchRate(BallType.DiveBall, ev = SpecialEvent.isSurfing), (3.5, True))
        self.assertTrue(self.catchRate(BallType.DiveBall, ev = SpecialEvent.isUnderWater), (3.5, True))
        self.assertTrue(self.catchRate(BallType.DiveBall), (1, True))

    def test_luxuryBall(self):
        self.assertTrue(self.catchRate(BallType.LuxuryBall), (1,True))

    def test_healBall(self):
        self.assertTrue(self.catchRate(BallType.HealBall), (1,True))

    def test_quickBall(self):
        self.assertTrue(self.catchRate(BallType.QuickBall, nbrOfTurns = 1), (5, True))
        self.assertTrue(self.catchRate(BallType.QuickBall, nbrOfTurns = 2), (1, True))

    def test_duskBall(self):
        self.assertTrue(self.catchRate(BallType.Duskball, ev = SpecialEvent.isAtNight), (3.5, True))
        self.assertTrue(self.catchRate(BallType.Duskball, ev = SpecialEvent.isInCave), (3.5, True))
        self.assertTrue(self.catchRate(BallType.Duskball), (1, True))

    def test_cherishBall(self):
        self.assertTrue(self.catchRate(BallType.CherishBall), (1, True))

    def test_parkBall(self):
        self.assertTrue(self.catchRate(BallType.ParkBall), (255, True))

    def test_dreamBall(self):
        self.assertTrue(self.catchRate(BallType.DreamBall), (255, True))


# Run tests ------------------------------------------------

if __name__ == '__main__':

    #test_pokemon_capture_gen1()
    #test_pokemon_capture_gen2()
    #test_plotPokemon()
    test_plotPokemons()
    #test_compare_classes()
    #test_show_avatar()
    #test_plotSinglePokemon()
    #unittest.main()




# TODO
# Finish pokemon.find_pokemons_with_attributes
# Implement SQLite database support for getting Pokemons
