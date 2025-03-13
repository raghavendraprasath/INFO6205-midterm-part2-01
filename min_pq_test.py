import unittest
from min_pq import MinPQ

class MinPQTest(unittest.TestCase):
    def setUp(self):
        self.min_pq = MinPQ()
    
    def test_insert_and_del_min(self):
        self.min_pq.insert(3)
        self.min_pq.insert(1)
        self.min_pq.insert(4)
        self.min_pq.insert(2)
        self.assertEqual(1, self.min_pq.del_min())
        self.assertEqual(2, self.min_pq.del_min())
        self.assertEqual(3, self.min_pq.del_min())
        self.assertEqual(4, self.min_pq.del_min())
    
    def test_is_empty(self):
        self.assertTrue(self.min_pq.is_empty())
        self.min_pq.insert(1)
        self.assertFalse(self.min_pq.is_empty())
        self.min_pq.del_min()
        self.assertTrue(self.min_pq.is_empty())
    
    def test_size(self):
        self.assertEqual(0, self.min_pq.size())
        self.min_pq.insert(1)
        self.assertEqual(1, self.min_pq.size())
        self.min_pq.insert(2)
        self.assertEqual(2, self.min_pq.size())
        self.min_pq.del_min()
        self.assertEqual(1, self.min_pq.size())
    
    def test_min(self):
        self.min_pq.insert(5)
        self.min_pq.insert(2)
        self.min_pq.insert(8)
        self.assertEqual(2, self.min_pq.min())
    
    def test_min_throws_exception_when_empty(self):
        with self.assertRaises(ValueError):
            self.min_pq.min()
    
    def test_del_min_throws_exception_when_empty(self):
        with self.assertRaises(ValueError):
            self.min_pq.del_min()
    
    def test_constructor_with_initial_capacity(self):
        min_pq_with_capacity = MinPQ(5)
        min_pq_with_capacity.insert(3)
        min_pq_with_capacity.insert(1)
        self.assertEqual(1, min_pq_with_capacity.del_min())
    
    def test_constructor_with_comparator(self):
        reverse_comparator = lambda a, b: b - a
        min_pq_with_comparator = MinPQ(comparator=reverse_comparator)
        min_pq_with_comparator.insert(3)
        min_pq_with_comparator.insert(1)
        self.assertEqual(3, min_pq_with_comparator.del_min())
    
    def test_constructor_with_array(self):
        keys = [4, 2, 5, 1, 3]
        min_pq_from_array = MinPQ(keys)
        self.assertEqual(1, min_pq_from_array.del_min())
        self.assertEqual(2, min_pq_from_array.del_min())
        self.assertEqual(3, min_pq_from_array.del_min())
        self.assertEqual(4, min_pq_from_array.del_min())
        self.assertEqual(5, min_pq_from_array.del_min())
    
    def test_iterator(self):
        self.min_pq.insert(3)
        self.min_pq.insert(1)
        self.min_pq.insert(4)
        self.min_pq.insert(2)
        iterator = iter(self.min_pq)
        self.assertEqual(1, next(iterator))
        self.assertEqual(2, next(iterator))
        self.assertEqual(3, next(iterator))
        self.assertEqual(4, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)
    
    def test_iterator_remove_throws_exception(self):
        self.min_pq.insert(1)
        iterator = iter(self.min_pq)
        next(iterator)
        with self.assertRaises(AttributeError):
            iterator.remove()
    
    def test_iterator_next_throws_exception_when_no_more_elements(self):
        self.min_pq.insert(1)
        iterator = iter(self.min_pq)
        next(iterator)
        with self.assertRaises(StopIteration):
            next(iterator)

if __name__ == '__main__':
    unittest.main()