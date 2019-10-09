# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


def tokenizador(value):
    """

    :param value:
    :return: Uma lista com as palavras com base nas palavras da frase Value, separa com base nos espaços
    """
    return value.split(' ')


class ReceitasItem(scrapy.Item):
    titulo = scrapy.Field()
    dificuldade = scrapy.Field()
    tempo = scrapy.Field()
    rendimento = scrapy.Field()
    ingredientes = scrapy.Field()
    preparo = scrapy.Field()
    autor = scrapy.Field()
    categoria = scrapy.Field()
    metodo_preparo = scrapy.Field()
    origem = scrapy.Field()
    ocasioes = scrapy.Field()
    informacoes = scrapy.Field()
    calorias = scrapy.Field()