import scrapy
from urllib.parse import urljoin
import re

class AutoScootSpider(scrapy.Spider):
    name = "autoscoot"
    start_urls = [
        'https://www.autoscout24.com/lst?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=1&ocs_listing=include&powertype=kw&search_id=2d5dtu2rrk3&size=20&sort=age&source=listpage_pagination&ustate=N%2CU',
    ]

    n_pages_to_scrape = 2

    def parse(self, response):
        # Process each car on the current page
        for car in response.css('div.ListItem_wrapper__TxHWu'):
            relative_url = car.css('a::attr(href)').get()
            if relative_url:
                full_url = urljoin(response.url, relative_url)
                yield response.follow(full_url, callback=self.parse_car)

        # Follow pagination link
        current_page_number = int(response.url.split('page=')[1].split('&')[0])
        next_page_number = current_page_number + 1
        if next_page_number <= self.n_pages_to_scrape: 
            next_page_url = response.url.replace(f'page={current_page_number}', f'page={next_page_number}')
            yield response.follow(next_page_url, callback=self.parse)

    def parse_car(self, response):
        brand = response.xpath('//*/h1/div[1]/span[1]/text()').get().strip()
        model = response.xpath('//*/h1/div[1]/span[2]/text()').get().strip()
        price = response.xpath('//*/div[3]/div[1]/div/span/text()').get().strip()
        mileage = response.xpath('//*/div[1]/div[4]/text()').get().strip()
        fuel_type = response.xpath('//*/div[4]/div[4]/text()').get().strip()

        
        car_info = {
            'brand': brand,
            'model': model,
            'price': price,
            'mileage': mileage,
            'fuel_type': fuel_type
        }

        yield car_info
