import scrapy
from bookscraper.items import bookItem
import random

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'data.csv' : {'format' : 'csv', 'overwrite' : True}
        }

    }




    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relativeURL = book.css('h3 a').attrib['href']

            if 'catalogue/' in relativeURL:
                bookURL = 'https://books.toscrape.com/' + relativeURL
            else: 
                bookURL = 'https://books.toscrape.com/catalogue/' + relativeURL
            yield scrapy.Request(bookURL,callback=self.parse_bookpage) # headers={"User-Agent":self.user_agent_list[random.randint(0,len(self.user_agent_list)-1)]})
            # yield{
            #     'name' : book.css('h3 a::text').get(),
            #     'price' : book.css('.product_price .price_color::text').get(),
            #     'url' : book.css('h3 a').attrib['href'],
            # }
        
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else: 
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)# headers={"User-Agent":self.user_agent_list[random.randint(0,len(self.user_agent_list)-1)]})

        
    def parse_bookpage(self,response):
     table_rows = response.css("table tr")
     book_item = bookItem()
     book_item['url'] = response.url,
     book_item['title'] = response.css('.product_main h1::text').get(),
     book_item['upc'] = table_rows[0].css("td ::text").get(),
     book_item['product_type'] = table_rows[1].css("td ::text").get(),
     book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
     book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
     book_item['tax'] = table_rows[4].css("td ::text").get(),
     book_item['availability'] = table_rows[5].css("td ::text").get(),
     book_item['num_reviews'] = table_rows[6].css("td ::text").get(),
     book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
     book_item['stars'] = response.css("p.star-rating").attrib['class'],
     book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
     book_item['price'] = response.css('p.price_color::text').get(),

     yield book_item