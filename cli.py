from operations import Operator
import sys
import logging


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    operations = Operator("samples/books.csv")
    print("*** Welcome to Book Data CLI ***")
    while True:
        print("-What would you like to do? Enter the number of the functionality.")
        print("1 - Get book info from csv by ISBN.")
        print("2 - Get book info from csv by Title.")
        print("3 - Process missing info for all data.")
        print("4 - Process missing info between lines.")
        print("5 - See current data on the terminal.")
        print("6 - Close the program.")
        try:
            inp = int(input())
            match inp:
                case 1:
                    isbn = input("Please enter the ISBN of the book.\n")
                    book = operations.get_book_info_by_isbn(isbn)
                    if book is None:
                        print("Isbn is not in the books.csv")
                        break
                    print(book)
                case 2:
                    title = input("Please enter the TITLE of the book.")
                    book = operations.get_book_info_by_title(title)
                    if book is None:
                        print("Title is not in the books.csv")
                        break
                    print(book)
                case 3:
                    operations.process_missing_info()
                    operations.update_csv()
                case 4:
                    try:
                        print(f"Enter start and end values betweeen 0 and {operations.book_count}")
                        start = int(input("Enter the start value.."))
                        end = int(input("Enter the end value.."))
                        operations.process_missing_info(start = start, end = end)
                    except:
                        print("Wrong input entered..")
                case 5:
                    operations.display_data()
                case 6:
                    sys.exit()
                case _:
                    print("You should enter an integer value between 1 and 6.")
        except:
            print("You should enter an integer value..")
            
            
if __name__ == '__main__':
    main()