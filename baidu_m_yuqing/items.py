# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduMYuqingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    update_item = scrapy.Field()

    ## m站通用字段
    index = scrapy.Field()
    ranking = scrapy.Field() # 排名
    page_index = scrapy.Field() # 页数
    introduce = scrapy.Field() # 简介
    media_name = scrapy.Field() # 媒体名称
    has_no = scrapy.Field() # 简介有无判定关键词
    content = scrapy.Field() # 正文
    dropdown = scrapy.Field()# 下拉词
    related = scrapy.Field() # 相关词

    source = scrapy.Field() # 抓取频道
    keyword = scrapy.Field() # 关键词
    title = scrapy.Field() # 搜索标题
    judge_keywords = scrapy.Field() # 判定关键词
    page_url = scrapy.Field() # 需要处理的链接
