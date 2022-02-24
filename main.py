# Use the Request library
import requests
import scrapy


class imagecrawler(scrapy.Spider):
    name = "image_crawler"
    start_urls = ["https://images.brickset.com/sets/large/10251-1.jpg?201510121127"]
    handle_httpstatus_list = [404, 410, 301, 500]

    def parse(self, response):
        css_selector = 'img'
        for x in response.css(css_selector):
            newsel = '@src'
            yield {
                'Image Link: ': x.xpath(newsel).extract_first(),
            }


# Set the target webpage
url = "https://images.brickset.com/sets/large/10251-1.jpg?201510121127"
r: object = requests.get(url)

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
