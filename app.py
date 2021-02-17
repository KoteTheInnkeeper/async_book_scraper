import logging
import asyncio
import aiohttp
from time import time

from async_timeout import timeout

from pages.all_books_page import BooksInPage, PageGenerator, Bookshelf

# Set the logger
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S",
                    level=logging.INFO,
                    filename='log.txt')


loop = asyncio.get_event_loop()

logger = logging.getLogger('scraping')
# Finished setting the logger.

logger.info('Loading books list...')


# This is the first page of the website when asked to show by pages
initial_page = 'http://books.toscrape.com/catalogue/page-1.html'

# This is an iterable generator with each page, accounting from the '1' to the 'last one'. The 'last page' number
# is also scraped from the page.
page_range = PageGenerator(initial_page)


async def fetch_page(session, url):
    async with timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks


print("Books are being scraped. Wait a minute!")
start = time()
pages = loop.run_until_complete(get_multiple_pages(loop, *page_range))  # Holds an 'await' of the grouped_tasks -> a list of results.

# scraped_books
scraped_books = []
for page_content in pages:
    books_in_this_page = BooksInPage(page_content)
    for book in books_in_this_page.books:
        scraped_books.append(book)

# Lets generate a Bookshelf object for holding the books in the entire website
web_bookshelf = Bookshelf(scraped_books)
print(f"Books scraped! It took %.2f seconds to do so." %(time() - start))
