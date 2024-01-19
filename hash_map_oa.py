# Name: Robert Cosentino
# OSU Email: cosentir@orgeonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/23
# Description: This file contains a HashMap class that utilizes open addressing
#           and quadratic probing to resolve collisions.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Inserts a key/value pair into the HashTable and resizes the table if necessary.
        If value already exists, it is updated. Utilizes open addressing

        :param key: the string associated with a particular value
        :param value: the object value that is associated with a particular key
        """
        # Check if resize is necessary
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Initialize position and prode count
        initial_position = self._hash_function(key) % self._capacity
        probe_count = 0
        position = initial_position

        # Looping until we find suitable bucket
        while True:
            current_entry = self._buckets[position]

            # if bucket is empty, it is valid for insertion
            if not current_entry:
                self._buckets[position] = HashEntry(key, value)
                self._size += 1
                return

            # current slot has matching key and isn't tombstone - value is updated
            elif current_entry.key == key and not current_entry.is_tombstone:
                current_entry.value = value
                return

            # Current slot is tombstone and is reused
            elif current_entry.is_tombstone:
                current_entry.key = key
                current_entry.value = value
                current_entry.is_tombstone = False
                self._size += 1
                return

            # At this point, current slot is occupied and we will probe further
            probe_count += 1
            position = (initial_position + probe_count ** 2) % self._capacity

    def table_load(self) -> float:
        """
        Computes load factor of the HashTable

        :return: Current load factor, as float
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Determines the number of empty buckets within the hash table

        :return: an integer that indicates the number of empty buckets
        """
        count = 0
        # Iterating over each bucket
        for i in range(self._buckets.length()):

            # Determining if the bucket is empty
            if self._buckets[i] is None:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hashtable to a new capacity

        :param new_capacity: Specified new capacity for the hashtable
        """
        # New capacity must be larger than current size
        if new_capacity < self._size:
            return

        new_capacity = self._next_prime(new_capacity)
        # old buckets stored for reinsertion
        old_buckets = self._buckets

        # New buckets initialized
        self._buckets = DynamicArray()
        for index in range(new_capacity):
            self._buckets.append(None)
        self._capacity = new_capacity
        self._size = 0

        # Rehashing and inserting old values into the new table
        for i in range(old_buckets.length()):
            entry = old_buckets[i]
            if entry is not None:
                self.put(entry.key, entry.value)

    def get(self, key: str) -> object:
        """
        Provides the value associated the specified key

        :param key: the key string that is associated with a particular value

        :return: the value associated with the specified key or None
        """
        # Determine initial index with the hash function
        index = self._hash_function(key) % self._capacity
        probe_count = 0

        while True:
            # calculating current index
            current_index = (index + probe_count ** 2) % self._capacity
            current_entry = self._buckets[current_index]

            # If the bucket is empty, no key
            if current_entry is None:
                return None
            # If the bucket has the specified key/isn't a tombstone, return the value
            if current_entry.key == key and not current_entry.is_tombstone:
                return current_entry.value
            # Incrementing probe count
            probe_count += 1

            # All buckets probed without key discovery
            if probe_count == self._capacity:
                return None

    def contains_key(self, key: str) -> bool:
        """
        Determines if a specified key is contained within the hash table

        :param key: the key to be sought after in the hash table

        :return: True if key is present, False if it is not
        """
        # Computing initial index
        index = self._hash_function(key) % self._capacity
        probe_count = 0

        while True:
            current_index = (index + probe_count ** 2) % self._capacity
            current_entry = self._buckets[current_index]

            # slot is empty, key is not present
            if current_entry is None:
                return False
            # slot has the desired key/isn't a tombstone
            if current_entry.key == key and not current_entry.is_tombstone:
                return True

            probe_count += 1

            # All buckets probed without discovery
            if probe_count == self._capacity:
                return False

    def remove(self, key: str) -> None:
        """
        Removes the specified key from the hash table

        :param key: specified key to be removed
        """
        # Determining initial index
        index = self._hash_function(key) % self._capacity
        probe_count = 0

        while True:
            # Determining current index
            curr_index = (index + probe_count ** 2) % self._capacity
            curr_entry = self._buckets[curr_index]

            # slot is empty, key is not present
            if curr_entry is None:
                return
            # slot has the specified key, mark it as tombstone and reduce size
            if curr_entry.key == key and not curr_entry.is_tombstone:
                curr_entry.is_tombstone = True
                self._size -= 1
                return

            # increment probe
            probe_count += 1

            # All buckets have been checked
            if probe_count == self._capacity:
                break

    def clear(self) -> None:
        """
        Clears all of the buckets in the hash table
        :return:
        """
        # Iterating over ever bucket
        for i in range(self._buckets.length()):
            # Making each bucket empty
            self._buckets[i] = None
        self._size = 0


    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieves all key/value pairs in the hash table

        :return: DA containing tuples of key/value pairs
        """
        # Initialize DA for the pairs
        keys_values_arr = DynamicArray()

        # Iterating over every bucket
        for bucket in range(self._buckets.length()):
            entry = self._buckets[bucket]

            # Checking for bucket validity
            if entry is not None and not entry.is_tombstone:
                keys_values_arr.append((entry.key, entry.value))

        return keys_values_arr


    def __iter__(self):
        """
        Initializes an iterator for the hash table

        :return: the initialized iterator
        """
        # Resetting iterator index to beginning of the table
        self._iter_index = 0
        return self
        pass

    def __next__(self):
        """
        Provides the next valid bucket in the hash table while iterating

        :return: the next valid bucket in the hash table
        """
        while self._iter_index < self._buckets.length():
            # Retrieving current bucket
            bucket = self._buckets[self._iter_index]
            self._iter_index += 1
            if bucket and not bucket.is_tombstone:
                return bucket

        raise StopIteration



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
