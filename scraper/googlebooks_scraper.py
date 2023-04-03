import requests
from data.book import Book
from data.variables import environment_variables
import logging

class Google():
    
    def __init__(self) -> None:
        pass
    
    def __get_payload_google(self, isIsbn : bool, query : str) -> dict:
        return {
            "q" : f"isbn:{query}" if isIsbn else query
        }
        
    def __search_books_google(self, isIsbn : bool, query : str) -> list:
        logging.info("Request google to get book..")
        payload = self.__get_payload_google(isIsbn, query)
        response = requests.get(environment_variables.get("GOOGLE_API_URL"), payload).json()
        if response.get("totalItems") == 0:
            return False
        return response.get("items")
    
    def __get_book_data_google(self, item : dict) -> Book:
        volume_info = item.get("volumeInfo")
        isbn = volume_info.get("industryIdentifiers")[0].get("identifier")
        title = volume_info.get("title")
        page_size = str(volume_info.get("pageCount"))
        author = ",".join(volume_info.get("authors")) if volume_info.get("authors") else ''
        price = ""
        return Book(isbn, title, page_size, author, price)
    
    def __get_exact_book_isbn_google(self, items : list, query : str) -> dict:
        for item in items:
            volume_info = item.get("volumeInfo")
            for identifier_type in volume_info.get("industryIdentifiers"):
                if identifier_type.get("type") == "ISBN_13" and identifier_type.get("identifier") == query:
                    return item
        return False
    
    def __get_perfect_match_book(self, items : list, query : str) -> list:
        for item in items:
            volume_info = item.get("volumeInfo")
            if volume_info.get("industryIdentifiers") and volume_info.get("title") == query:
                return item
        return False
        
    def get_book_google(self, isIsbn : bool, query) -> Book:
        logging.info("Preparing book from google.")
        items = self.__search_books_google(isIsbn, query)
        if not items:
            return False
        if isIsbn == False and len(items) > 1:
            item = self.__get_perfect_match_book(items, query)
            if not item:
                return False
            book = self.__get_book_data_google(item)
            return book
        elif isIsbn:
            item = self.__get_exact_book_isbn_google(items, query)
            if not item:
                return False
            book = self.__get_book_data_google(item)
            return book
        return False
    
            

