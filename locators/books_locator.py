class BookLocator:
    TITLE = 'article.product_pod h3 a'  # We want the 'title' attribute from this tag
    LINK = 'article product_pod div.image_container h3 a'   # We want the 'href' attribute from this tag
    PRICE = 'div.product_price p.price_color'   # We wan to se a regex to extract the price here
    RATING = 'p.star-rating'    # We want the 'following class name' to this one.


class AttributesReg:
    PRICE_NUMBER = "\\\\xc2\\\\xa3([0-9\.]*)"   # This one should give us the price.

