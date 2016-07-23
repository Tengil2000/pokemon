#!/usr/bin/env python
# -*- coding: utf-8 -*- 
""" -----------------------------------------------------------------------
Object to represent POKéMON versions
2016-07-17 Alexander Karlsson
----------------------------------------------------------------------- """
from enum import Enum

class PokemonVersion(Enum):
    null = "NULL"
    GS   = "GoldAndSilver"
    HGSS = "HeartGoldAndSoulSilver"
    C    = "Crystal"
    

