# -*- coding: utf-8 -*-
import scrapy
import re
import traceback
import pymongo
import cx_Oracle
from scrapy import log
from baidu_m_yuqing.items import BaiduMYuqingItem
from scrapy.conf import settings
import urllib
import pdb
import copy

import os
os.system('export LANG=zh_CN.GB18030')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class BaiduMQuanBuSpider(scrapy.Spider):
    name = "baidu_m_wenda"

    def __init__(self, *args, **kwargs):
        super(BaiduMQuanBuSpider, self).__init__(*args, **kwargs)
        try:
            connstr = "%s/%s@%s/%s" % (
                    settings['ORACLE_SERVER_USERNAME'],
                    settings['ORACLE_SERVER_PASSWORD'],
                    settings['ORACLE_SERVER_ADDR'],
                    settings['ORACLE_SERVER_DBNAME'])
            self.oracleFetchConn = cx_Oracle.connect(connstr)
        except Exception, err:
            self.logger.error("Manager fetch Connection Oracle Error!: %s" % (err,))

        cr = self.oracleFetchConn.cursor()
        exesql = settings['GET_HUICONG_YUQING_KEYWORD_SQL'].format('baidu_m_wenda'.upper(), settings['SELECT_STEP'])
        ret = cr.execute(exesql)
        self.start_urls = ret.fetchall()
        cr.close()

    def start_requests(self):
        #pdb.set_trace()
        for index, keyword, page_max in  self.start_urls:
            pn_max = 10 * (page_max*2)
            page_index = 0
            keyword = keyword.decode('GBK')
            for pn in range(0, pn_max, 10):
                page_index = page_index + 1
                item = BaiduMYuqingItem()
                item['index'] = index
                item['keyword'] = keyword
                item['source'] = 'baidu_m_wenda'
                item['page_index'] = page_index
                item['has_no'] = 'no'
                item['media_name'] = ' '
                item['dropdown'] = ' '
                item['related'] = ' '
                cur_url = 'http://m.baidu.com/sf/vsearch?pd=wenda_tab&'
                ky = keyword.encode('gb18030')
                url = cur_url + 'pn=%d&word=%s' % (pn, ky)
                meta = {'pn': pn, 'item': item, 'dont_retry': True}
                self.log('insert new keyword=%s pn=%d index=%d page_index=%d' %
                         (keyword, pn, index, page_index), level=log.INFO)
                yield scrapy.Request(url=url, callback=self.parse, meta=meta, dont_filter=True)
        # keywords = [u'慧聪网怎么样']
        # page_max = 5
        # for keyword in keywords:
            # pn_max = 10 * 1
            # index = 0
            # page_index = 0
            # for pn in range(0, pn_max, 10):
                # page_index = page_index + 1
                # item = BaiduMYuqingItem()
                # item['index'] = index
                # item['keyword'] = keyword
                # item['source'] = 'baidu_m_wenda'
                # item['page_index'] = page_index
                # item['has_no'] = 'no'
                # cur_url = 'http://m.baidu.com/sf/vsearch?pd=wenda_tab&'
                # ky = keyword
                # url = cur_url + 'pn=%d&word=%s' % (pn, ky)
                # meta = {'pn': pn, 'item': item, 'dont_retry': True}
                # self.log('insert new keyword=%s pn=%d index=%d page_index=%d' %
                         # (keyword, pn, index, page_index), level=log.INFO)
                # yield scrapy.Request(url=url, callback=self.parse, meta=meta, dont_filter=True)


    def parse(self, response):
        #pdb.set_trace()
        item = response.meta['item']
        pn = response.meta['pn']

        if response.status != 200:
            self.log('fetch failed! keyword=%s index=%d status=%d jump_url=%s' %
                     (item['keyword'], item['index'], item['status'], response.headers.get('Location', '')), level=log.WARNING)
            if response.status == 302 and response.headers.get('Location', '').find('vcode') > 0:
                ##block
                return
            else:
                yield item

        ## 搜索结果简介
        introduces = response.xpath("//div[@class='c-line-clamp4 c-color-gray-a sfc-wenda-tab-text']//text()").extract()
        introduces = ''.join(introduces)
        intros = introduces.split('...')

        handles = response.xpath("//div[@class='c-container']")
        cur_rank = 0
        for (introduce, handle) in zip(intros, handles):
            cur_rank += 1
            page_baidu_url = handle.xpath("a/@href").extract()
            ## 去重保持顺序不变
            page_baidu_url = sorted(set(page_baidu_url), key = page_baidu_url.index)
            page_baidu_url = page_baidu_url[0] if page_baidu_url else ''
            item['ranking'] = cur_rank
            item['introduce'] = introduce.strip()
            # print 'rangking', cur_rank
            # print item['introduce']
            if not page_baidu_url:
                continue
            item = copy.deepcopy(response.meta['item'])
            yield scrapy.Request(url=page_baidu_url, callback=self.parse_page, meta={'item' : item}, dont_filter=True)

    def parse_page(self, response):
        #pdb.set_trace()
        item = response.meta['item']
        if response.status == 200:
            title = response.xpath("//title/text()").extract()
            title = title[0] if title else ''
            item['title'] = title.strip()
        item['page_url'] = response.url
        # print item['page_url']
        item['content'] = response.body_as_unicode()
        yield item

    def closed(self, reason):
        self.oracleFetchConn.close()
