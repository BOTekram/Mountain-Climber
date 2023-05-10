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
        """
        empty = Trail(None)
        mountain_list = []

        call_stack = LinkedStack()
        call_stack.push(self)

        # while there are still paths to follow
        while not call_stack.is_empty():
            current_trail = call_stack.pop()

            if isinstance(current_trail.store, TrailSplit):
                mountain_list.append("split")
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
                all_mount_in_series = current_trail.collect_all_mountains()

        print(mountain_list)
        
        for list_mountain in self.collect_all_mountains():
            print(list_mountain)
        print(self.collect_all_mountains())





                
             
                
    def collect_all_mount_series(self):
        empty = Trail(None)
        mountain_list = []
        next_split = None

        call_stack = LinkedStack()
        call_stack.push(self)

        # while there are still paths to follow
        while not call_stack.is_empty():
            current_trail = call_stack.pop()

            if isinstance(current_trail.store, TrailSplit):
                next_split = current_trail
                
            elif isinstance(current_trail.store, TrailSeries):
                mountain = current_trail.store.mountain
                following_path = current_trail.store.following
                mountain_list.append(mountain)
                if following_path != empty:
                    call_stack.push(following_path)
                else:
                    mountain_list.append([])
                    
        return (mountain_list,next_split)
    

    def collect_all_mount_split(self):
        assert isinstance(self.store, TrailSplit)

        paths = [self.store.path_top,self.store.path_bottom,self.store.path_follow]

        is_all_mount = False
        while not is_all_mount:
            for i in range(3):
                if paths[i] == Trail(None):
                    paths[i] = []
                elif isinstance(paths[i], TrailSeries):
                    paths[i] = paths[i].collect_all_mount_series()
                elif  isinstance(paths[i], TrailSplit):
                    paths[i] = paths[i].collect_all_mount_split()

            for i in range(3):
                is_all_mount = True
                if not isinstance(paths[i], Mountain):
                    is_all_mount = False

        
        print(paths)

        mount_list = paths[:-1]
        fol_path = paths[-1]
        mount_list = [path.extend(fol_path) for path in mount_list]
        
        return mount_list
        






    


    

        
if '__main__' == __name__:
    top_top = Mountain("top-top", 5, 3)
    top_bot = Mountain("top-bot", 3, 5)
    top_mid = Mountain("top-mid", 4, 7)
    bot_one = Mountain("bot-one", 2, 5)
    bot_two = Mountain("bot-two", 0, 0)
    final   = Mountain("final", 4, 4)
    trail = Trail(TrailSplit(
        Trail(TrailSplit(
            Trail(TrailSeries(top_top, Trail(None))),
            Trail(TrailSeries(top_bot, Trail(None))),
            Trail(TrailSeries(top_mid, Trail(None))),
        )),
        Trail(TrailSeries(bot_one, Trail(TrailSplit(
            Trail(TrailSeries(bot_two, Trail(None))),
            Trail(None),
            Trail(None),
        )))),
        Trail(TrailSeries(final, Trail(None)))
    ))
    trail_series = Trail(TrailSeries(top_top, Trail(TrailSeries(top_mid,Trail(TrailSplit(
            Trail(TrailSeries(bot_two, Trail(None))),
            Trail(None),
            Trail(None),
        ))))))
    
    trail_split = Trail(TrailSplit(
            Trail(TrailSeries(bot_two, Trail(None))),
            Trail(None),
            Trail(None),
        ))

    # res = trail.length_k_paths(3)
    res = trail_series.collect_all_mount_series()
    # print(res[0])
    next_split = res[1]
    print(next_split.collect_all_mount_split())
    # res = trail_split.collect_all_mount_split()
    # print(res[0])
    # print(res[1])