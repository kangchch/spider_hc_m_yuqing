# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import datetime
import cx_Oracle
from scrapy.conf import settings
from scrapy import log
import logging
from scrapy.exceptions import DropItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

os.system('export LANG=zh_CN.GB18030')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'


class BaiduMYuqingPipeline(object):

    def __init__(self):
        self.logger = logging.getLogger('baidu_m_HuiCongYuQing')
        self.oracleConn = None
        try:
            connstr = "%s/%s@%s/%s" % (
                    settings['ORACLE_SERVER_USERNAME'],
                    settings['ORACLE_SERVER_PASSWORD'],
                    settings['ORACLE_SERVER_ADDR'],
                    settings['ORACLE_SERVER_DBNAME'])
            self.oracleConn = cx_Oracle.connect(connstr)
        except Exception, err:
            self.logger.error("Connection Oracle Error!: %s" % (err,))

    def process_item(self, item, spider):

        if not item:
            return
        #pdb.set_trace()

        keywordset = settings.get('JUDGE_KEYWORDS', ())
        hit_keywords = []
        result_item = {}
        for keyword in keywordset:
            if item['page_url'].find('hc360.com') > 0:
                continue

            if keyword in item['title'] or keyword in item['content'] or keyword in item['introduce'] or keyword in item['dropdown'] or keyword in item['related']:
                hit_keywords.append(keyword)

            # add 判定词是否在简介里
            if keyword in item['introduce'] or keyword in item['title']:
                item['has_no'] = 'has'

            # add 判定词是否在下拉词中
            # if keyword.encode('utf-8', 'ignore') in item['dropdown']:
                # result_item['dropdown'] = item['dropdown']

            # add 判定词是否在相关词中
            # if keyword in item['related']:
                # result_item['related'] = item.get(u'related', u'')


        if not hit_keywords:
            return item

        result_item['index'] = item['index']
        result_item['keyword'] = item['keyword']
        result_item['judge_keywords'] = ','.join(hit_keywords)
        result_item['page_url'] = item.get(u'page_url', u'')
        result_item['title'] = item.get(u'title', u'')
        result_item['introduce'] = item.get(u'introduce', u'')
        result_item['ranking'] = item.get(u'ranking', u'')
        result_item['page_index'] = item.get(u'page_index', u'')
        result_item['has_no'] = item['has_no']
        result_item['media_name'] = item.get(u'media_name', u'')  ##只有资讯和贴吧有媒体名称
        result_item['source'] = item['source']
        result_item['dropdown'] = item.get(u'dropdown', u'')
        result_item['related'] = item.get(u'related', u'')
        self.insertOracle(result_item)

    def insertOracle(self, item):
        cr = self.oracleConn.cursor()
        exesql = settings['INSERT_SQL'].format(
                    keyword = item['keyword'],
                    judge_keywords = item['judge_keywords'],
                    page_url = item['page_url'],
                    title = item['title'],
                    source = item['source'],
                    ranking = item['ranking'],
                    page_index = item['page_index'],
                    media_name = item['media_name'],
                    introduce = item['introduce'],
                    has_no = item['has_no'],
                    dropdown = item['dropdown'],
                    related = item['related']
               )

        try:
            cr.execute(exesql)
            self.oracleConn.commit()
            cr.close()
            self.log('insert into succed!')
            self.updateOracle(item)
        except Exception, err:
            self.logger.error(u'{0:s} ERROR!'.format(exesql))
    def updateOracle(self, item):
        cr = self.oracleConn.cursor()
        exesql = settings['UPDATE_HUICONG_YUQING_KEYWORD_TBL_SQL'].format(item['source'], item['index'])
        try:
            cr.execute(exesql)
            self.oracleConn.commit()
            cr.close()
            self.log('update succed!')
        except Exception, err:
            self.logger.error(u'{0:s} ERROR!'.format(exesql))


