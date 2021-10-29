import scrapy


class DiscussionSpider(scrapy.Spider):
    name = "discussion"
    pages = []

    def start_requests(self):
        urls = [
            "https://scratch.mit.edu/discuss/10/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parseSubpage(self, response):
        date = 'div.box-head a::text'
        author = 'a.black::text'
        post_content = 'div.post_body_html::text'

        for post in response.css('div.djangobb div.blockpost'):
            yield {
                'date': post.css(date).get(),
                'author': post.css(author).get(),
                'post_content': post.css(post_content).get()
            }

    def parse(self, response):
        for post in response.css('tbody tr'):
            yield {
                'title': post.css('div.tclcon h3.topic_isread a::text').get(),
                'author': post.css('span.byuser::text').get()[3:],
                'views': post.css('td.tc3::text').get(),
                'replies': post.css('td.tc2::text').get(),
                'link': post.css('div.tclcon h3.topic_isread a::attr(href)').get()
            }

        next_page = response.css('div.tclcon h3.topic_isread a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parseSubpage)
    


        
