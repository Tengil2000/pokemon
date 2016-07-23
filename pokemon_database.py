#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" -----------------------------------------------------------------------
Functions for the Pokémon database. The databse is a sqlite3
database.
Begun 2016-07-19 Alexander Karlsson
----------------------------------------------------------------------- """
import sqlite3
import csv

def create_database():
    """ Physical creation of the Pokemon sqlite3 database
        N.B: This is only done once and only once"""

    conn = sqlite3.connect('pokemon/pokemon_sql.db')
    print "opened database"

    conn.execute("""CREATE TABLE POKEMON
        (name           TEXT    PRIMARY KEY NOT NULL,
        id              REAL                NOT NULL,
        hp              INT                 NOT NULL,
        attack          INT                 NOT NULL,
        defense         INT                 NOT NULL,
        sp_attack       INT                 NOT NULL,
        sp_defense      INT                 NOT NULL,
        speed           INT                 NOT NULL,
        total           INT                 NOT NULL,
        class1          TEXT                NOT NULL,
        class2          TEXT                        ,
        ability1        TEXT                NOT NULL,
        ability2        TEXT                        ,
        hidden_ability  TEXT                        ,
        mass_kilo       REAL                NOT NULL,
        mass_lbs        REAL                NOT NULL,
        color           TEXT                NOT NULL,
        gender          TEXT                        ,
        catch_rate      INT                          );""")

    print "table created"

    conn.close()


def insert_pokemons():
    """ Inserts all pokemons from the csv file into the sqlite3 database.
        N.B. This is only done once per database."""

    conn = sqlite3.connect('pokemon/pokemon_sql.db')
    print "opened databse successfully"

    with open('pokemon/pokedex.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name       = row[0]
            id_num     = float(row[1])
            hp         = int(row[3])
            att        = int(row[4])
            df         = int(row[5])
            spatt      = int(row[6])
            spdf       = int(row[7])
            speed      = int(row[8])
            tot        = int(row[9])
            class1     = row[10].strip()
            class2     = row[11].strip()
            ab1        = row[13]
            ab2        = row[14]
            hiab3      = row[15]
            masskilo   = float(row[16])
            masslbs    = masskilo * 2.20462262
            color      = row[20]
            gender     = row[22]
            catch_rate = row[25]

            im_file = "pokemon/sprites/sugimori/" + str(id_num) + ".png"

            conn.execute('INSERT INTO POKEMON VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (name, id_num, hp, att, df, spatt, spdf, speed, tot, class1, class2, 
            ab1, ab2, hiab3, masskilo, masslbs, color, gender, catch_rate))
    
    conn.commit()

    print "Operation done successfully"
    conn.close()


def test_select():
    conn = sqlite3.connect('pokemon/pokemon_sql.db')
    print "opened databse successfully"

    #cursor = conn.execute("SELECT * FROM POKEMON WHERE NAME = 'Abomasnow'")
    cursor = conn.execute("SELECT * FROM POKEMON WHERE name = 'Abomasnow'")

    for row in cursor:
        print row[0]

    print "operation done successfully"
    conn.close()


#create_database()
insert_pokemons()
#test_select()