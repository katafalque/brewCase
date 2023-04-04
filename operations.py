from scraper.scraper import ScraperFactory
from data.csv_reader import csv_io
from data.book import Book
import tqdm
import logging
import asyncio
import random


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
        for row in self.data:
            book = csv_io.row_to_book(row)
            data_dict_isbn[book.isbn] = book
        return data_dict_isbn
        
    def __get_data_dict_title(self) -> Book:
        logging.info("Creating data dict keys = title..")
        data_dict_title = {}
        for row in self.data:
            book = csv_io.row_to_book(row)
            data_dict_title[book.title] = book
        return data_dict_title

    def __have_missing_values(self, book : Book) -> bool:
        return (book.author != '' and book.isbn != '' and book.price != '' and book.page_size != '' and book.title != '')
        
    def __book_to_row(self, book : Book) -> list:
        if book:
            return [book.author, book.title, book.price, book.isbn, book.price]
        return False
        
    def get_book_info_by_isbn(self, isbn : str) -> Book:
        book = self.data_dict_isbn.get(isbn)
        return book
    
    def get_book_info_by_title(self, title : str) -> Book:
        book = self.data_dict_title.get(title)
        return book
    
    async def process_missing_info(self, start : int = 0, end : int = 0):
        logging.info("Processing missing info..")  
        
        if start == 0 and end == 0:
            start, end = 0, self.book_count
        
        tasks = []

        for row in self.data[start : end - 1]:
            random_scraper_index = random.randint(0, 1)
            scraper = self.scrapers[random_scraper_index]
            book = csv_io.row_to_book(row)
            if book.isbn != '':
                task = asyncio.create_task(scraper.get_book(book.isbn))
                tasks.append(task)
            elif book.title != '':
                task = asyncio.create_task(scraper.get_book(book.title))
                tasks.append(task)
            else:
                tasks.append(asyncio.sleep(0))

        books = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
        
        for index, book in enumerate(books):
            row = self.__book_to_row(book)
            self.data[index + start] = row
            
        self.update_csv()
            
            
    def update_csv(self) -> None:
        csv_io.write_csv(self.file_path, self.data)
        
    def display_data(self) -> None:
        for row in self.data:
            print(row)


