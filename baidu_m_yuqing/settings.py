# -*- coding: utf-8 -*-

# Scrapy settings for baidu_m_yuqing project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'baidu_m_yuqing'

SPIDER_MODULES = ['baidu_m_yuqing.spiders']
NEWSPIDER_MODULE = 'baidu_m_yuqing.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baidu_m_yuqing (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'baidu_m_yuqing.middlewares.BaiduMYuqingSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'baidu_m_yuqing.downloadmiddleware.anti_ban.AntiBanMiddleware': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'baidu_m_yuqing.pipelines.BaiduMYuqingPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = [403, 500]
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ORACLE_SERVER_ADDR= "192.168.100.148:1521"
ORACLE_SERVER_USERNAME = "snatch"
ORACLE_SERVER_PASSWORD = "e3hAbdiK"
ORACLE_SERVER_DBNAME = "snatch"

GET_HUICONG_YUQING_KEYWORD_SQL=u'select id, keyword, search_max_page from HUICONG_QUQING_KEYWORD_TBL where {0:s}_FETCH_STATUS = 0 and rownum < {1:d}'
SELECT_STEP = 100

INSERT_SQL=u""\
u"insert into huicong_yuqing_info_tbl(id, keyword, judge_keywords, page_url, title, source, ranking, page_index, media_name, introduce, has_no, dropdown, related) "\
u"values(huicong_yuqing_info_tbl_seq.nextval,'{keyword}','{judge_keywords}','{page_url}','{title}','{source}','{ranking}','{page_index}','{media_name}','{introduce}','{has_no}','{dropdown}','{related}')"


UPDATE_HUICONG_YUQING_KEYWORD_TBL_SQL="update HUICONG_QUQING_KEYWORD_TBL set {0:s}_FETCH_STATUS = 1 where id = {1:d}"

SPIDER_INFO = {
    'ID': 'TJ_01',
    'SUB_ID': 4,
    'SUB_NUM': 6,
    'TJ_PROXY': True,
    'PUB_PROXY': False,
    'MULTI_IP': {'MONGO': False,
                 'LOCALE_ALL': False,
                 'LOCALE_ONE': False,
                 'NEED_AUTH': False}
}

AUTOTHROTTLE_ENABLED = False
# EXTENSIONS = {
            # 'HuiCong_YuQing.extensions.AutoThrottleWithList.AutoThrottleWithList':300,
            # }

JUDGE_KEYWORDS = (u'骗人', u'骗子', u'垃圾', u'坑人', u'诈骗', u'无良', u'骗局', u'倒闭', u'破产', u'圈套', u'骗钱', u'欺骗')

LOG_LEVEL = 'INFO'
# LOG_FILE = 'logs/spider.log'
