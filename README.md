# Hash Map Implementations
This repository contains Python implementations of the hash map data structure using two different collision resolution strategies: Separate Chaining and Quadratic Probing. Both implementations utilize a dynamic array and hash functions to efficiently store and retrieve key-value pairs.

## Overview
### Hash Map
A hash map is a data structure that stores key-value pairs. It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found. Ideally, the hash function will assign each key to a unique bucket, but this situation is rarely achievable. Therefore, collision resolution strategies become essential to handle cases where the hash function maps two or more keys to the same bucket.

### Dynamic Array
The DynamicArray class is a contiguous storage mechanism that grows automatically as more elements are added. It supports operations like append, pop, swap, get_at_index, and set_at_index.

# Separate Chaining (hash_map_sc.py)
This implementation of the hash map uses Separate Chaining as the collision resolution technique. In Separate Chaining, each bucket of the hash table is independent, and has some sort of list of entries with the same index. Our implementation uses a singly linked list for this purpose.

## Features
* Insertion (put): Adds a new key-value pair to the hash map. If the key already exists, its value is updated.
* Search (get, contains_key): Retrieves the value associated with a given key. Checks if a given key is present in the hash map.
* Deletion (remove): Removes a key-value pair from the hash map.
* Resizing (resize_table): Increases the size of the hash map and rehashes existing key-value pairs into the new space.
* Load Factor Calculation (table_load): Calculates the current load factor of the hash map.
* Bucket Management (empty_buckets): Counts the number of empty buckets in the hash map.

### Implementation Details
* The HashMap class stores key-value pairs in a DynamicArray, each element of which is a LinkedList.
* Each LinkedList can contain multiple SLNode instances if multiple keys hash to the same index.
* The SLNode class represents an element in the singly linked list, containing the key, value, and a pointer to the next node.
* The LinkedList class provides methods for insertion, deletion, and search operations within the list.

# Quadratic Probing
This implementation of the hash map uses Quadratic Probing as the collision resolution technique. In Quadratic Probing, when a collision occurs, the algorithm tries to find the next open slot using a quadratic function of the number of tries until an empty slot is found.

## Features
* Insertion (put): Inserts a new key-value pair into the hash map. If the key already exists, its value is updated. The hash map is resized if the load factor becomes too high.
* Search (get, contains_key): Retrieves the value associated with a given key and checks if a given key is present in the hash map.
* Deletion (remove): Removes a key-value pair from the hash map by marking its slot as a tombstone.
* Resizing (resize_table): Increases the size of the hash map to a new capacity and rehashes existing key-value pairs into the new space.
* Load Factor Calculation (table_load): Calculates the current load factor of the hash map.
* Bucket Management (empty_buckets): Counts the number of empty buckets in the hash map.

### Implementation Details
* The HashMap class stores key-value pairs in a DynamicArray, each element of which can be a HashEntry or None.
* Each HashEntry stores a key, a value, and a boolean flag is_tombstone to indicate if the entry is active or has been logically removed (tombstone).
* Collision resolution is handled by Quadratic Probing. When a collision occurs, the algorithm computes the next index based on a quadratic function of the number of tries.
* The hash map supports resizing when the load factor exceeds a certain threshold, ensuring that the operations remain efficient even as more elements are added.


## Made By
* Rob Cosentino

### Contact:
* robert.cosentino1@gmail.com
* linkedin.com/in/rob-cosentino/
