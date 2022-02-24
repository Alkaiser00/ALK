# Command to run script for scraping - scrapy runspider test.py -s USER_AGENT="Mobile"

import scrapy
import requests

URL = 'https://brickset.com/sets/year-2010'
Header_URL = 'http://httpbin.org/headers'


def Task5():
    # Task 5 i: Perform a "get" request on the given website
    r = requests.get(URL)
    # print(r.text)  # This will get the full page

    # Task 5 ii: Display an "OK" return status
    print("==========")
    print("Status code:")
    print("\t*", r.status_code)

    # If status code is 200 == OK, it will show success, if not will show an error has occurred
    if r.status_code == 200:
        print('\t Success!')
    else:
        print('\t An error has occurred.')

    # Task 5 iii: Display the Website header
    h = requests.head(URL)
    print("==========")
    print("Header:")
    for x in h.headers:
        print("\t", x, ".", h.headers[x])
    print("==========")

    # Task 5 iv: Modify the Header user-agent to display "Mobile"
    headers = {
        'User-Agent': "Mobile"
    }
    r2 = requests.get(Header_URL, headers=headers)
    print("Modified Header:")
    print("\t ", r2.request.headers)
    print("==========")


Task5()


# Task 6:
class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'
    start_urls = [URL]

    # Task 7: recursively extract JPG images on all known links. Display the list of image links.
    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'Image Link:': brickset.css(IMAGE_SELECTOR).extract_first(),
            }

        # To recurse next page
        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
