import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/page/1/']

    # def start_requests(self):
    #     urls= ['http://quotes.toscrape.com/page/1/', 'http://quotes.toscrape.com/page/2/']
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text' : quote.css("span.text::text").get(),
                'author' : quote.css("small.author::text").get(),
                'tags' : quote.css("div.tags a.tag::text").getall()
            }

            next_page = response.css("li.next a::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)