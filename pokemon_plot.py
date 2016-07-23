#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" -----------------------------------------------------------------------
Various plotting functions.
2016-07-15 Alexander Karlsson
----------------------------------------------------------------------- """
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from pylab import *
from pokemon import Pokemon, PokemonClass
import pokemon
import numpy as np

class PokemonStatPLot(PolarAxes):
    name = 'radar'
    N = 7
    RESOLUTION = 1
    theta = 2*pi * linspace(0, 1, N+1)[:-1]
    theta += pi/2

    def draw_frame(self, x0, y0, r):
        verts = [(r*cos(t) + x0, r*sin(t) + y0) for t in self.theta]
        return Polygon(verts, closed=True)

    def set_varlabels(self, labels):
        self.set_thetagrids(self.theta * 180/pi, labels)

    def get_axes_patch(self):
        x0, y0 = (0.5, 0.5)
        r = 0.5
        return self.draw_frame(x0, y0, r)



def plotPokemons(pokemonList):
    """
    Plots the stats of one or multiple pokemons
    """
    register_projection(PokemonStatPLot)
    N = 7

    theta = 2*pi * linspace(0, 1, N+1)[:-1]
    theta += pi/2
    labels = ['Max HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed', 'Mass']
    
    for pokemon1 in pokemonList:
        desc1 = [pokemon1.HP, pokemon1.attack, pokemon1.defense, pokemon1.sp_attack, pokemon1.sp_defense, 
            pokemon1.speed, pokemon1.mass_kilo]

        ax = subplot(111, projection='radar')
        ax.fill(theta, desc1, pokemon1.color, label=pokemon1.name)
    

    for patch in ax.patches:
        patch.set_alpha(0.5)

    ax.set_varlabels(labels)
    rgrids((50, 100, 150, 200, 255))

    legend()
    grid(True)
    show()


def plotPokemon(pokemon1):
    register_projection(PokemonStatPLot)
    N = 7

    theta = 2*pi * linspace(0, 1, N+1)[:-1]
    theta += pi/2
    labels = ['Max HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed', 'Mass']
    
    desc1 = [pokemon1.HP, pokemon1.attack, pokemon1.defense, pokemon1.sp_attack, pokemon1.sp_defense, 
        pokemon1.speed, pokemon1.mass_kilo]

    ax1 = subplot(121, projection='radar')
    ax1.fill(theta, desc1, pokemon1.color, label=pokemon1.name)
    

    for patch in ax1.patches:
        patch.set_alpha(0.5)

    ax1.set_varlabels(labels)
    rgrids((50, 100, 150, 200, 255))

    im = pokemon.getAvatar(pokemon1.pokemontype)
    ax2 = subplot(122)
    ax2.imshow(im)    
    tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    
    legend()
    grid(False)
    show()   


def compare_classes(pokemonClasses):
    """Compare two classes by taking the mean values of all stats and then plots them."""
    pokemons = []
    
    for pClass in pokemonClasses:
        pok = pokemon.find_pokemons_by_class(pClass)
        p = pok[0]
        p.name = pClass.name

        for i in range(1, len(pok)):
            p.HP         += pok[i].HP
            p.attack     += pok[i].attack
            p.defense    += pok[i].defense
            p.sp_attack  += pok[i].sp_attack
            p.sp_defense += pok[i].sp_defense
            p.speed      += pok[i].speed

        p.HP         /= len(pok)
        p.attack     /= len(pok)
        p.defense    /= len(pok)
        p.sp_attack  /= len(pok)
        p.sp_defense /= len(pok)
        p.speed      /= len(pok)

        pokemons.append(p)


    plotPokemons(pokemons)