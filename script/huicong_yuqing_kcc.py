#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlwt
import xlsxwriter
import pdb
import cx_Oracle
import datetime
import smtplib
from email.mime.text import MIMEText

sys.path.append('/tools/python_common')
from send_mail import *

warning_mail_list = [
    PHONE_MAIL['kangchaochao@hc360.com']
]

ORACLE_SERVER_ADDR = "192.168.100.148:1521"
ORACLE_SERVER_USERNAME = "snatch"
ORACLE_SERVER_PASSWORD = "e3hAbdiK"
ORACLE_SERVER_DBNAME = "snatch"



CHANNEL_DICT = {
        u'baidu_wangye' :u'百度网页',
        u'baidu_xinwen' :u'百度新闻',
        u'so_wangye' : u'360搜索网页',
        u'so_xinwen' : u'360搜索新闻',
        u'sogou_wangye' : u'搜狗搜索网页',
        u'sogou_xinwen' : u'搜狗搜索新闻',
        u'baidu_m_quanbu' : u'百度移动全部',
        u'baidu_m_tieba' : u'百度移动贴吧',
        u'baidu_m_wenda' : u'百度移动问答',
        u'baidu_m_zixun' : u'百度移动资讯',
        }

CHANNEL_SPECIAL_DICT = {
        u'baidu_zhidao' :u'百度知道',
        u'baidu_wenku' : u'百度文库',
        u'baidu_tieba' : u'百度贴吧',
        # u'baidu_m_dropdown' : u'百度移动下拉词',
        # u'baidu_m_related' : u'百度移动联想词',
        u'baidu_m_droprelated' : u'百度移动下拉联想词',
        }

if  __name__ == '__main__':

    DIR_PATH = os.path.split(os.path.realpath(__file__))[0]
    LOG_FILE = DIR_PATH + '/logs/' + __file__.replace('.py', '.log')
    logInit(logging.INFO, LOG_FILE, 0, True)

    oracleConn = None
    now = datetime.datetime.now()
    try:
        connstr = "%s/%s@%s/%s" % (
                ORACLE_SERVER_USERNAME,
                ORACLE_SERVER_PASSWORD,
                ORACLE_SERVER_ADDR,
                ORACLE_SERVER_DBNAME)
        oracleConn = cx_Oracle.connect(connstr)
    except Exception, err:
        print("Connection Oracle Error!: %s" % (err,))
    book = xlsxwriter.Workbook('HuiCong_YuQing_{0:04d}_{1:02d}_{2:02d}.xlsx'.format(now.year, now.month, now.day), {'strings_to_urls': False})
    tc = 0
    for channel in CHANNEL_DICT.keys():
        sheet1 = book.add_worksheet(CHANNEL_DICT[channel])
        sheet1.write(0, 0, u'频道')
        sheet1.write(0, 1, u'搜索关键字')
        sheet1.write(0, 2, u'判定关键词')
        sheet1.write(0, 3, u'搜索标题')
        sheet1.write(0, 4, u'简介')
        sheet1.write(0, 5, u'标题简介有无判定关键词')
        sheet1.write(0, 6, u'页数')
        sheet1.write(0, 7, u'排名')
        sheet1.write(0, 8, u'媒体名称')
        sheet1.write(0, 9, u'需要处理的快照链接')
        sheet1.write(0, 10, u'原链接')
        #TODO
        count = 1
        cr = oracleConn.cursor()
        # cr.execute("select source, keyword, judge_keywords, title, snapshoot_url, page_url from huicong_yuqing_info_tbl where source = '{0:s}' and to_char(insert_time, 'yyyy-mm-dd') = '{1:04d}-{2:02d}-{3:02d}'".format(channel, now.year, now.month, now.day))
        cr.execute("select source, keyword, judge_keywords, title, introduce, has_no, page_index, ranking, media_name, snapshoot_url, page_url from huicong_yuqing_info_tbl where source = '{0:s}' and insert_time > sysdate-6".format(channel))
        for ele in cr:
            if ele[10] and ele[10].find('hc360.com') > 0:
                continue
            sheet1.write(count, 0, CHANNEL_DICT[ele[0]])
            sheet1.write(count, 1, ele[1].decode('GBK')  if ele[1] else u'')
            sheet1.write(count, 2, ele[2].decode('GBK')  if ele[2] else u'')
            sheet1.write(count, 3, ele[3].decode('GBK')  if ele[3] else u'')
            sheet1.write(count, 4, ele[4].decode('GBK')  if ele[4] else u'')
            sheet1.write(count, 5, ele[5].decode('GBK')  if ele[5] else u'')
            sheet1.write(count, 6, ele[6].decode('GBK')  if ele[6] else u'')
            sheet1.write(count, 7, ele[7].decode('GBK')  if ele[7] else u'')
            sheet1.write(count, 8, ele[8].decode('GBK')  if ele[8] else u'')
            sheet1.write(count, 9, ele[9].decode('GBK')  if ele[9] else u'')
            sheet1.write(count, 10, ele[10].decode('GBK')  if ele[10] else u'')
            count = count + 1
            tc += 1
        #book.save('book.xls')
        cr.close()

    #baidu_wenku
    sheet1 = book.add_worksheet(CHANNEL_SPECIAL_DICT['baidu_wenku'])
    sheet1.write(0, 0, u'频道')
    sheet1.write(0, 1, u'搜索关键字')
    sheet1.write(0, 2, u'判定关键词')
    sheet1.write(0, 3, u'简介')
    sheet1.write(0, 4, u'标题简介有无判定关键词')
    sheet1.write(0, 5, u'页数')
    sheet1.write(0, 6, u'排名')
    sheet1.write(0, 7, u'媒体名称')
    sheet1.write(0, 8, u'文库标题')
    sheet1.write(0, 9, u'需要处理的链接')
    count = 1
    cr = oracleConn.cursor()
    # cr.execute("select source, keyword, judge_keywords, title, page_url from huicong_yuqing_info_tbl where source = '{0:s}' and to_char(insert_time, 'yyyy-mm-dd') = '{1:04d}-{2:02d}-{3:02d}'".format('baidu_wenku', now.year, now.month, now.day))
    cr.execute("select source, keyword, judge_keywords, introduce, has_no, page_index, ranking, media_name, title, page_url from huicong_yuqing_info_tbl where source = '{0:s}' and insert_time > sysdate-6".format('baidu_wenku'))
    for ele in cr:
        if ele[9] and ele[9].find('hc360.com') > 0:
            continue
        sheet1.write(count, 0, CHANNEL_SPECIAL_DICT[ele[0]])
        sheet1.write(count, 1, ele[1].decode('GBK')  if ele[1] else u'')
        sheet1.write(count, 2, ele[2].decode('GBK')  if ele[2] else u'')
        sheet1.write(count, 3, ele[3].decode('GBK')  if ele[3] else u'')
        sheet1.write(count, 4, ele[4].decode('GBK')  if ele[4] else u'')
        sheet1.write(count, 5, ele[5].decode('GBK')  if ele[5] else u'')
        sheet1.write(count, 6, ele[6].decode('GBK')  if ele[6] else u'')
        sheet1.write(count, 7, ele[7].decode('GBK')  if ele[7] else u'')
        sheet1.write(count, 8, ele[8].decode('GBK')  if ele[8] else u'')
        sheet1.write(count, 9, ele[9].decode('GBK')  if ele[9] else u'')
        count = count + 1
        tc += 1
    cr.close()

    #baidu_tieba
    sheet1 = book.add_worksheet(CHANNEL_SPECIAL_DICT['baidu_tieba'])
    sheet1.write(0, 0, u'频道')
    sheet1.write(0, 1, u'搜索关键字')
    sheet1.write(0, 2, u'判定关键词')
    sheet1.write(0, 3, u'简介')
    sheet1.write(0, 4, u'标题简介有无判定关键词')
    sheet1.write(0, 5, u'页数')
    sheet1.write(0, 6, u'排名')
    sheet1.write(0, 7, u'媒体名称')
    sheet1.write(0, 8, u'贴吧名称')
    sheet1.write(0, 9, u'帖子标题')
    sheet1.write(0, 10, u'需要处理的链接')
    count = 1
    cr = oracleConn.cursor()
    # cr.execute("select source, keyword, judge_keywords, tieba_name, title, page_url from huicong_yuqing_info_tbl where source = '{0:s}' and to_char(insert_time, 'yyyy-mm-dd') = '{1:04d}-{2:02d}-{3:02d}'".format('baidu_tieba', now.year, now.month, now.day))
    cr.execute("select source, keyword, judge_keywords, introduce, has_no, page_index, ranking, media_name, tieba_name, title, page_url from huicong_yuqing_info_tbl where source = '{0:s}' and insert_time > sysdate-6".format('baidu_tieba'))
    for ele in cr:
        if ele[10] and ele[10].find('hc360.com') > 0:
            continue
        sheet1.write(count, 0, CHANNEL_SPECIAL_DICT[ele[0]])
        sheet1.write(count, 1, ele[1].decode('GBK')  if ele[1] else u'')
        sheet1.write(count, 2, ele[2].decode('GBK')  if ele[2] else u'')
        sheet1.write(count, 3, ele[3].decode('GBK')  if ele[3] else u'')
        sheet1.write(count, 4, ele[4].decode('GBK')  if ele[4] else u'')
        sheet1.write(count, 5, ele[5].decode('GBK')  if ele[5] else u'')
        sheet1.write(count, 6, ele[6].decode('GBK')  if ele[6] else u'')
        sheet1.write(count, 7, ele[7].decode('GBK')  if ele[7] else u'')
        sheet1.write(count, 8, ele[8].decode('GBK')  if ele[8] else u'')
        sheet1.write(count, 9, ele[9].decode('GBK')  if ele[9] else u'')
        sheet1.write(count, 10, ele[10].decode('GBK')  if ele[10] else u'')
        count = count + 1
        tc += 1
    cr.close()
    #baidu_zhidao
    sheet1 = book.add_worksheet(CHANNEL_SPECIAL_DICT['baidu_zhidao'])
    sheet1.write(0, 0, u'频道')
    sheet1.write(0, 1, u'搜索关键字')
    sheet1.write(0, 2, u'判定关键词')
    sheet1.write(0, 3, u'简介')
    sheet1.write(0, 4, u'标题简介有无判定关键词')
    sheet1.write(0, 5, u'页数')
    sheet1.write(0, 6, u'排名')
    sheet1.write(0, 7, u'媒体名称')
    sheet1.write(0, 8, u'知道标题')
    sheet1.write(0, 9, u'投诉链接')
    sheet1.write(0, 10, u'侵权内容')
    sheet1.write(0, 11, u'侵权内容发布时间')
    count = 1
    cr = oracleConn.cursor()
    # cr.execute("select source, keyword, judge_keywords, title, page_url, zhidao_id, post_time from huicong_yuqing_info_tbl where source = '{0:s}' and to_char(insert_time, 'yyyy-mm-dd') = '{1:04d}-{2:02d}-{3:02d}'".format('baidu_zhidao', now.year, now.month, now.day))
    cr.execute("select source, keyword, judge_keywords, introduce, has_no, page_index, ranking, media_name, title, page_url, zhidao_id, post_time from huicong_yuqing_info_tbl where source = '{0:s}' and insert_time > sysdate-6".format('baidu_zhidao'))
    for ele in cr:
        if ele[9] and ele[9].find('hc360.com') > 0:
            continue
        sheet1.write(count, 0, CHANNEL_SPECIAL_DICT[ele[0]])
        sheet1.write(count, 1, ele[1].decode('GBK')  if ele[1] else u'')
        sheet1.write(count, 2, ele[2].decode('GBK')  if ele[2] else u'')
        sheet1.write(count, 3, ele[3].decode('GBK')  if ele[3] else u'')
        sheet1.write(count, 4, ele[4].decode('GBK')  if ele[4] else u'')
        sheet1.write(count, 5, ele[5].decode('GBK')  if ele[5] else u'')
        sheet1.write(count, 6, ele[6].decode('GBK')  if ele[6] else u'')
        sheet1.write(count, 7, ele[7].decode('GBK')  if ele[7] else u'')
        sheet1.write(count, 8, ele[8].decode('GBK')  if ele[8] else u'')
        sheet1.write(count, 9, ele[9].decode('GBK')  if ele[9] else u'')
        sheet1.write(count, 10, ele[10].decode('GBK')  if ele[10] else u'匿名')
        sheet1.write(count, 11, ele[11].decode('GBK')  if ele[11] else u'')
        count = count + 1
        tc += 1

    #baidu_m_dropdown
    sheet1 = book.add_worksheet(CHANNEL_SPECIAL_DICT['baidu_m_droprelated'])
    sheet1.write(0, 0, u'频道')
    sheet1.write(0, 1, u'搜索关键字')
    sheet1.write(0, 2, u'负面下拉词')
    sheet1.write(0, 3, u'负面联想词')
    count = 1
    cr = oracleConn.cursor()
    cr.execute("select source, keyword, dropdown, related from huicong_yuqing_info_tbl where source = '{0:s}' or source = '{1:s}' and insert_time > sysdate-6".format('baidu_m_dropdown', 'baidu_m_related'))
    # cr.execute("select source, keyword, dropdown from huicong_yuqing_info_tbl where source = '{0:s}'".format('baidu_m_dropdown'))
    for ele in cr:
        sheet1.write(count, 0, u'百度移动')
        sheet1.write(count, 1, ele[1].decode('GBK')  if ele[1] else u'')
        sheet1.write(count, 2, ele[2].decode('GBK')  if ele[2] else u'')
        sheet1.write(count, 3, ele[3].decode('GBK')  if ele[3] else u'')
        count = count + 1
        tc += 1
    cr.close()

    #baidu_m_related
    # sheet1 = book.add_worksheet(CHANNEL_SPECIAL_DICT['baidu_m_related'])
    # sheet1.write(0, 0, u'频道')
    # sheet1.write(0, 1, u'搜索关键字')
    # sheet1.write(0, 2, u'负面联想词')
    # count = 1
    # cr = oracleConn.cursor()
    # cr.execute("select source, keyword, dropdown from huicong_yuqing_info_tbl where source = '{0:s}' and insert_time > sysdate-6".format('baidu_m_dropdown'))
    # for ele in cr:
        # sheet1.write(count, 0, CHANNEL_SPECIAL_DICT[ele[0]])
        # sheet1.write(count, 1, ele[1].decode('GBK')  if ele[1] else u'')
        # sheet1.write(count, 2, ele[2].decode('GBK')  if ele[2] else u'')
        # count = count + 1
        # tc += 1
    # cr.close()

    book.close()

    title = u'{0:04d}{1:02d}{2:02d}慧聪负面新闻'.format(now.year, now.month, now.day)
    mail_send = ['gaozhenzhou@hc360.com',
                 'zhangdongtao@hc360.com',
                 'sutanbin@hc360.com',
                 'huangqian@hc360-inc.com',
                 'mabosen@hc360.com',
                 'kangchaochao@hc360.com',
                 'wangxiaojuan@hc360.com',
                 'shimiao@hc360.com',
                 'sunyingping@hc360.com']
    # mail_send = ['kangchaochao@hc360.com']
    body = ''
    send_mail(title, body, mail_send,'HuiCong_YuQing_{0:04d}_{1:02d}_{2:02d}.xlsx'.format(now.year, now.month, now.day))

    ## reset fetch status
    cr.execute(
        '''
        UPDATE HUICONG_QUQING_KEYWORD_TBL SET
            BAIDU_WANGYE_FETCH_STATUS=0,
            BAIDU_XINWEN_FETCH_STATUS=0,
            BAIDU_ZHIDAO_FETCH_STATUS=0,
            BAIDU_WENKU_FETCH_STATUS=0,
            BAIDU_TIEBA_FETCH_STATUS=0,
            SOGOU_WANGYE_FETCH_STATUS=0,
            SOGOU_XINWEN_FETCH_STATUS=0,
            SO_WANGYE_FETCH_STATUS=0,
            SO_XINWEN_FETCH_STATUS=0,
            BAIDU_M_QUANBU_FETCH_STATUS=0,
            BAIDU_M_TIEBA_FETCH_STATUS=0,
            BAIDU_M_WENDA_FETCH_STATUS=0,
            BAIDU_M_ZIXUN_FETCH_STATUS=0,
            BAIDU_M_DROPDOWN_FETCH_STATUS=0,
            BAIDU_M_RELATED_FETCH_STATUS=0
        '''
    )
    oracleConn.commit()
    cr.close()
    oracleConn.close()

    if tc == 0:
        warning_mail_title = u'[w]hcyq 0'
        send_mail(warning_mail_title.encode('utf-8'), warning_mail_title.encode('utf-8'), warning_mail_list)
