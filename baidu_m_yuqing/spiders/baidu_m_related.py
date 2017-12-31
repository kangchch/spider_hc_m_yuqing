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
    name = "baidu_m_related"

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
        exesql = settings['GET_HUICONG_YUQING_KEYWORD_SQL'].format('baidu_m_related'.upper(), settings['SELECT_STEP'])
        ret = cr.execute(exesql)
        self.start_urls = ret.fetchall()
        cr.close()

    def start_requests(self):
        #pdb.set_trace()
        for index, keyword, page_max in  self.start_urls:
            keyword = keyword.decode('GBK')
            item = BaiduMYuqingItem()
            item['index'] = index
            item['keyword'] = keyword
            item['source'] = 'baidu_m_related'
            item['page_index'] = ''
            item['has_no'] = ''
            item['media_name'] = ''
            item['title'] = ''
            item['introduce'] = ''
            item['ranking'] = ''
            item['page_url'] = ''
            item['content'] = ''
            item['dropdown'] = ' '
            item['related'] = ''
            cur_url = 'http://m.baidu.com/s?'
            ky = keyword.encode('gb18030')
            url = cur_url + '&word=%s' % (ky)
            meta = {'item': item, 'dont_retry': True}
            self.log('insert new keyword=%s index=%d ' %
                     (keyword, index), level=log.INFO)
            yield scrapy.Request(url=url, callback=self.parse, meta=meta, dont_filter=True)
        # keywords = [u'慧聪网可靠么']
        # for keyword in keywords:
            # index = 0
            # # keyword = keyword.decode('GBK')
            # item = BaiduMYuqingItem()
            # item['index'] = index
            # item['keyword'] = keyword
            # item['source'] = 'baidu_m_related'
            # item['has_no'] = ''
            # item['media_name'] = ''
            # item['title'] = ''
            # item['introduce'] = ''
            # item['ranking'] = ''
            # item['page_url'] = ''
            # item['content'] = ''
            # item['dropdown'] = ''
            # cur_url = 'http://m.baidu.com/s?'
            # # ky = keyword.encode('gb18030')
            # ky = keyword
            # url = cur_url + '&word=%s' % (ky)
            # meta = {'item': item, 'dont_retry': True}
            # self.log('insert new keyword=%s index=%d ' %
                     # (keyword, index ), level=log.INFO)
            # yield scrapy.Request(url=url, callback=self.parse, meta=meta, dont_filter=True)


    def parse(self, response):
        #pdb.set_trace()
        item = response.meta['item']

        if response.status != 200:
            self.log('fetch failed! keyword=%s index=%d status=%d jump_url=%s' %
                     (item['keyword'], item['index'], item['status'], response.headers.get('Location', '')), level=log.WARNING)
            if response.status == 302 and response.headers.get('Location', '').find('vcode') > 0:
                ##block
                return
            else:
                yield item

        handles = response.xpath("//a[@class='rw-item']")
        for handle in handles:
            related = handle.xpath("text()").extract()
            item['related'] = related[0] if related else ''
            # print item['related']
            # print type(item['related'])
            yield item

    def closed(self, reason):
        self.oracleFetchConn.close()
