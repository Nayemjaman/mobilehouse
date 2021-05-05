import scrapy
import unicodedata
def cfDecodeEmail(encodedString):                       
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email

class PhoneSpiderSpider(scrapy.Spider):
    name = 'phone_spider'
    allowed_domains = ['gsmarena.com.bd']
    start_urls = [
        'https://www.gsmarena.com.bd/'
    ]
    

    def parse(self, response):
        brand_links = response.css('.col-md-6 a::attr(href)').extract()
        yield from response.follow_all(brand_links, self.parse_mobiles)
        # yield from response.follow_all(['https://www.gsmarena.com.bd/mobiistar/'], self.parse_mobiles) 

    def parse_mobiles(self, response): 
        yield from response.follow_all(response.css('.product-thumb a::attr(href)').extract(), self.parse_mobile_details)

    def parse_mobile_details(self, response): 
        mobile_details = {}

        for table in response.css('div.panel-box .table-striped'):
            temp_heading = ''
            temp_title = []
 
            for tr in table.css('tr'):
                heading =  unicodedata.normalize("NFKD",tr.css('th ::text').extract_first())
                title = unicodedata.normalize("NFKD",tr.css('td ::text').extract_first())
                

                if tr.css('.__cf_email__'):                    
                    x = tr.css('td ::attr(data-cfemail)').extract()
                    title = [cfDecodeEmail(y) for y in x]
                    
                if len(heading.strip()) < 1:
                    heading = temp_heading 
                    temp_title.append(title) 
                    mobile_details[heading] = temp_title               
                else:
                    temp_title = []
                    heading = unicodedata.normalize("NFKD",tr.css('th ::text').extract_first())
                    temp_heading = heading
                    temp_title.append(title)  
                    mobile_details[heading] = title
            

        yield mobile_details

