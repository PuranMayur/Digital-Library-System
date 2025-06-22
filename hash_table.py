from typing import Any, Tuple
from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        self.params = params
        self.size = 0
        self.load_factor = 0
        
        if collision_type == "Chain":
            self.table = [None] * params[1]
            self.table_size = params[1]
            self.z = params[0]
            
        elif collision_type == "Linear":
            self.table = [None] * params[1]
            self.table_size = params[1]
            self.z = params[0]
            
        else:
            self.table = [None] * params[3]
            self.table_size = params[3]
            self.z = params[0]
            self.z2 = params[1]
            self.c2 = params[2]
        pass
    
    def hash1(self, key):
        hash_val = 0
        if isinstance(key, tuple):
            key = key[0]
            
        for char in reversed(str(key)):
            if char.islower():
                val = ord(char) - ord('a')
            elif char.isupper():
                val = ord(char) - ord('A') + 26
            else:
                val = ord(char)
            hash_val = (hash_val * self.z + val) % self.table_size
        
        return hash_val

    def hash2(self, key):
        hash_val = 0
        if isinstance(key, tuple):
            key = key[0]
        
        for char in reversed(str(key)):
            if char.islower():
                val = ord(char) - ord('a')
            elif char.isupper():
                val = ord(char) - ord('A') + 26
            else:
                val = ord(char)
            hash_val = (hash_val * self.z2 + val) % self.c2
        
        step_size = self.c2 - hash_val
        return step_size
    
    def insert(self, x):
        
        if self.collision_type == "Chain":
            hash_value = self.hash1(x)
            if self.table[hash_value] is None:
                self.table[hash_value] = [x]
                self.size += 1
                self.load_factor = self.size / self.table_size
            else:
                if isinstance(self, HashSet):
                    if not any(element == x for element in self.table[hash_value]):
                        self.table[hash_value].append(x)
                        self.size += 1
                        self.load_factor = self.size / self.table_size
                elif isinstance(self, HashMap):
                    if not any(element[0] == x[0] for element in self.table[hash_value]):
                        self.table[hash_value].append(x)
                        self.size += 1
                        self.load_factor = self.size / self.table_size
                
        elif self.collision_type == "Linear":
            hash_value = self.hash1(x)
            if self.table[hash_value] is None:
                self.table[hash_value] = x
                self.size += 1
                self.load_factor = self.size / self.table_size
            else:
                if isinstance(self, HashSet):
                    if self.table[hash_value] == x:
                        return
                elif isinstance(self, HashMap):
                    if self.table[hash_value][0] == x[0]:
                        return
                i = 1
                marker = hash_value
                while self.table[(hash_value + i) % self.table_size] is not None:
                    if isinstance(self, HashSet):
                        if self.table[(hash_value + i) % self.table_size] == x:
                            return
                    elif isinstance(self, HashMap):
                        if self.table[(hash_value + i) % self.table_size][0] == x[0]:
                            return
                    i += 1
                    if (hash_value + i) % self.table_size == marker:
                        raise Exception("Table is full")
                self.table[(hash_value + i) % self.table_size] = x
                self.size += 1
                self.load_factor = self.size / self.table_size
                
        else:
            hash_value = self.hash1(x)
            if self.table[hash_value] is None:
                self.table[hash_value] = x
                self.size += 1
                self.load_factor = self.size / self.table_size
            else:
                if isinstance(self, HashSet):
                    if self.table[hash_value] == x:
                        return
                elif isinstance(self, HashMap):
                    if self.table[hash_value][0] == x[0]:
                        return
                hash_value2 = self.hash2(x)
                i = 1
                marker = hash_value
                while self.table[(hash_value + i * hash_value2) % self.table_size] is not None:
                    if isinstance(self, HashSet):
                        if self.table[(hash_value + i * hash_value2) % self.table_size] == x:
                            return
                    if isinstance(self, HashMap):
                        if self.table[(hash_value + i * hash_value2) % self.table_size][0] == x[0]:
                            return
                    i += 1
                    if (hash_value + i * hash_value2) % self.table_size == marker:
                        raise Exception("Table is full")
                self.table[(hash_value + i * hash_value2) % self.table_size] = x
                self.size += 1
                self.load_factor = self.size / self.table_size
                pass
    
    def find(self, key):
        
        if self.collision_type == "Chain":
            hash_value = self.hash1(key)
            if self.table[hash_value] is None:
                return None
            else:
                hash_list = self.table[hash_value]
                for element in hash_list:
                    if isinstance(self, HashSet):
                        if element == key:
                            return element
                    elif isinstance(self, HashMap):
                        if element[0] == key:
                            return element[1]
                return None
        
        elif self.collision_type == "Linear":
            hash_value = self.hash1(key)
            if isinstance(self, HashSet):
                if self.table[hash_value] is None:
                    return None
                elif self.table[hash_value] == key:
                    return self.table[hash_value]
                else:
                    i = 1
                    marker = hash_value
                    while self.table[(hash_value + i) % self.table_size] is not None:
                        if self.table[(hash_value + i) % self.table_size] == key:
                            return self.table[(hash_value + i) % self.table_size]
                        i += 1
                        if (hash_value + i) % self.table_size == marker:
                            return None
                    return None
            elif isinstance(self, HashMap):
                if self.table[hash_value] is None:
                    return None
                elif self.table[hash_value][0] == key:
                    return self.table[hash_value][1]
                else:
                    i = 1
                    marker = hash_value
                    while self.table[(hash_value + i) % self.table_size] is not None:
                        if self.table[(hash_value + i) % self.table_size][0] == key:
                            return self.table[(hash_value + i) % self.table_size][1]
                        i += 1
                        if (hash_value + i) % self.table_size == marker:
                            return None
                    return None
        
        else:
            hash_value = self.hash1(key)
            if isinstance(self, HashSet):
                if self.table[hash_value] is None:
                    return None
                elif self.table[hash_value] == key:
                    return self.table[hash_value]
                else:
                    hash_value2 = self.hash2(key)
                    i = 1
                    marker = hash_value
                    while self.table[(hash_value + i * hash_value2) % self.table_size] is not None:
                        if self.table[(hash_value + i * hash_value2) % self.table_size] == key:
                            return self.table[(hash_value + i * hash_value2) % self.table_size]
                        i += 1
                        if (hash_value + i * hash_value2) % self.table_size == marker:
                            return None
                    return None
                
            elif isinstance(self, HashMap):
                if self.table[hash_value] is None:
                    return None
                elif self.table[hash_value][0] == key:
                    return self.table[hash_value][1]
                else:
                    hash_value2 = self.hash2(key)
                    i = 1
                    marker = hash_value
                    while self.table[(hash_value + i * hash_value2) % self.table_size] is not None:
                        if self.table[(hash_value + i * hash_value2) % self.table_size][0] == key:
                            return self.table[(hash_value + i * hash_value2) % self.table_size][1]
                        i += 1
                        if (hash_value + i * hash_value2) % self.table_size == marker:
                            return None
                    return None
        pass
    
    def get_slot(self, key):   
        return self.hash1(key)
        pass
    
    def get_load(self):
        return self.load_factor
        pass
    
    def __str__(self):
        
        hash_list = []
        
        if self.collision_type == "Chain":
            #
            for element in self.table:
                if element is None:
                    hash_list.append("<EMPTY>")
                else:
                    if isinstance(self, HashSet):
                        
                        hash_list.append(" ; ".join(f"{sub_element}" for sub_element in element))
                    elif isinstance(self, HashMap):
                        
                        hash_list.append(" ; ".join(f"({sub_element[0]}, {sub_element[1]})" for sub_element in element))
            return " | ".join(hash_list)
        
        else:
            for element in self.table:
                if element is None:
                    hash_list.append("<EMPTY>")
                else:
                    if isinstance(self, HashSet):
                        # HashSet: display key only
                        hash_list.append(f"{element}")
                    elif isinstance(self, HashMap):
                        # HashMap: display (key, value)
                        hash_list.append(f"({element[0]}, {element[1]})")
            return " | ".join(hash_list)
        pass
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        new_size = get_next_size()
        new_table = [None] * new_size
        self.size = 0
        self.load_factor = 0
        self.table_size = new_size
        old_table = self.table[:]
        self.table = new_table
        
        if self.collision_type == "Chain":
            for element in old_table:
                if element is not None:
                    for sub_element in element:
                        self.insert(sub_element)
        
        else:
            for element in old_table:
                if element is not None:
                    self.insert(element)
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        pass
    
    def insert(self, key):
        super().insert(key)
        pass
    
    def find(self, key):
        temp = super().find(key)
        if temp is None:
            return False
        return True
        pass
    
    def get_slot(self, key):
        return super().get_slot(key)
        pass
    
    def get_load(self):
        return super().get_load()
        pass
    
    def __str__(self):
        return super().__str__()
        pass
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        pass
    
    def insert(self, x):
        # x = (key, value)
        super().insert(x)
        pass
    
    def find(self, key):
        return super().find(key)
        pass
    
    def get_slot(self, key):
        return super().get_slot(key)
        pass
    
    def get_load(self):
        return super().get_load()
        pass
    
    def __str__(self):
        return super().__str__()
        pass