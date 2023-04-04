from scraper.babil_scraper import Babil
from scraper.dr_scraper import DR
from data.variables import environment_variables
import logging
import os

class ScraperFactory:
    def __init__(self) -> None:
        self.scrapers = []
        self.__scraper_factory()
        
        
    def __scraper_factory(self) -> None:
        logging.info("Creating factory for scrapers")
        babil_scraper = Babil(os.getenv("BABIL_URL"))
        dr_scraper = DR(os.getenv("DR_URL"))
        
        self.scrapers = [babil_scraper, dr_scraper]
        
    def get_scrapers(self) -> dict:
        return self.scrapers