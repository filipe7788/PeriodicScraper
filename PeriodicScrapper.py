import scrapy
from inline_requests import inline_requests

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

    @inline_requests
    def parse_Periodico(self, response):
        coverImage = response.css('div.heading a.cover img::attr(src)').get('')

        titleText = response.css('h1::text').get('').strip()
    
        volumeAndNumber = titleText[0:10]
        year = response.css('div.published span.value::text').get('').strip()[0:4]
        volumeURL = response.meta['volumeURL']

        pdfs = []

        for section in response.css("ul.cmp_article_list h3 a::attr(href)").extract():
            item = section.strip()
            result = yield scrapy.Request(item)
            
            # Pagina do artigo 
            title = result.css("h1.page_title::text").get('').strip()
            keywords = result.css('.obj_article_details .item.keywords span::text').get('')
            strippedKeywords = ''.join(c for c in keywords if c not in '\r\t\n')
            # Página do periódico
            category = response.css('div.section h2::text').get('').strip()
            
            # Pagina do artigo 
            pdfLink = result.css('ul.value.galleys_links li a::attr(href)').get('')
            doiLink = result.css('.item.doi a::attr(href)').get('')

            # Pagina do artigo 
            rawAuthors = result.css('ul.authors span.name::text').extract()
            strippedAuthors = []
            for item in rawAuthors:
                strippedAuthors.append(''.join(c for c in item if c not in '\r\t\n'))

            pdfs.append(
                {
                    "title": title,
                    "keywords": strippedKeywords.split(','),
                    "category": category,
                    "pdfLink": pdfLink,
                    "doiLink": doiLink,
                    "authors": strippedAuthors
                }
            )
            
        yield {
            "year": year,
            "volumeAndNumber": volumeAndNumber,
            "coverImageUrl": coverImage,
            "volumeURL": volumeURL,
            "documents": pdfs
        }