import logging

from pages.all_books_page import BooksInPage, PageGenerator, Bookshelf

# Set the logger
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S",
                    level=logging.INFO,
                    filename='logs.txt')

logger = logging.getLogger('scraping')
# Finished setting the logger.

logger.info('Loading books list...')


# This is the first page of the website when asked to show by pages
initial_page = 'http://books.toscrape.com/catalogue/page-1.html'

# This is an iterable generator with each page, accounting from the '1' to the 'last one'. The 'last page' number
# is also scraped from the page.
page_range = PageGenerator(initial_page)

print("Books are being scraped. Wait a minute!")
# scraped_books
scraped_books = []
for page in page_range:
    books_in_this_page = BooksInPage(page)
    for book in books_in_this_page.books:
        scraped_books.append(book)

# Lets generate a Bookshelf object for holding the books in the entire website
web_bookshelf = Bookshelf(scraped_books)
print("Books scraped!")


