from scraper.scraper import ScraperFactory
from data.csv_reader import csv_io
from data.book import Book
from tqdm import tqdm
import logging


class Operator:
    def __init__(self, file_path : str) -> None:
        self.file_path = file_path
        self.scrapers = ScraperFactory().get_scrapers()
        self.data = self.__load_data(file_path)
        self.data_dict_isbn = self.__get_data_dict_isbn()
        self.data_dict_title = self.__get_data_dict_title()
        self.book_count = len(self.data) - 1
        
    def __load_data(self, file_path: str) -> list:
        logging.info("Loading data from csv..")
        rows = csv_io.get_csv_file_rows(file_path)
        return rows
    
    def __get_data_dict_isbn(self) -> dict:
        logging.info("Creating data dict keys = isbn..")
        data_dict_isbn = {}
        for row in self.data[1:]:
            book = csv_io.row_to_book(row)
            data_dict_isbn[book.isbn] = book
        return data_dict_isbn
        
    def __get_data_dict_title(self) -> Book:
        logging.info("Creating data dict keys = title..")
        data_dict_title = {}
        for row in self.data[1:]:
            book = csv_io.row_to_book(row)
            data_dict_title[book.title] = book
        return data_dict_title
        
    def __get_start_values_per_scraper(self, start : int = 0, end : int= 0) -> list:
        logging.info("Preparing search intervals with respect to inputs..")
        scraper_count = len(self.scrapers)
        if start == 0 and end == 0:
            start_values = [i * (int(self.book_count / scraper_count)) for i in range(scraper_count)]
            return start_values
        start_values = [i * (int((end - start) / scraper_count)) + start for i in range(scraper_count)]
        return start_values
        
    def __book_to_row(self, book : Book) -> list:
        if book:
            return [book.author, book.title, book.price, book.isbn, book.price]
        return False
    
    def __update_row(self, index : int, row : list):
        self.data[index] = row
        
    def get_book_info_by_isbn(self, isbn : str) -> Book:
        book = self.data_dict_isbn.get(isbn)
        return book
    
    def get_book_info_by_title(self, title : str) -> Book:
        book = self.data_dict_title.get(title)
        return book
    
    def process_missing_info(self, start : int = 0, end : int = 0) -> list:
        logging.info("Processing missing info..")
        start_values = self.__get_start_values_per_scraper(start, end)                
        amazon = self.scrapers.get("Amazon")
        google = self.scrapers.get("Google")
        interval = int(self.book_count if start == 0 and end == 0 else (end - start) / 2)
        amazon_list = self.data[start_values[0]:start_values[1]]
        google_list = self.data[start_values[1]:start_values[1] + interval]

        amazon_results = []
        google_results = []
        progress_bar = tqdm(total = len(amazon_list) + len(amazon_list))
        for index, row in enumerate(amazon_list):
            book = csv_io.row_to_book(row)
            if book and (book.author == '' or book.isbn == '' or book.title == '' or book.price != ''):
                if book.author == '' or book.isbn == '' or book.title == '' or book.price != '':
                    resp = amazon.get_book_amazon(book.isbn)
                    amazon_results.append(self.__book_to_row(resp))
                    self.__update_row(index + start_values[0], row)
            progress_bar.update(1)
                
                
        for index, row in enumerate(google_list):
            print("in here")
            book = csv_io.row_to_book(row)
            if book and book.isbn != '' and (book.author == '' or book.isbn == '' or book.title == '' or book.price != ''):
                resp = google.get_book_google(True, book.isbn)
                if not resp:
                    print(f"ISBN : {book.isbn} produced no results..")
                else:
                    google_results.append(self.__book_to_row(resp))
                    self.__update_row(index + start_values[1], row)
            elif book and book.title != '':
                resp = google.get_book_google(False, book.title)
                if not resp:
                    print(f"Title : {book.title} produced no results..")
                else:
                    google_results.append(self.__book_to_row(resp))
                    self.__update_row(index + start_values[1], row)  
            
            progress_bar.update(1)
    
    def update_csv(self) -> None:
        csv_io.write_csv(self.file_path, self.data)
        
    def display_data(self) -> None:
        for row in self.data:
            print(row)


