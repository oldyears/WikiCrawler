# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikispiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    # sex = scrapy.Field()
    age = scrapy.Field()
    current_position = scrapy.Field()
    political_parties = scrapy.Field()
    career = scrapy.Field()
    spouse = scrapy.Field()
    children = scrapy.Field()
    relatives = scrapy.Field()
    residence = scrapy.Field()
    highest_degree = scrapy.Field()
    time_in_politics = scrapy.Field()
    number_of_politics = scrapy.Field()
    number_of_elections = scrapy.Field()
    aveSup_elections = scrapy.Field()
    sucRate_elections = scrapy.Field()
    pass
