from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.variables import environment_variables
from data.book import Book
import logging
import traceback

class Amazon():
    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument("window_size=1920x1080")
        chrome_options.add_argument("disable-gpu")
        chrome_options.add_argument("log-level=3")
        self.driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
        
    def __open_amazon(self) -> None:
        logging.info("Opening Amazon")
        self.driver.get(environment_variables.get("AMAZON_URL"))
        
    def __set_book_search_amazon(self) -> None:
        logging.info("Setting book search for amazon")
        self.driver.find_element(By.XPATH, environment_variables.get("AMAZON_DEPARTMENT_DROPDOWN_XPATH")).click()
        
    def __search_box_input_amazon(self, input) -> None:
        logging.info("Setting search box input for amazon")
        self.driver.find_element(By.XPATH, environment_variables.get("AMAZON_SEARCHBOX_XPATH")).send_keys(input)
        
    def __click_search_button_amazon(self) -> None:
        logging.info("Clicking search button amazon")
        self.driver.find_element(By.XPATH, environment_variables.get("AMAZON_SEARCH_BUTTON_XPATH")).click()
        
    def __click_first_result_amazon(self) -> None:
        logging.info("Clicking first result for amazon")
        self.driver.find_element(By.XPATH, environment_variables.get("AMAZON_FIRST_RESULT_XPATH")).click()
        
    def __check_if_book_exists_amazon(self) -> bool:
        logging.info("Checking if  book exists in amazon")
        if self.driver.find_elements(By.XPATH, environment_variables.get("AMAZON_BOOK_EXIST_XPATH")):
            return True
        return False
    
    def __check_if_out_of_stock(self) -> bool:
        logging.info("Checking if book is in stock in amazon")
        if self.driver.find_elements(By.XPATH, environment_variables.get("AMAZON_BOOK_OOS_XPATH")):
            return True
        return False
        
    def __get_book_amazon(self, input : str) -> bool:
        self.__open_amazon()
        self.__set_book_search_amazon()
        self.__search_box_input_amazon(input)
        self.__click_search_button_amazon()
        if not self.__check_if_book_exists_amazon():
            self.__click_first_result_amazon()
            return True
        return False
        
    def get_book_amazon(self, input : str) -> Book:
        try:
            logging.info("Preparing book from amazon")
            if self.__get_book_amazon(input):
                price = ''
                page_size =  WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, environment_variables.get("AMAZON_BOOK_PAGESIZE_XPATH")))).text
                if not self.__check_if_out_of_stock():
                    price = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, environment_variables.get("AMAZON_BOOK_PRICE_XPATH")))).text
                title = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, environment_variables.get("AMAZON_BOOK_TITLE_XPATH")))).text
                if self.__check_if_out_of_stock():
                    isbn = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, environment_variables.get("AMAZON_BOOK_ISBN_OOS_XPATH")))).text
                else:
                    isbn = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, environment_variables.get("AMAZON_BOOK_ISBN_XPATH")))).text
                author = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, environment_variables.get("AMAZON_BOOK_AUTHOR_XPATH")))).text
                return Book(isbn, title, page_size, author, price)
            logging.info("Book not found in amazon")
            return False
        except:
            logging.info(f"Exception occured {traceback.format_exc()}")
            return False
