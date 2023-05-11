from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        self.table = Subtable(0)
        self.count = 0
        self.level = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        return self.table[key]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        try:
            _ = self.table[key]
        except KeyError:
            self.count+=1

        self.table[key] = value

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        del self.table[key]
        self.count-=1

    def __len__(self):
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        return self.table.get_position_seq(key)

    def __contains__(self, key: K) -> bool:
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
        

class Subtable():
    TABLE_SIZE = 27
    def __init__(self,level) -> None:
        self.array = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1
    
    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        position = self.hash(key)
        # base case 1
        if self.array[position] is None:
            raise KeyError(key)
        
        old_key, old_value = self.array[position]
        # base case 2
        if not isinstance(old_value,Subtable):
            if old_key==key:
                # converge when it hits a value
                return old_value
            else:
                raise KeyError(key)
        else:
            # continue searching
            sub_table = old_value
            return sub_table[key]
    
    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        try:
            self.get_position_seq(key)  # raises KeyError if key doesnt exist
        except KeyError:
            self.count+=1

        position = self.hash(key)
        # base case 1
        if self.array[position] is None:
            self.array[position] = (key,value)
        
        old_key, old_value = self.array[position]
        if not isinstance(old_value,Subtable):
            # base case 2
            if old_key==key:
                # converge when it hits a value
                # overwrite old value
                self.array[position] = (key,value)
            
            else:
                self.array[position] = (key[:self.level+1],Subtable(self.level+1))
                # reinsert
                self.array[position][1][old_key] = old_value
                # continue searching
                self.array[position][1][key] = value
        else:
            # continue searching
            sub_table = old_value
            sub_table[key] = value
    
    def get_position_seq(self,key) -> list[int]:
        position = self.hash(key)
        # base case 1
        if self.array[position] is None:
            raise KeyError(key)
        
        old_key, old_value = self.array[position]
        # base case 2
        if not isinstance(old_value,Subtable):
            if old_key==key:
                # converge when it hits a value
                return [position]
            else:
                raise KeyError(key)
        else:
            # continue searching
            sub_table = old_value
            return [position] + sub_table.get_position_seq(key)
        
    def __delitem__(self,key):
        pos_seq = self.get_position_seq(key)  # raises KeyError if key doesnt exist
        
        next_position = pos_seq[0]
        if len(pos_seq) == 1: # no subtable, just delete
            self.array[next_position] = None
        else:
            next_subtable = self.array[next_position][1]
            # print(next_subtable.count,"here")
            # for item in next_subtable.array:
            #     print(next_subtable.count,"here",item,next_subtable.level)
            del next_subtable[key]
            next_subtable.count-=1

            if next_subtable.count == 1:
                for item in next_subtable.array:
                    if item is not None:
                        old_key_value_tuple = item
                        break
                self.array[next_position] = old_key_value_tuple