import re

from locators.books_locator import BookLocator, AttributesReg


class BookParser:
    """
        Given an specific 'book' item in the page, this would make an object with the desired caracteristics.
    """

    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f"Book '{self.title}', rated {self.rating}"

    def __str__(self):
        string_star = 'stars' if self.rating > 1 else 'star'
        return f"'{self.title}' was rated {self.rating} {string_star} out of five (£{self.price})."

    @property
    def title(self) -> str:
        locator = BookLocator.TITLE
        return self.parent.select_one(locator).attrs['title']

    @property
    def rating(self) -> int:
        RATINGS = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        locator = BookLocator.RATING
        classes = self.parent.select_one(locator).attrs['class']
        star_rating = [e for e in classes if e != 'star-rating']
        return RATINGS[star_rating[0]]

    @property
    def price(self):
        locator = BookLocator.PRICE
        price_string = str(self.parent.select_one(locator).string)
        regex = AttributesReg.PRICE_NUMBER
        matches = re.search(regex, price_string)
        return float(matches.group(1))
