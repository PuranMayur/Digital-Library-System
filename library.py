from typing import List
import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
            
        book = [(book_titles[i], texts[i]) for i in range(len(book_titles))]
        copy_book = book[:]
        copy_book = self.merge_sort(copy_book, lambda x, y: x[0] < y[0])
        
        for i in range(len(copy_book)):
            copy_book[i] = copy_book[i][0], self.merge_sort(copy_book[i][1], lambda x, y: x < y)
            
        self.book_titles = [copy_book[i][0] for i in range(len(copy_book))]
        texts = [copy_book[i][1] for i in range(len(copy_book))]
            
        self.distinct_words_list: List[List[str]] = []
        for i in range(len(self.book_titles)):
            temp_list = []
            if texts[i] == []:
                self.distinct_words_list.append([])
                continue
            temp = texts[i][0]
            temp_list.append(temp)
            for j in range(len(texts[i])):
                if texts[i][j] != temp:
                    temp = texts[i][j]
                    temp_list.append(temp)
            self.distinct_words_list.append(temp_list)
        pass
    
    def distinct_words(self, book_title):
        return self.distinct_words_list[self.binary_search(self.book_titles, book_title)]
        pass
    
    def count_distinct_words(self, book_title):
        return len(self.distinct_words_list[self.binary_search(self.book_titles, book_title)])
        pass
    
    def search_keyword(self, keyword):
        reqd_books = []
        for i in range(len(self.book_titles)):
            if self.binary_search(self.distinct_words_list[i], keyword) != -1:
                reqd_books.append(self.book_titles[i])
        return reqd_books
        pass
    
    def print_books(self):
        for i in range(len(self.book_titles)):
            print(f"{self.book_titles[i]}: {' | '.join(self.distinct_words_list[i])}")
        pass
    
    def merge_sort(self, arr, comparator = lambda x, y: x < y):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], comparator)
        right = self.merge_sort(arr[mid:], comparator)
        return self.merge(left, right, comparator)
    
    def merge(self, left, right, comparator):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if comparator(left[i], right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result += left[i:]
        result += right[j:]
        return result
    
    def binary_search(self, arr, target, comparator = lambda x, y: x < y):
        
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            if comparator(arr[mid], target):
                left = mid + 1
            else:
                right = mid - 1
        return -1

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name = name
        self.params = params
        self.books = []
        if name == "Jobs":
            self.hash_table = ht.HashMap(collision_type = "Chain", params = params)
        elif name == "Gates":
            self.hash_table = ht.HashMap(collision_type = "Linear", params = params)
        else:
            self.hash_table = ht.HashMap(collision_type = "Double", params = params)
        pass
    
    def add_book(self, book_title, text):
        
        self.books.append(book_title)
        hash_set = ht.HashSet(collision_type = self.hash_table.collision_type, params = self.params)
        
        for word in text:
            hash_set.insert(word)
        temp = (book_title, hash_set)
        self.hash_table.insert(temp)

    def distinct_words(self, book_title) -> List[str]:
        hash_set = self.hash_table.find(book_title)
        if hash_set is None:
            return []
        if self.name == "Jobs":
            return [x for element in hash_set.table if element is not None for x in element]
        else:
            return [element for element in hash_set.table if element is not None]
        pass
    
    def count_distinct_words(self, book_title):
        hash_set = self.hash_table.find(book_title)
        return hash_set.size
        pass
    
    def search_keyword(self, keyword):
        
        keyword_books_list = []
        for book in self.books:
            curr_hashset = self.hash_table.find(book)
            if curr_hashset is None:
                continue
            if curr_hashset.find(keyword):
                keyword_books_list.append(book)
        return keyword_books_list
        pass
    
    def print_books(self):
        
        for i in range(len(self.books)):
            curr_hashset = self.hash_table.find(self.books[i])
            print(f"{self.books[i]}: {str(curr_hashset)}")
        pass