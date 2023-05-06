from __future__ import annotations

from mountain import Mountain
from typing import List
import bisect

#What is bisect? -> bisect module provides support for maintaining a list in sorted order without having to sort the list after each insertion. For long lists of items with expensive comparison operations, this can be an improvement over the more common approach. The module is called bisect because it uses a basic bisection algorithm to do its work. The source code may be most useful as a working example of the algorithm (the boundary conditions are already right!).

class MountainOrganiser:
    '''
    A class that organises mountains by their length and name

    === Attributes ===
    
    mountains: a list of mountains in the organiser
    mountain: a mountain in the organiser
    pos : the position of the mountain in the organiser
    '''

    def __init__(self) -> None:
        '''
        Creates a new MountainOrganiser
        Time Complexity: O(1)
        '''
        self.mountains = [] 




    def cur_position(self, mountain: Mountain) -> int:
        '''
        Returns the current position of the mountain in the organiser

        Worst Time Complexity: O(log n) where n is the number of mountains in the organiser, when n is not 0
        Best Time Complexity: O(1) where n is the number of mountains in the organiser, when n is 0
        '''

        pos = bisect.bisect_left(self.mountains, (mountain.length, mountain.name)) #pos is the position where the mountain should be inserted
        if pos != len(self.mountains) and self.mountains[pos] == (mountain.length, mountain.name): #if the mountain is already in the organiser, return the position
            return pos
        
        else: #raise KeyError if the mountain is not in the organiser
            raise KeyError("Mountain not found")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        '''
        Adds a list of mountain to the organiser 
        add_mountains should have complexity at most 

        Worst time Complexity: O(n log n) where n is the number of mountains in the organiser, when n is not 0
        Best Time Complexity: O(n) where n is the number of mountains in the organiser, when n is 0
        '''
        for mountain in mountains: #for each mountain in the list, insert it into the organiser
            bisect.insort(self.mountains, (mountain.length, mountain.name))





        

        
