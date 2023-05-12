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
        """
        Follow a path and add mountains according to a personality.
        Best Time Complexity: O(n)
        Worst Time Complexity: O(n)
        """
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
        """
        Returns a list of all mountains on the trail.
        Best Time Complexity: O(n)
        Worst Time Complexity: O(n)
        """
        empty = Trail(None)
        mountain_list = []

        call_stack = LinkedStack()
        call_stack.push(self)

        # while there are still paths to follow
        while not call_stack.is_empty():
            current_trail = call_stack.pop()

            if isinstance(current_trail.store, TrailSplit):
                path_top = current_trail.store.path_top
                path_bottom = current_trail.store.path_bottom
                following_path = current_trail.store.path_follow
                
                if following_path != empty:
                    call_stack.push(following_path)
                if path_bottom != empty:
                    call_stack.push(path_bottom)
                if path_top != empty:
                    call_stack.push(path_top)
                
            elif isinstance(current_trail.store, TrailSeries):
                mountain = current_trail.store.mountain
                following_path = current_trail.store.following

                if following_path != empty:
                    call_stack.push(following_path)
                mountain_list.append(mountain)

        return mountain_list
        

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.

        Best Time Complexity: O(n^k) where n is the number of branches and k is the length of the path
        Worst Time Complexity: O(n^k) where n is the number of branches and k is the length of the path
        """
        total_path = self.search_all_path()
        length_k_path = [path for path in total_path if len(path) == k]

        return length_k_path

    def search_all_path(self) -> list[list[Mountain]]:
        """
        Helper function for length_k_paths.
        Best Time Complexity: O(n^k) where n is the number of branches and k is the length of the path
        Worst Time Complexity: O(n^k) where n is the number of branches and k is the length of the path
        """
        current_trail = self

        if current_trail == Trail(None):
            return [[]]
        elif isinstance(current_trail.store, TrailSplit):
            trail_top = current_trail.store.path_top
            trail_bottom = current_trail.store.path_bottom
            trail_follow = current_trail.store.path_follow

            all_path_top = trail_top.search_all_path()  # [[Mountain]]
            all_path_bottom = trail_bottom.search_all_path()
            all_path_follow = trail_follow.search_all_path()
            
            total_path = self.extend_list(all_path_top, all_path_bottom,True)
            total_path = self.extend_list(total_path, all_path_follow,False)

            return total_path
        elif isinstance(current_trail.store, TrailSeries):
            initial_mountain = current_trail.store.mountain
            trail_follow = current_trail.store.following

            call_stack = LinkedStack()
            total_path = [[initial_mountain]]
            call_stack.push(trail_follow)

            while not call_stack.is_empty():
                current_trail = call_stack.pop()
                total_path = self.extend_list(total_path, current_trail.search_all_path(),False)
            return total_path
        


    def extend_list(self, first_part: list[list[Mountain]], second_part: list[list[Mountain]], is_join) -> list[list[Mountain]]:
        """
        Return all combination of paths from first part and second part
        Example: 
        first_part = [[a],[b]]
        second_part = [[c,d],[e]]
        if is_join is True, just extends
            return [[a],[b],[c,d],[e]]
        else
            return [[a,c,d],[a,e],[b,c,d],[b,e]]

        Best Time Complexity: O(n^2) where n is the number of branches
        Worst Time Complexity: O(n^2) where n is the number of branches
        """
        if is_join:
            first_part.extend(second_part)
            return first_part
        else:
            return [first + second for first in first_part for second in second_part] # all combination