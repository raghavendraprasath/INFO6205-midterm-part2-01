from typing import TypeVar, Generic, List, Iterator, Callable, Optional, Any, Union

T = TypeVar('T')  # Generic type parameter

class MinPQ(Generic[T]):
    """
    The MinPQ class represents a priority queue of generic keys.
    It supports the usual insert and delete-the-minimum operations,
    along with methods for peeking at the minimum key, testing if the 
    priority queue is empty, and iterating through the keys.
    
    This implementation uses a binary heap.
    The insert and delete-the-minimum operations take O(log n) amortized time,
    where n is the number of elements in the priority queue. This is an amortized bound
    (and not a worst-case bound) because of array resizing operations.
    The min, size, and is_empty operations take O(1) time in the worst case.
    Construction takes time proportional to the specified capacity or the
    number of items used to initialize the data structure.
    """
    
    def __init__(self, init_capacity_or_keys=None, comparator=None):
        """
        Initialize a new MinPQ.
        
        Args:
            init_capacity_or_keys: Either the initial capacity or a list of keys
            comparator: A function that compares two keys
        """
        self.comparator = comparator
        
        # Handle different constructor patterns
        if init_capacity_or_keys is None:
            # Default constructor: MinPQ()
            init_capacity = 1
            keys_to_use = None
        elif isinstance(init_capacity_or_keys, int):
            # Constructor with capacity: MinPQ(capacity)
            init_capacity = init_capacity_or_keys
            keys_to_use = None
        else:
            # Constructor with keys: MinPQ(keys)
            init_capacity = 1
            keys_to_use = init_capacity_or_keys
        
        # pq[0] is not used, indices start at 1
        self.pq = [None] * (init_capacity + 1)
        self.n = 0  # number of items on priority queue
        
        if keys_to_use is not None:
            self.n = len(keys_to_use)
            self.pq = [None] * (len(keys_to_use) + 1)
            for i in range(self.n):
                self.pq[i+1] = keys_to_use[i]
            for k in range(self.n // 2, 0, -1):
                self._sink(k)
            assert self._is_min_heap()
    
    def is_empty(self) -> bool:
        """
        Returns True if this priority queue is empty.
        
        Returns:
            True if this priority queue is empty, False otherwise
        """
        return self.n == 0
    
    def size(self) -> int:
        """
        Returns the number of keys on this priority queue.
        
        Returns:
            The number of keys on this priority queue
        """
        return self.n
    
    def min(self) -> T:
        """
        Returns a smallest key on this priority queue.
        
        Returns:
            A smallest key on this priority queue
        
        Raises:
            ValueError: If this priority queue is empty
        """
        if self.is_empty():
            raise ValueError("Priority queue underflow")
        return self.pq[1]
    
    def _resize(self, capacity: int):
        """
        Resize the underlying array to have the given capacity.
        
        Args:
            capacity: The new capacity of the array
        """
        assert capacity > self.n
        temp = [None] * capacity
        for i in range(1, self.n + 1):
            temp[i] = self.pq[i]
        self.pq = temp
    
    def insert(self, x: T):
        """
        Adds a new key to this priority queue.
        
        Args:
            x: The key to add to this priority queue
        """
        # double size of array if necessary
        if self.n == len(self.pq) - 1:
            self._resize(2 * len(self.pq))
        
        # add x, and percolate it up to maintain heap invariant
        self.n += 1
        self.pq[self.n] = x
        self._swim(self.n)
        assert self._is_min_heap()
    
    def del_min(self) -> T:
        """
        Removes and returns a smallest key on this priority queue.
        
        Returns:
            A smallest key on this priority queue
        
        Raises:
            ValueError: If this priority queue is empty
        """
        if self.is_empty():
            raise ValueError("Priority queue underflow")
        min_element = self.pq[1]
        self._exch(1, self.n)
        self.n -= 1
        self._sink(1)
        self.pq[self.n+1] = None  # to avoid loitering and help with garbage collection
        if self.n > 0 and self.n == (len(self.pq) - 1) // 4:
            self._resize(len(self.pq) // 2)
        assert self._is_min_heap()
        return min_element
    
    def _swim(self, k: int):
        """
        Move the element at position k up to restore the heap invariant.
        
        Args:
            k: The position of the element to swim
        """
        # STUDENT TODO: Implement the swim method
        pass
    
    def _sink(self, k: int):
        """
        Move the element at position k down to restore the heap invariant.
        
        Args:
            k: The position of the element to sink
        """
        # STUDENT TODO: Implement the sink method
        pass
    
    def _greater(self, i: int, j: int) -> bool:
        """
        Check if pq[i] > pq[j].
        
        Args:
            i: The first index
            j: The second index
        
        Returns:
            True if pq[i] > pq[j], False otherwise
        """
        if self.comparator is None:
            return self.pq[i] > self.pq[j]
        else:
            return self.comparator(self.pq[i], self.pq[j]) > 0
    
    def _exch(self, i: int, j: int):
        """
        Exchange the elements at positions i and j.
        
        Args:
            i: The first position
            j: The second position
        """
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
    
    def _is_min_heap(self) -> bool:
        """
        Check if the heap is a valid min heap.
        
        Returns:
            True if the heap is a valid min heap, False otherwise
        """
        for i in range(1, self.n + 1):
            if self.pq[i] is None:
                return False
        for i in range(self.n + 1, len(self.pq)):
            if self.pq[i] is not None:
                return False
        if self.pq[0] is not None:
            return False
        return self._is_min_heap_ordered(1)
    
    def _is_min_heap_ordered(self, k: int) -> bool:
        """
        Check if the subtree rooted at k is a valid min heap.
        
        Args:
            k: The root of the subtree to check
        
        Returns:
            True if the subtree is a valid min heap, False otherwise
        """
        if k > self.n:
            return True
        left = 2 * k
        right = 2 * k + 1
        if left <= self.n and self._greater(k, left):
            return False
        if right <= self.n and self._greater(k, right):
            return False
        return self._is_min_heap_ordered(left) and self._is_min_heap_ordered(right)
    
    def __iter__(self) -> Iterator[T]:
        """
        Returns an iterator that iterates over the keys on this priority queue
        in ascending order.
        
        Returns:
            An iterator that iterates over the keys in ascending order
        """
        return self.HeapIterator(self)
    
    class HeapIterator:
        """
        Iterator for the MinPQ class.
        """
        
        def __init__(self, pq):
            """
            Initialize a new HeapIterator.
            
            Args:
                pq: The MinPQ to iterate over
            """
            if pq.comparator is None:
                self.copy = MinPQ(pq.size())
            else:
                self.copy = MinPQ(pq.size(), pq.comparator)
            for i in range(1, pq.n + 1):
                self.copy.insert(pq.pq[i])
        
        def __iter__(self):
            """
            Returns self as the iterator.
            
            Returns:
                Self as the iterator
            """
            return self
        
        def __next__(self):
            """
            Returns the next element in the iteration.
            
            Returns:
                The next element in the iteration
            
            Raises:
                StopIteration: If there are no more elements
            """
            if self.copy.is_empty():
                raise StopIteration
            return self.copy.del_min()