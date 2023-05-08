from mountain import Mountain




class MountainManager:

    def hash(self, key):
        return key % self.size

    def rehash(self, previous_hash):
        return (previous_hash + 1) % self.size
    

    def __init__(self, size = 10) -> None:
        self.size = size
        self.keys = [None] * self.size
        self.values = [None] * self.size


    def add_mountain(self, mountain: Mountain):
        key = mountain.difficulty_level
        hash_value = self.hash(key)

        # If the key is not already in the table, add it to the first available slot
        while self.keys[hash_value] is not None and self.keys[hash_value] != key:
            hash_value = self.rehash(hash_value)

        if self.keys[hash_value] is None:
            self.keys[hash_value] = key
            self.values[hash_value] = [mountain]
        else:
            self.values[hash_value].append(mountain)

    def remove_mountain(self, mountain: Mountain):
        '''
        Remove a mountain from the manager
        '''

        


        

    def edit_mountain(self, old: Mountain, new: Mountain):
        '''Remove the old mountain and add the new mountain.'''
        


    def mountains_with_difficulty(self, diff: int):
        '''Return a list of all mountains with this difficulty.'''
        
    

       

    def group_by_difficulty(self):
        '''Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.'''
        
        