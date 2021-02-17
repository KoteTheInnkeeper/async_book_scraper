import re
import requests
import logging

from bs4 import BeautifulSoup
from locators.in_page_parents import PageReg, PageLocator, BookPageLocator
from parser.book_parser import BookParser

logger = logging.getLogger('scraping.all_books_page')

class BooksInPage:
    def __init__(self, url: str):
        page_content = str(requests.get(url).content)
        logger.info("Parsing page content with BeautifulSoup4.")
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def books(self) -> list:
        logger.info(f"Finding all books in the page using '{BookPageLocator.BOOK}'.")
        locator = BookPageLocator.BOOK
        books_tags = self.soup.select(locator)
        return [BookParser(e) for e in books_tags]


class PageGenerator:
    def __init__(self, url: str):
        self.soup_for_page = BeautifulSoup(str(requests.get(url).content), 'html.parser')
        self.number = 1
        self.url = url

    @property
    def last(self) -> int:
        locator = PageLocator.PAGER
        page_tag = self.soup_for_page.select_one(locator).string
        regex = PageReg.TOTAL_PAGES
        matches = re.search(regex, page_tag)
        last_page = int(matches.group(1))
        return last_page

    def __next__(self) -> str:
        if self.number <= self.last:
            current = self.number
            self.number += 1
            return self.divided_page[0] + str(current) + self.divided_page[1]
        else:
            raise StopIteration()

    @property
    def divided_page(self) -> list:
        regex = PageReg.URL_DIVIDER
        matches = re.findall(regex, self.url)
        return matches

    def __iter__(self):
        return self


class Bookshelf:
    def __init__(self, parsed_books: list):
        """
        Initializes this class as one for holding 'BookParser' objects in its property 'books', which is a list.
        """
        self.content = parsed_books

    def __repr__(self):
        return f"<Bookshelf object with a list of books in it>"

    def __str__(self):
        """
            A string dunder to print all bookshelf's content when asked for printing a Bookshelf object.
        :return:
        """
        string_to_print = ''
        for i, book in enumerate(self.content, start=1):
            string_to_print += f'{i}) "{book.title}" (£{book.price}) was rated {book.rating}/5.\n'
        return string_to_print



