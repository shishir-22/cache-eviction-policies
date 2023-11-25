"""
This LRUCache implementation uses a doubly linked list and a hash map to efficiently manage a fixed-capacity cache with Least Recently Used (LRU) eviction policy.
Each cache entry is represented by a Node, containing a key, value, and pointers to the previous and next nodes in the linked list.
The cache is initialized with a specified capacity, and two sentinel nodes, "Head" and "Tail," to simplify boundary operations.

The __add_next_to_head method adds a given node next to the "Head" sentinel, maintaining the most recently used order.
The __remove_node_from_current_position method removes a node from its current position in the linked list.

The get method retrieves the value associated with a given key from the cache. If the key is present, the corresponding node is moved next to the "Head" sentinel to indicate its recent use.
If the key is not present, the method returns -1.

The put method inserts or updates a key-value pair in the cache. If the key is already present, the method updates the value and moves the corresponding node next to the "Head."
If the key is not present, and the cache is at full capacity, the least recently used node (at the "Tail" end) is evicted before adding the new node. If the cache has available capacity,
a new node is added next to the "Head."

Overall, this LRUCache implementation ensures efficient and constant-time access to cached items by employing a combination of a doubly linked list and a hash map,
effectively managing the recency and frequency of cache accesses.
"""
class Node:
    def __init__(self, key, value, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.hash_map = {}
        self.head = Node("Head", "Head")
        self.tail = Node("Tail", "Tail")
        self.head.next = self.tail
        self.tail.prev = self.head

    def __add_next_to_head(self, node):
        """
        Method to add the node next to head to maintain the recency
        """
        node.next = self.head.next
        node.prev = self.head
        self.head.next = node
        if node.next:
            node.next.prev = node

    def __remove_node_from_current_position(self, node):
        """
        Method to remove the node from current position
        """
        node.prev.next = node.next
        node.next.prev = node.prev

    def __print_cache(self):
        """
        Method to print the data of cache
        """
        mover = self.head
        print("Cache")
        while mover != self.tail:
            print(mover.key, mover.value)
            mover = mover.next

    def get(self, key: int) -> int:
        if self.hash_map.get(key):
            # Move the node next to head
            node = self.hash_map[key]
            # Remove the node from current place
            self.__remove_node_from_current_position(node)
            # Add the node next to the head
            self.__add_next_to_head(node)
            return node.value
        else:
            return -1
        

    def put(self, key: int, value: int) -> None:
        if self.hash_map.get(key):
            node = self.hash_map[key]
            # Update the value in existing node
            node.value = value
            # Remove the node from current place
            self.__remove_node_from_current_position(node)
            # Add the node next to the head
            self.__add_next_to_head(node)
        else:
            if len(self.hash_map) == self.capacity:
                # Remove the node from tail
                node_to_be_removed = self.tail.prev
                self.__remove_node_from_current_position(node_to_be_removed)
                del self.hash_map[node_to_be_removed.key]
                del node_to_be_removed

                # Add the new key and value
                self.hash_map[key] = Node(key, value)
                self.__add_next_to_head(self.hash_map[key])
            else:
                self.hash_map[key] = Node(key, value)
                # Add the node next to the head
                self.__add_next_to_head(self.hash_map[key])


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
