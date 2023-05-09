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
        pass

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
        Return true if a new key is inserted.
        """
        position = self.hash(key)
        # base case 1
        if self.array[position] is None:
            self.array[position] = (key,value)
            self.count += 1
        
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

if '__main__' == __name__:
    ih = InfiniteHashTable()
    ih["lin"] = 1
    ih["leg"] = 2
    print(ih.get_location("lin"))
    print(ih.get_location("lin")== [4, 1])
    print(ih.get_location("leg")== [4, 23])
    print(len(ih)== 2)
    ih["mine"] = 3
    ih["linked"] = 4
    print(ih.get_location("mine")== [5])
    print(ih.get_location("lin")== [4, 1, 6, 26])
    print(ih.get_location("linked")== [4, 1, 6, 3])
    print(len(ih), 4)
    ih["limp"] = 5
    ih["mining"] = 6
    print(ih.get_location("limp")== [4, 1, 5])
    print(ih.get_location("mine")== [5, 1, 6, 23])
    print(ih.get_location("mining")== [5, 1, 6, 1])
    print(len(ih), 6)
    ih["jake"] = 7
    ih["linger"] = 8
    print(ih.get_location("jake")== [2])
    print(ih.get_location("linger")== [4, 1, 6, 25])
    print(len(ih)== 8)
