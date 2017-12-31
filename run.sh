#!/bin/bash
cd /app/spider_hc_m_yuqing
rm *.log nohup.out -rf
nohup scrapy crawl baidu_m_quanbu --logfile log_baidu_m_quanbu.log  > nohup_quanbu.out 2>&1 &
nohup scrapy crawl baidu_m_zixun --logfile log_baidu_m_zixun.log > nohup_zixun.out 2>&1 &
nohup scrapy crawl baidu_m_tieba --logfile log_baidu_m_tieba.log > nohup_tieba.out 2>&1 &
nohup scrapy crawl baidu_m_wenda --logfile log_baidu_m_wenda.log > nohup_wenda.out 2>&1 &
nohup scrapy crawl baidu_m_dropdown --logfile log_baidu_m_dropdown.log > nohup_wenda.out 2>&1 &
nohup scrapy crawl baidu_m_related --logfile log_baidu_m_related.log > nohup_wenda.out 2>&1 &
