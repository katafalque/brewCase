from data.book import Book
import unittest

class TestBook(unittest.TestCase):
    
    def setUp(self):
        print("\nRunning setUp method...")
        self.book_1 = Book("11-11", "aaaa", "2222 pages", "bbbb", "33,33 TL")
        self.book_2 = Book("44-44", "dddd", "5555 pages", "eeee", "66,66 TL")
    
    def test_edit_isbn(self):
        print("Running test_edit_isbn...")
        self.assertEqual(self.book_1.isbn, "1111")
        self.assertEqual(self.book_2.isbn, "4444")
    
    def test_edit_price(self):
        print("Running test_discount...")
        self.assertEqual(self.book_1.price,"33,33")
        self.assertEqual(self.book_2.price,"66,66")
        
    def test_edit_page_size(self):
        print("Running test_discount...")
        self.assertEqual(self.book_1.page_size,"2222")
        self.assertEqual(self.book_2.page_size,"5555")
    


if __name__=='__main__':
	unittest.main()