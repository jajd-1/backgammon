import pandas as pd
import numpy as np 
import random
from enum import Enum
from dataclasses import dataclass

class Colour(Enum):
    white = 1
    black = -1

class Point():
    """An instance of Point will have associated to it a colour (possibly None if there are no checkers) and a count, which tells you the number of checkers of that colour. 
    We define methods to add or remove a single checker from a point."""

    def __init__(self, colour: Colour | None = None, count: int = 0):
        self.colour = colour 
        self.count = count 

    def is_empty(self):
        return self.count == 0
    
    def is_blot(self):
        return self.count == 1
    
    def is_owned_by(self, colour: Colour):
        return self.colour == colour 
    
    
    # def is_blocked_for(self, colour: Colour):         (I think these should form part of rules class)
    #     return(self.colour is not None 
    #            and self.colour != colour 
    #            and self.count >= 2)
    
    # def can_land(self, colour: Colour):
    #     return not self.is_blocked_for(colour)
    
    def add_checker(self, colour: Colour):
        if self.is_empty():
            self.colour = colour
            self.count = 1
        elif self.colour == colour:
            self.count += 1
        else:
            raise ValueError("Cannot stack on opponent's point")    #This should be prevented by rules class
    
    def remove_checker(self):
        if self.count == 0:
            raise ValueError("No checkers to remove")       #This should be prevented by rules class
        
        self.count -= 1
        if self.count == 0:
            self.colour = None 



@dataclass(frozen=True) #dataclass automatically generates common methods (e.g. __init__, __repr__) for classes that mainly store data, i.e. classes with no behaviour 
class SingleMove():
    from_idx: int   #the initial board index of the checker. from_idx = 0 means from the bar
    to_idx: int     #the ending board index of the checker. to_idx = -1 means bear off
    die_used: int   #the die used for this move


class Board():
    def __init__(self):
        """The board consists of 24 points, the bar and the bear-off area."""
        self.points = [Point() for _ in range(24)]      #A list of 24 Point objects (which will be indexed from 0 to 23)
        self.bar = {Colour.white: 0, Colour.black: 0}   #Colour is an Enum, which is immutable and hence can be used as a dict key
        self.off = {Colour.white: 0, Colour.black: 0}

    @staticmethod  #we are about to define a function that just happens to live inside the Board class, but doesn't receive self 
    def shift(idx: int) -> int:      #convert the index on the board (1 to 24) to the Python index (0 to 23)
        if not (1 <= idx <= 24):
            raise ValueError("Points on board must be from 1 to 24")
        else: 
            return idx - 1
        
    def point_at_index(self, idx: int) -> Point:    #Given the board index idx, returns the point object at Python index idx - 1 in the list points
        return self.points[self.shift(idx)]
    
    def starting_setup(self) -> None: 
        self.__init__()     #this clears the board

        def place_checker(colour: Colour, idx: int, n: int):     #will place n checkers of colour 'colour' at board index idx 
            p = self.point_at_index(idx) 
            for _ in range(n):
                p.add_checker(colour)

        place_checker(Colour.white, 24, 2)
        place_checker(Colour.white, 13, 5)
        place_checker(Colour.white, 8, 3)
        place_checker(Colour.white, 6, 5)

        place_checker(Colour.black, 1, 2)
        place_checker(Colour.black, 12, 5)
        place_checker(Colour.black, 17, 3)
        place_checker(Colour.black, 19, 5)

    
    def take_from_bar(self, colour: Colour) -> None:
        if self.bar[colour] <= 0:
            raise ValueError("Bar is empty.")
        self.bar[colour] -= 1
    
    def put_on_bar(self, colour: Colour) -> None:
        self.bar[colour] += 1
    
    def bear_off(self, colour: Colour) -> None:
        self.off[colour] += 1
    
    def move_checker(self, colour: Colour, from_idx: int, to_idx: int) -> None:
        #this does NOT check legality of the move!
        if from_idx == 0:
            self.take_from_bar(colour)
        else: 
            self.point_at_index(from_idx).remove_checker()

        if to_idx == -1:
            self.bear_off(colour)
            return 
        
        dest = self.point_at_index(to_idx)

        if not dest.is_empty() and dest.colour != colour:
            if not dest.is_blot():
                raise ValueError("You cannot land on a blocked point.")     #This should be prevented by rules class
            opponent_colour = dest.colour()
            dest.remove_checker()
            self.put_on_bar(opponent_colour)

        dest.add_checker(colour) 


class Dice():
    def __init__(self):
        


#class Rules():

#class Player():








    











"""
class Game():
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.current_player_index = 0
        self.dice = Dice()
        self.rules = Rules()
        self.game_over = False 
"""