from scraper.amazon_scraper import Amazon
from scraper.googlebooks_scraper import Google
import logging

class ScraperFactory:
    def __init__(self) -> None:
        self.scrapers = {}
        self.__scraper_factory()
        
        
    def __scraper_factory(self) -> None:
        logging.info("Creating factory for scrapers")
        amazon_scraper = Amazon()
        google_scraper = Google()
        self.scrapers = {
            "Amazon" : amazon_scraper,
            "Google" : google_scraper
        }
        
    def get_scrapers(self) -> dict:
        return self.scrapers