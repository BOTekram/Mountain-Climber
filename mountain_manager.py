from mountain import Mountain




class MountainManager:

    def hash(self, key):
        '''Hashes the key and returns the hash value.'''
        return key % self.size

    def rehash(self, previous_hash):
        '''Rehashes the previous hash and returns the new hash value.'''
        return (previous_hash + 1) % self.size
    

    def __init__(self, size = 10) -> None:
        '''Initializes the MountainManager with a given size.'''
        self.size = size
        self.keys = [None] * self.size
        self.values = [None] * self.size


    def add_mountain(self, mountain: Mountain):
        '''Add a mountain to the manager.'''
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
        '''Remove a mountain from the manager'''

      
        key = mountain.difficulty_level
        hash_value = self.hash(key)
       
        while self.keys[hash_value] is not None:
            if self.keys[hash_value] == key:
                self.values[hash_value].remove(mountain)
                if len(self.values[hash_value]) == 0:
                    self.keys[hash_value] = None
                    self.values[hash_value] = None
                return
            hash_value = self.rehash(hash_value)

        


        

    def edit_mountain(self, old: Mountain, new: Mountain):
        '''Remove the old mountain and add the new mountain.'''

        self.remove_mountain(old)
        self.add_mountain(new)
        


    def mountains_with_difficulty(self, diff: int):
        '''Return a list of all mountains with this difficulty.'''
        
        result = []
        for i in range(self.size):
            if self.keys[i] is not None:
                for mountain in self.values[i]:
                    if mountain.difficulty_level == diff:
                        result.append(mountain)
        return result

        
    

       

    def group_by_difficulty(self):
        '''Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.'''
        
        groups = [[] for _ in range(self.size)]
        for i in range(self.size):
            if self.keys[i] is not None:
                groups[self.keys[i]].extend(self.values[i])
        return [sorted(group, key=lambda m: m.difficulty_level) for group in groups if group]