"""
This LFUCache implementation utilizes a doubly linked list and two hash maps to effectively manage a fixed-capacity cache with Least Frequently Used (LFU) eviction policy.
Each cache entry is represented by a Node, containing a key, value, frequency, and pointers to the previous and next nodes in the linked list.
The cache is initialized with a specified capacity, and two sentinel nodes, "Head" and "Tail," to simplify boundary operations.

The __add_node_in_given_freq_dll method adds a given node to the doubly linked list corresponding to its frequency, maintaining the order based on frequency.
The __remove_the_given_node method removes a node from its current position in the linked list.

The get method retrieves the value associated with a given key from the cache. If the key is present, the corresponding node's frequency is incremented, and the node is moved to the respective frequency list.
If the key is not present, the method returns -1.

The put method inserts or updates a key-value pair in the cache. If the key is already present, the method updates the value and moves the corresponding node to the appropriate frequency list.
If the key is not present, and the cache is at full capacity, the least frequently used node is evicted before adding the new node. If the cache has available capacity,
a new node is added to the frequency list with a frequency of 1.

Overall, this LFUCache implementation ensures efficient and constant-time access to cached items by employing a combination of a doubly linked list and two hash maps,
effectively managing the frequency and recency of cache accesses.
"""

class Node:
    def __init__(self, key, value, next=None, prev=None):
        self.key = key
        self.value = value
        self.freq = 1
        self.next = next
        self.prev = prev


class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_node_hash = {} # {key: node}
        self.freq_dll_hash = {} # {freq: (head, tail)}
        self.min_freq = 1

    def __print_cache(self):
        """
        Method to print the content of cache
        """
        print("Cache")
        for freq, dll in self.freq_dll_hash.items():
            print("Freq: ", freq)
            curr_freq_node = dll[0]
            while curr_freq_node:
                print(curr_freq_node.key, curr_freq_node.value)
                curr_freq_node = curr_freq_node.next


    def __reset_min_freq(self):
        """
        Method to reset the min freq value
        """
        for freq, dll in sorted(self.freq_dll_hash.items()):
            head, tail = dll[0], dll[1]
            if head.next != tail:
                self.min_freq = freq
                return



    def __insert_node_next_to_head(self, node, head):
        """
        Method to insert the given node next to the given head
        """
        node.prev = head
        node.next = head.next
        head.next = node
        node.next.prev = node

    def __remove_the_given_node(self, node):
        """
        Method to remove the given node from DLL
        """
        node.prev.next = node.next
        node.next.prev = node.prev

    def __add_node_in_given_freq_dll(self, node, freq):
        """
        Method to add the node in the given freq DLL
        """
        if self.freq_dll_hash.get(freq):
            head, tail = self.freq_dll_hash[freq]
        else:
            head = Node("Head", "Head")
            tail = Node("Tail", "Tail")
            head.next = tail
            tail.prev = head
            self.freq_dll_hash[freq] = (head, tail)
        # Insert the node next to head of given freq
        self.__insert_node_next_to_head(node, head)

    def __increment_the_freq_of_node(self, node):
        """
        Method to increment the freq of given node and insert it in new freq DLL
        """
        # Increment the freq of node and move to the respective freq DLL
        old_freq = node.freq
        node.freq += 1

        # Move the node to the DLL of corresponding freq
        freq = node.freq
        # Remove the node from current freq DLL
        self.__remove_the_given_node(node)

        # Add the key to DLL of given freq
        self.__add_node_in_given_freq_dll(node, freq) 

        # Update the min freq
        self.__reset_min_freq()


    def get(self, key: int) -> int:
        """
        Method to get the key value from cache
        """
        if self.key_node_hash.get(key):
            node = self.key_node_hash[key]
            self.__increment_the_freq_of_node(node)
            return node.value

        else:
            return -1


    def put(self, key: int, value: int) -> None:
        """
        Method to put the key value in cache
        """
        if self.key_node_hash.get(key):
            # Update the key value and frequency
            node = self.key_node_hash[key]
            node.value = value
            self.__increment_the_freq_of_node(node)
        else:
            if len(self.key_node_hash) == self.capacity:
                # Remove the key with least frequency, if two keys have same freq then
                # remove the LRU key
                head, tail = self.freq_dll_hash[self.min_freq]
                # Remove the node left to the tail of DLL
                node = tail.prev
                self.__remove_the_given_node(node)
                key_to_remove = node.key
                del self.key_node_hash[key_to_remove]
                del node

                # Add the new key to DLL of freq 1
                node = Node(key, value)
                self.key_node_hash[key] = node
                self.__add_node_in_given_freq_dll(node, 1) 
                self.min_freq = 1
            else:
                # Add new key
                node = Node(key, value)
                self.key_node_hash[key] = node

                # Add the key to DLL of freq 1
                self.__add_node_in_given_freq_dll(node, 1)    
                self.min_freq = 1
    

        


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
