import aiohttp
import logging
import traceback
from data.book import Book
from bs4 import BeautifulSoup

class DR:
    def __init__(self, url : str) -> None:
        self.url = url

    def __get_params_dr(self, query : str) -> dict:
        return {
            "q" : query,
            "redirect" : "search"
        }

    async def __get_book_href_dr(self, query : str) -> str:
        try:
            logging.info(f"Trying execute : {self.__get_book_href_dr.func_name} for query : {query}")
            
            params = self.__get_params_dr(query)
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.dr.com.tr/search", params=params) as response:
                    response = await response.content.read()
            
            soup = BeautifulSoup(response,"html.parser")
            href = soup.find("a",{"class":"js-search-prd-item"}).get("href")
            
            logging.info(f"Execution of : {self.__get_book_href_dr.func_name} for query : {query} was successfull")
            
            return href
        except Exception:
            
            logging.info(f"Something went wrong during execution : {self.__get_book_href_dr.func_name} for query : {query}")
            logging.info(f"Exception traceback : {traceback.format_exc()}")
            
            return False
    
    async def __get_book_page_dr(self, query : str) -> str:
        try:
            logging.info(f"Trying execute : {self.__get_book_page_dr.func_name} for query : {query}")
            
            href = await self.__get_book_href_dr(query)
            if not href:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://www.dr.com.tr/{href}") as response:
                        response = await response.content.read()
                
                logging.info(f"Execution of : {self.__get_book_page_dr.func_name} for query : {query} was successfull")
                
                return response
            
        except Exception:
                
                logging.info(f"Something went wrong during execution : {self.__get_book_page_dr.func_name} for query : {query}")
                logging.info(f"Exception traceback : {traceback.format_exc()}")
                
                return False

    
    async def __book_page_parser_dr(self, query : str) -> dict:
        try:
            
            logging.info(f"Trying execute : {self.__book_page_parser_dr.func_name} for query : {query}")
            
            page = await self.__get_book_page_dr(query)
            if not page:
                parser = BeautifulSoup(page,"html.parser")
                datas = parser.find("div", {"class":"product-property"}).find("ul")
                
                book_data = {}
                key_list = ["title" , "author", "publisher", "grade", "page_size", "size", "year", "lang", "isbn"]
                
                for index, tag in enumerate(datas.find_all("li")):
                    attr = str(tag.text).strip().replace("\n", ":")
                    attr_list = attr.split(": ")
                    book_data[key_list[index]] = attr_list[1]
                    
                price = parser.find("div", {"class" : "salePrice"}).find("span").text
                
                book_data["price"] = price
                
                logging.info(f"Execution of : {self.__book_page_parser_dr.func_name} for query : {query} was successfull")
                
                return book_data
            
        except Exception:
                
            logging.info(f"Something went wrong during execution : {self.__book_page_parser_dr.func_name} for query : {query}")
            logging.info(f"Exception traceback : {traceback.format_exc()}")
            
            return False
    
    async def get_book(self, query : str) -> Book:
        try:
            logging.info(f"Trying execute : {self.get_book.func_name} D&R for query : {query}")
            
            book_data = await self.__book_page_parser_dr(query)
            if not book_data:
                
                logging.info(f"Execution of : {self.__book_page_parser_dr.func_name} D&R for query : {query} was successfull")
                
                return Book(book_data.get("isbn"), book_data.get("title"), book_data.get("page_size"), book_data.get("author"), book_data.get("price"))
            
        except Exception:
            logging.info(f"Something went wrong during execution : {self.get_book.func_name} D&R for query : {query}")
            logging.info(f"Exception traceback : {traceback.format_exc()}")
            
            return False
    

    
    