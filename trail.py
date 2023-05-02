from __future__ import annotations
from dataclasses import dataclass
from mountain import Mountain
from typing import TYPE_CHECKING, Union
from data_structures.linked_stack import LinkedStack
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
        empty = Trail(None)

        call_stack = LinkedStack()
        call_stack.push(self)

        # while there are still paths to follow
        while not call_stack.is_empty():
            current_trail = call_stack.pop()

            if isinstance(current_trail.store, TrailSplit):
                path_top = current_trail.store.path_top
                path_bottom = current_trail.store.path_bottom
                following_path = current_trail.store.path_follow
                # push the trail following the split to the stack
                if following_path != empty:
                    call_stack.push(following_path)
                # choose the trail to take in the split based on personality and push to stack, which is processed immediately
                if personality.select_branch(path_top, path_bottom):
                    call_stack.push(path_top)
                else:
                    call_stack.push(path_bottom)
                
            elif isinstance(current_trail.store, TrailSeries):
                mountain = current_trail.store.mountain
                following_path = current_trail.store.following
                #  adds the mountain which will be passed by the walker, and push the following trail to the stack
                personality.add_mountain(mountain)
                if following_path != empty:
                    call_stack.push(following_path)
        
        
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
        