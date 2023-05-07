from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.referential_array import ArrayR
from data_structures.hash_table import LinearProbeTable, FullError

K = TypeVar('K')
K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        Create a new Double Hash Table.

        :complexity: O(N) where N is the table size.
        __init__(self, sizes=None, internal_sizes=None) , create the underlying array. If sizes is not None, the provided array should replace the existing TABLE_SIZES to decide the size of the top-level hash table. If internal_sizes is not None, the provided array should replace the existing TABLE_SIZES for the internal hash tables
        """
        if sizes is not None:
            self.sizes = sizes
        else:
            self.sized = self.TABLE_SIZES

        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.size_index = 0 
        self.count = 0
        self.array:ArrayR[tuple[K, V]] = ArrayR(self.sizes[self.size_index]) 

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value
    
    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        return the:
        Index to access in the top-level table, followed by Index to access in the low-level table In a tuple.

        Your linear probe method should create the internal hash table if is_insert is true and this is the first pair with key1.
        """
        # Initial position
        top_level_position = self.hash1(key1)

        for _ in range(self.table_size):
            if self.array[top_level_position] is None:
                # Empty spot. Am I upserting or retrieving?
                if is_insert:
                    self.array[top_level_position] = LinearProbeTable(self.internal_sizes[self.size_index])
                    self.array[top_level_position].hash = lambda k: self.hash2(k, self.array[top_level_position])  # override the hashfuction
                else:
                    # item doesn't exist
                    raise KeyError(key1)
            elif self.array[top_level_position][0] == key1: # Found the top level position
                underlying_linear_hash_table = self.array[top_level_position]
                underlying_linear_hash_table._linear_probe(key2,is_insert)

                # found the bottom-level position as well
                return (top_level_position,underlying_linear_hash_table.position)
            else: 
                # Taken by something else. Time to linear probe.
                position = (position + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
        else:
            raise KeyError(key1)
        
    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        if key is None:
            for i in range(len(self.array)):
                if self.array[i] is not None:
                    yield self.array[i][0]
        else:
            for i in range(len(self.array)):
                if self.array[i] is not None:
                    if self.array[i][0] == key:
                        for j in range(len(self.array[i][1])):
                            if self.array[i][1][j] is not None:
                                yield self.array[i][1][j][0]

                                

        

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        If key = None, return all top-level keys in the hash table
        If key != None, return all low-level keys in the sub-table of top-level key
        """

        

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        
        """
        #return an iterator that yields the keys/values one by one rather than searching the entire table at the start.

      

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        #If key = None, return all values in all entries of the hash table
        #If key != None, restrict to all values in the sub-table of top-level key






    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, False)
        return self.array[position1][position2][1]
        
        

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        
        """
        position1, position2 = self._linear_probe(key[0], key[1], True)
        self.array[position1][position2] = (key[0], data)

        
    

        

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
            
        

        
    
        

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        
        
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

        

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count
       

    
    
    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """

        
        
if '__main__' == __name__:
    
    # dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
    # dt.hash1 = lambda k: ord(k[0]) % 12
    # dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

    # dt["Tim", "Jen"] = 1
    # dt["Amy", "Ben"] = 2
    # dt["May", "Ben"] = 3
    # dt["Ivy", "Jen"] = 4
    # dt["May", "Tom"] = 5
    # dt["Tim", "Bob"] = 6
    # self.assertRaises(KeyError, lambda: dt._linear_probe("May", "Jim", False))
    # self.assertEqual(dt._linear_probe("May", "Jim", True), (6, 1))
    # dt["May", "Jim"] = 7 # Linear probing on internal table
    # self.assertEqual(dt._linear_probe("May", "Jim", False), (6, 1))
    # self.assertRaises(KeyError, lambda: dt._linear_probe("Het", "Liz", False))
    # self.assertEqual(dt._linear_probe("Het", "Liz", True), (2, 2))
    # dt["Het", "Liz"] = 8 # Linear probing on external table
    # self.assertEqual(dt._linear_probe("Het", "Liz", False), (2, 2))
    print('Hi')
    pass
