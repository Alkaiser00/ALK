import re

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class PexelsScraper(scrapy.Spider):
    name = "pexels"

    # Define the regex we'll need to filter the returned links
    url_matcher = re.compile('^https:\/\/www\.pexels\.com\/photo\/')

    # Create a set that'll keep track of ids we've crawled
    crawled_ids = set()

    src_extractor = re.compile('src="([^"]*)"')
    tags_extractor = re.compile('alt="([^"]*)"')

    def start_requests(self):
        url = "https://www.pexels.com/"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        body = Selector(text=response.body)
        link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]

        # Crawl the filtered links
        for link in next_links:
            yield scrapy.Request(link, self.parse)

        images = body.css('img.image-section__image').extract()

        # body.css().extract() returns a list which might be empty
        for image in images:
            img_url = PexelsScraper.src_extractor.findall(image)[0]
            tags = [tag.replace(',', '').lower() for tag in PexelsScraper.tags_extractor.findall(image)[0].split(' ')]
            print(img_url, tags)

    def is_extracted(self, url):
        # Image urls are of type: https://www.pexels.com/photo/asphalt-blur-clouds-dawn-392010/
        id = int(url.split('/')[-2].split('-')[-1])
        if id not in PexelsScraper.crawled_ids:
            PexelsScraper.crawled_ids.add(id)
            return False
        return True

# Set the target webpage
url = "https://www.pexels.com/"
r = requests.get(url)

# This will get the full page
# print(r.text)
# This will get the status code
print("Status code:")
print("\t *", r.status_code)

# This will just get just the headers
h = requests.head(url)
print("Header:")
print("**********")
# To print line by line
for x in h.headers:
    print("\t ", x, ":", h.headers[x])
print("**********")

# This will modify the headers user-agent
headers = {
    'User-Agent': "Mobile"
}
# Test it on an external site
url2 = 'http://httpbin.org/headers'
rh = requests.get(url2, headers=headers)
print(rh.text)