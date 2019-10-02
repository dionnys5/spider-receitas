import scrapy
from receitas.items import ReceitasItem


class ReceitasSpider(scrapy.Spider):
    """
    A :class QuostesSpider: é composta pelos parâmetros e lógica da seleção e coleta de dados de uma página HTML.
    """
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    # Lembrar de sempre colocar nomes significativos para os arquivos de saída.
    # Para testes sempre apagar a pasta criada definida em JOBDIR
    custom_settings = {
        'ITEM_PIPELINES': {
            'receitas.pipelines.ReceitasPipeline': 400
        },
        'LOG_FILE': 'tutorial.log',
        'FEED_FORMAT': 'csv',
        'JOBDIR': 'crawls\\tutorial',
        'FEED_URI': 'tutorial_resultados_2.csv'
    }

    def parse(self, response):
        '''
        :param response: Que é o valor do conteúdo da página visitada a partir das start_urls
        :return: Objeto da classe TutorialItem que define a estrutura de dados coletados
        '''
        item = ReceitasItem()
        for quote in response.css("div.quote"):
            item['quote'] = quote.css("span.text::text").get()
            item['autor'] = quote.css("small.author::text").get()
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
