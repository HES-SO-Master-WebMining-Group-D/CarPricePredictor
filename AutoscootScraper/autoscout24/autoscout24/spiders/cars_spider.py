import scrapy
from urllib.parse import urljoin

class AutoScootSpider(scrapy.Spider):
    name = "autoscoot"
    start_urls = [
        f'https://www.autoscout24.com/lst/{brand}?atype=C&desc=1&page=1' for brand in [
            'audi', 'bmw', 'ford', 'opel', 'volkswagen', 'renault', 'alfa-romeo', 'aston-martin', 'bentley', 'bugatti',
            'cadillac', 'chevrolet', 'citroen', 'corvette', 'cupra', 'dacia', 'ferrari', 'honda', 'hyundai', 'jaguar',
            'jeep', 'kia', 'land-rover', 'lamborghini', 'lexus', 'maserati', 'mazda', 'mclaren', 'mini', 'mitsubishi',
            'nissan', 'peugeot', 'porsche', 'rolls-royce', 'skoda', 'seat', 'smart', 'subaru', 'suzuki', 'tesla', 'toyota'
        ]
    ]

    n_pages_to_scrape = 20

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
        def extract_with_default(xpath, default="unknown"):
            return response.xpath(xpath).get().strip() if response.xpath(xpath).get() else default

        car_info = {
            'url': response.url,
            'brand': extract_with_default('//*/h1/div[1]/span[1]/text()'),
            'model': extract_with_default('//*/h1/div[1]/span[2]/text()'),
            'price': extract_with_default('//*/div[3]/div[1]/div/span/text()'),
            'first_registration': extract_with_default('//*/div[3]/div[2]/div[3]/div[4]/text()'),
            'mileage': extract_with_default('//*/div[1]/div[4]/text()'),
            'fuel_type': extract_with_default('//*/div[4]/div[4]/text()'),
            'color': extract_with_default('//*[@id="color-section"]/div/div[2]/dl/dd[1]/text()'),
            'gearbox': extract_with_default('//*[@id="technical-details-section"]/div/div[2]/dl/dd[2]/text()'),
            'power': extract_with_default('//*[@id="technical-details-section"]/div/div[2]/dl/dd[1]/text()'),
            'engine_size': extract_with_default('//*[@id="technical-details-section"]/div/div[2]/dl/dd[3]/text()'),
            'seller': extract_with_default('//*[@id="__next"]/div/div/main/div[3]/div[3]/div[2]/div[6]/div[4]/text()'),
            'location': extract_with_default('//*[@id="__next"]/div/div/main/div[3]/div[2]/a/text()'),
            'body_type': extract_with_default('//*[@id="basic-details-section"]/div/div[2]/dl/dd[1]/text()'),
            'doors': extract_with_default('//*[@id="basic-details-section"]/div/div[2]/dl/dd[5]/text()'),
            'seats': extract_with_default('//*[@id="basic-details-section"]/div/div[2]/dl/dd[4]/text()'),
            'drivetrain': extract_with_default('//*[@id="basic-details-section"]/div/div[2]/dl/dd[3]/text()'),
            'co2_emission': extract_with_default('//*[@id="environment-details-section"]/div/div[2]/dl/dd[2]/text()'),
            'emission_class': extract_with_default('//*[@id="environment-details-section"]/div/div[2]/dl/dd[3]/text()'),
            'condition': extract_with_default('//*[@id="basic-details-section"]/div/div[2]/dl/dd[2]/text()'),
            'upholstery': extract_with_default('//*[@id="color-section"]/div/div[2]/dl/dd[4]/text()'),
            'upholstery_color': extract_with_default('//*[@id="color-section"]/div/div[2]/dl/dd[3]/text()'),
        }

        yield car_info
