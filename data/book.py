class Book:
    def __init__(self, isbn : str, title : str, page_size : str, author : str, price : str) -> None:
        self.isbn = self.__edit_isbn(isbn)
        self.title = title
        self.page_size = self.__edit_page_size(page_size)
        self.author = author
        self.price = self.__edit_price(price)
    
    def __edit_isbn(self, isbn : str) -> str:
        if '-' in isbn:
            return isbn.replace('-', '')
        return isbn
    
    def __edit_price(self, price : str) -> str:
        tokens = price.split()
        if len(tokens) > 1:
            return tokens[0]
        return price
    
    def __edit_page_size(self, page_size : str) -> str:
        tokens = page_size.split()
        if len(tokens) > 1:
            return tokens[0]
        return page_size
    
    def __str__(self):
        return f"Title => {self.title}, Page Size => {self.page_size}, Author => {self.author}, Price => {self.price}, ISBN => {self.isbn}"