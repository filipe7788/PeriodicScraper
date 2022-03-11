import scrapy

class PeriodicScrapper(scrapy.Spider):
    name = 'PeriodicScrapper'
    start_urls = [
        'https://periodicos.ufba.br/index.php/revistaici/issue/archive', 
        'https://periodicos.ufba.br/index.php/revistaici/issue/archive/2'
    ]
        
    def parse(self, response):
        for periodicos in response.css('.obj_issue_summary'):

            volumeURL = periodicos.css('a.title').css("::attr(href)").get()
                       
            yield scrapy.Request(
                volumeURL,
                callback=self.parse_Periodico,
                meta={"volumeURL": volumeURL}
            )

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)

    def parse_Periodico(self, response):
        coverImage = response.css('div.heading a.cover img::attr(src)').get()

        titleText = response.css('h1::text').get().strip()
    
        volumeAndNumber = titleText[0:11]
        year = titleText[12:16]
        volumeURL = response.meta['volumeURL']

        fatherData = {
            "volumeAndNumber": volumeAndNumber,
            "coverImageUrl": coverImage,
            "year": year,
            "volumeURL": volumeURL
        }
        

        for section in response.css("ul.cmp_article_list h3 a::attr(href)").extract():
            item = section.strip()
            yield scrapy.Request(
                item,
                callback=self.parse_Documentos,
                meta={"item": fatherData}
            )

        
    def parse_Documentos(self, response):
        pdfs = response.css("h1.page_title::text").get().strip()
        data = response.meta["item"]
        yield {'pdfs': pdfs, "data": data}