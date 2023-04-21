import scrapy

# XPATH:
# links = '//div[@class="field-item even"]/h3/a/@href')'
# title = '//h1[contains(@class, "documentFirstHeading")]/text()'
# parrafos = '//div[@class="field-item even"]/p[text() and string-length(normalize-space(.)) > 5]'


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = ['https://www.cia.gov/readingroom/historical-collections']
    custom_settings = {
        'FEEDS': {
            'cia.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'indent': 4,
            }
        },
    }

    def parse(self, response):
        links = response.xpath(
            '//div[@class="field-item even"]/h3/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_links, cb_kwargs={'url': response.urljoin(link)})

    def parse_links(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath(
            '//h1/text()').get()
        paragraph = response.xpath(
            '//div[@class="field-item even"]/p[text() and string-length(normalize-space(.)) > 5]/text()').get()
        paragraph = paragraph.replace('<p>', '').replace('</p>', '')
        yield {
            'url': link,
            'title': title,
            'body': paragraph,
        }
