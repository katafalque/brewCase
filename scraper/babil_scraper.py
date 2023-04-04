import aiohttp
import logging
import traceback
import asyncio
from data.book import Book
from bs4 import BeautifulSoup

class Babil:
    def __init__(self, url : str) -> None:
        self.url = url

    def __get_params_babil(self, query : str) -> dict:
        return {
            "q" : query
        }

    async def __get_book_href_babil(self, query : str) -> str:
        try:
            logging.info(f"Trying execute : {self.__get_book_href_babil.__name__} for query : {query}")
            
            params = self.__get_params_babil(query)
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.babil.com/search", params=params) as response:
                    response = await response.content.read()
            
            soup = BeautifulSoup(response,"html.parser")
            href=soup.find("div", {"class" : "products-content"}).find("a").get("href")
            
            logging.info(f"Execution of : {self.__get_book_href_babil.__name__} for query : {query} was successfull")
            logging.info(f"HREF = {href}")
            return href
        except Exception:
            
            logging.info(f"Something went wrong during execution : {self.__get_book_href_babil.__name__} for query : {query}")
            logging.info(f"Exception traceback : {traceback.format_exc()}")
            
            return False
    
    async def __get_book_page_babil(self, query : str) -> str:
        try:
            logging.info(f"Trying execute : {self.__get_book_page_babil.__name__} for query : {query}")
            
            href = await self.__get_book_href_babil(query)
            if href:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://www.babil.com{href}") as response:
                        response = await response.content.read()
                
                logging.info(f"Execution of : {self.__get_book_page_babil.__name__} for query : {query} was successfull")
                
                return response
            
        except Exception:
                
                logging.info(f"Something went wrong during execution : {self.__get_book_page_babil.__name__} for query : {query}")
                logging.info(f"Exception traceback : {traceback.format_exc()}")
                
                return False

    
    async def __book_page_parser_babil(self, query : str) -> dict:
        try:
            
            logging.info(f"Trying execute : {self.__book_page_parser_babil.__name__} for query : {query}")
            
            page = await self.__get_book_page_babil(query)
            if page:
                parser = BeautifulSoup(page,"html.parser")
                datas = parser.find("div", {"class", "col-lg-6"}).find_all("div", {"class" : "col-lg-8"})
                page_size = str(datas[0].text).strip()
                isbn = str(datas[-1].text).strip()
                price = str(parser.find("div", {"class", "col-lg-7"}).find("span", {"class", "new-price"}).text).strip()
                title = str(parser.find("div", {"class", "col-lg-12"}).find("h1").text).strip()
                author = str(parser.find("div", {"class", "col-lg-12"}).find("h2").text).strip()
                
                book_data = {"page_size" : page_size, "isbn" : isbn, "price" : price, "title" : title, "author" : author}
                
                logging.info(f"Execution of : {self.__book_page_parser_babil.__name__} for query : {query} was successfull")
                
                return book_data
            
        except Exception:
                
            logging.info(f"Something went wrong during execution : {self.__book_page_parser_babil.__name__} for query : {query}")
            logging.info(f"Exception traceback : {traceback.format_exc()}")
            
            return False
    
    async def get_book(self, query : str) -> Book:
        try:
            logging.info(f"Trying execute : {self.get_book.__name__} BABIL for query : {query}")
            
            book_data = await self.__book_page_parser_babil(query)
            if book_data:
                
                logging.info(f"Execution of : {self.get_book.__name__} BABIL for query : {query} was successfull")
                
                b = Book(book_data.get("isbn"), book_data.get("title"), book_data.get("page_size"), book_data.get("author"), book_data.get("price"))
                print(b)
                return b
            
        except Exception:
            logging.info(f"Something went wrong during execution : {self.get_book.__name__} BABIL for query : {query}")
            logging.info(f"Exception traceback : {traceback.format_exc()}")
            
            return False
