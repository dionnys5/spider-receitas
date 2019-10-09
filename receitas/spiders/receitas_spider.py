import scrapy
import json
import re
from receitas.items import ReceitasItem


def define_valor(finder):
    resultado = finder[0] if len(finder) > 0 else 'Indefinido'
    return resultado

class ReceitasSpider(scrapy.Spider):
    name = "receitas"

    start_urls = [
        'https://mdemulher.abril.com.br/filtros_receitas/?is-home-template-list=true&pagina=0'
    ]


    custom_settings = {
        'ITEM_PIPELINES': {
            'receitas.pipelines.ReceitasPipeline': 400
        },
        'LOG_FILE': 'tutorial.log',
        'FEED_FORMAT': 'csv',
        #'JOBDIR': 'crawls\\tutorial',
        'FEED_URI': 'resultado_receitas.csv'
    }

    def parse(self, response):

        jsonresponse = json.loads(response.text)
        links = re.findall(r'href="(.*?)" class="legenda"', jsonresponse['html'])
        for link in links:
            yield scrapy.Request(link, callback=self.parse_receita)

        if jsonresponse['next']:
            url = response.request.url
            proxima = url[:-1] + str(int(url[-1]) + 1)
            yield scrapy.Request(proxima, self.parse)

        # item = ReceitasItem()
        # for quote in response.css("div.quote"):
        #     item['quote'] = quote.css("span.text::text").get()
        #     item['autor'] = quote.css("small.author::text").get()
        #     yield item
        #
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_receita(self, response):
        item = ReceitasItem()
        titulo = re.findall(r'<h1 class="article-title">(.*?)</h1>', response.text)
        dificuldade = re.findall(r'Dificuldade</strong> (.*)<<', response.text)
        tempo = re.findall(r'Preparo<\/strong> (.*)<', response.text)
        rendimento = re.findall(r'Rendimento<\/strong> (.*)<', response.text)
        ingredientes = re.findall(r'<li>+\s+<strong>(\d|\d/\d|\d .+?|a gosto)</strong>(.*)<a .+?>(.*?)</', response.text)
        preparo = re.findall(r'<p>(.*)<\/p>?', response.text)
        autor = re.findall(r'<p>\*<em>(.*)<\/em><\/p>', response.text)
        categoria = re.findall(r'Categoria <\/strong>+\s+<a (?:.*)>(.*)<\/a>', response.text)
        metodo_preparo = re.findall(r'preparo <\/strong>+\s+<a (?:.*)>(.*)<\/a>', response.text)
        origem = re.findall(r'geográficas <\/strong>+\s+<a (?:.*)>(.*)<\/a>', response.text)
        ocasioes = re.findall(r'Ocasiões <\/strong>+\s+<a (?:.*)>(.*)<\/a>', response.text)
        informacoes = re.findall(r'Informações <\/strong>+\s+<a (?:.*)>(.*)<\/a>', response.text)
        calorias = re.findall(r'calorias">+\s+(.*)\s+<\/span>', response.text)
        item['titulo'] = define_valor(titulo)
        item['dificuldade'] = define_valor(dificuldade)
        item['tempo'] = define_valor(tempo)
        item['rendimento'] = define_valor(rendimento)
        item['ingredientes'] = ingredientes if len(ingredientes) > 0 else 'Indefinido'
        item['preparo'] = preparo if len(preparo) > 0 else 'Indefinido'
        item['autor'] = define_valor(autor)
        item['categoria'] = define_valor(categoria)
        item['metodo_preparo'] = define_valor(metodo_preparo)
        item['origem'] = define_valor(origem)
        item['ocasioes'] = define_valor(ocasioes)
        item['informacoes'] = define_valor(informacoes)
        item['calorias'] = define_valor(calorias)
        yield item
