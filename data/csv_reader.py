import csv
from data.book import Book
import logging

class csv_io:
    
    @staticmethod
    def get_csv_file_rows(file_path : str) -> list:
        logging.info("Reading csv file.")
        with open(file_path, "r", encoding="utf-8") as file:
            rows = list(csv.reader(file, delimiter=";"))
        return rows[1:]
    
    @staticmethod
    def is_value_missing(row : list):
        for value in list:
            if value == '':
                return True
        return False
    
    @staticmethod
    def write_csv(file_path : str, books : list):
        logging.info("Writing to csv file")
        with open(file_path, "w", encoding="utf-8") as file:
            header = ['authors', 'title', 'price', 'isbn13', 'page-size']
            writer = csv.writer(file, delimiter=";", lineterminator="\n")
            writer.writerow(header)
            writer.writerows(books)
    
    @staticmethod
    def row_to_book(row : list) -> Book:
        author = row[0]
        title = row[1]
        price = row[2]
        isbn = row[3]
        page_size = ''
        try:
            page_size = row[4]
        finally:
            return Book(isbn, title, page_size, author, price)
        
