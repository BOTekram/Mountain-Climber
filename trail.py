from __future__ import annotations
from dataclasses import dataclass
from mountain import Mountain
from typing import TYPE_CHECKING, Union
# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail


    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store
        
                                                                                      

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """
#TrailSeries (Mountain(name, difficulty, length), Trail(info))

#Trail(info)
    #Arguments are :- (None, TrailSeries, TrailSplit)

#TrailSplit(Trail(info), Trail(info), Trail(info))
#.store is basically what’s stored inside a trail series object. Only trail series has .store


    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""

        return TrailSeries(self.mountain
                           (self.mountain.name, 0, 0), 
                           self.following)
        

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
            
        return TrailSeries(mountain,
                           Trail( TrailSeries
                                 (self.mountain, self.following) 
                                 )
                            )


    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        
        return TrailSplit(Trail(None), 
                          Trail(None), 
                          Trail(TrailSeries
                                (self.mountain, self.following)
                                )
                          )
        
    

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""

        return TrailSeries(self.mountain, 
                           Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        
    
    
        return TrailSeries(self.mountain, 
                           Trail(
                                TrailSplit(
                                        Trail(None), Trail(None), Trail(self.following.store)
                                        )
                                )
                            )

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""

        return Trail(TrailSeries(mountain, self))


    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        
        return Trail(TrailSplit(Trail(None), Trail(None), self))
        
    
    

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        
        if isinstance(self.store, TrailSplit):
            if personality.select_branch(self.store.path_top, self.store.path_bottom):
                self.store = self.store.path_top.store
            else:
                self.store = self.store.path_bottom.store
        elif isinstance(self.store, TrailSeries):
            self.store = self.store.following.store
        else:
            raise ValueError("Cannot follow a path when there is no path to follow!")





        
        
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError() #donot touch yet (task 1)
        

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError() #donot touch yet (task 1)
        
        
    
        
        
