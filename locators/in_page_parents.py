class PageLocator:
    PAGER = 'div.page_inner section ul.pager li.current'


class PageReg:
    TOTAL_PAGES = '[0-9]+ of ([0-9]+)'      # We will need the 'group one' of this one.
    URL_DIVIDER = "[a-z\.\/\-\:]+"           # Splitting the url.


class BookPageLocator:
    BOOK = 'section div ol.row li.col-xs-6.col-sm-4.col-md-3.col-lg-3'




