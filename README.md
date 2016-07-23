# POKéMON

## Gotta plot em all

The python code is easy to use and can easyly be extended. For easy creation of Pokémons a sqlite3 database is created with various stats. Many objects are based on enum usage, which avoids usage of strings.

It is very easy to create a Pokémon object.

```python
pokemon = Pokemon(PokemonType.Pidgey, state = State.asleep)
# or
pokemon = Pokemon(PokemonType.Pidgey) # for normal state 
```

### Example of usage

#### Simulation of catch rate generation I
Use any Pokémon to simulate the catch rate of generation I Pokémon.
<p align="center">
<img src="images/catch1.png" height="400" alt="Screenshot"/>
</p>

#### Simulation of catch rate generation II
Use any Pokémon and Pokémon ball to simulate catch rate of Pokémon generation II.

<p align="center">
<img src="images/catch2.png" height="400" alt="Screenshot"/>
</p>

#### Plot stats of a Pokémon
Plot the stats of any Pokémon in a spider net plot.

<p align="center">
<img src="images/plot_single.png" height="450" alt="Screenshot"/>
</p>

<p align="center">
<img src="images/plot_pokemon.png" height="450" alt="Screenshot"/>
</p>

#### Compare Pokémons
Compare Pokémons in a spider net plot.

<p align="center">
<img src="images/plot_pokemons.png" height="450" alt="Screenshot"/>
</p>

#### Compare Pokémon classes
Compare different Pokémon classes in a spider net plot.

<p align="center">
<img src="images/compare_classes.png" height="450" alt="Screenshot"/>
</p>