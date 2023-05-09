from mountain import Mountain
class MountainManager:
    '''
    A class that manages mountains.

    Type Arguments
    ---------------
    Mountain: The type of mountain to manage.

    Attributes
    ----------
    size: int
        The size of the hash table.
    keys: list
        The keys of the hash table.
    values: list
        The values of the hash table.

    Methods
    -------
    hash(key)
        Hashes the key and returns the hash value.
    rehash(previous_hash)
        Rehashes the previous hash and returns the new hash value.
    add_mountain(mountain)
        Add a mountain to the manager.
    remove_mountain(mountain)
        Remove a mountain from the manager  

    Complexity
    ----------
    Best Case Complexity: O(1)
    Worst Case Complexity: O(n)

    '''

    
    def hash(self, key):
        '''
        Hashes the key and returns the hash value.
        
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        '''
        return key % self.size 

    def rehash(self, previous_hash):
        '''
        Rehashes the previous hash and returns the new hash value.

        Best Case Complexity: O(1) 
        Worst Case Complexity: O(1)
        '''
        return (previous_hash + 1) % self.size
    

    def __init__(self, size = 10) -> None:
        '''
        Initializes the MountainManager with a given size.

        Best Case Complexity: O(1) 
        Worst Case Complexity: O(1) 
        '''
        self.size = size
        self.keys = [None] * self.size
        self.values = [None] * self.size


    def add_mountain(self, mountain: Mountain):
        '''
        Add a mountain to the manager.
        
        Best Case Complexity: O(1) when the first slot is empty
        Worst Case Complexity: O(n) when the first slot is full
        '''
        key = mountain.difficulty_level
        hash_value = self.hash(key)

        # If the slot is not empty, rehash until we find an empty slot
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
        
        Best Case Complexity: O(1) when the mountain is the first element in the list
        Worst Case Complexity: O(n) when the mountain is the last element in the list
        '''

      
        key = mountain.difficulty_level
        hash_value = self.hash(key)
       
        # If the slot is not empty, rehash until we find the mountain
        while self.keys[hash_value] is not None: 
            if self.keys[hash_value] == key:
                self.values[hash_value].remove(mountain)
                if len(self.values[hash_value]) == 0:
                    self.keys[hash_value] = None
                    self.values[hash_value] = None
                return
            hash_value = self.rehash(hash_value)

        


        

    def edit_mountain(self, old: Mountain, new: Mountain):
        '''
        Remove the old mountain and add the new mountain.
        
        Best Case Complexity: O(1) when the mountain is the first element in the list
        Worst Case Complexity: O(n) when the mountain is the last element in the list
        '''

        self.remove_mountain(old) 
        self.add_mountain(new)
        


    def mountains_with_difficulty(self, diff: int):
        '''
        Return a list of all mountains with this difficulty.
        
        Best Case Complexity: O(1) when the first slot is empty
        Worst Case Complexity: O(n) when the first slot is full
        '''
        
        result = []

        for i in range(self.size):
            if self.keys[i] is not None:
                for mountain in self.values[i]:
                    if mountain.difficulty_level == diff:
                        result.append(mountain)
        return result

        
    

       

    def group_by_difficulty(self):
        '''
        Returns a list of lists of all mountains, grouped by and sorted by ascending difficulty.
        
        Best Case Complexity: O(n) when the first slot is empty
        Worst Case Complexity: O(n) when the first slot is full
        '''
        
        groups = [[] for _ in range(self.size)]
        for i in range(self.size):
            if self.keys[i] is not None:
                groups[self.keys[i]].extend(self.values[i])
        return [sorted(group, key=lambda m: m.difficulty_level) for group in groups if group]