import ssl
import json
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

from stocklib import CompanyCodeCrawler
from stocklib import StockPriceCrawler
from stocklib import Profiler

from stockdaolib import StockDao
import json
import os

companyCrawler = CompanyCodeCrawler()
stockPriceCrawler = StockPriceCrawler()

profiler = Profiler()

##############################################################################################
# 1. Get company code
##############################################################################################
company_list = companyCrawler.getCompanyCode()

##############################################################################################
# 2. Get stock prices
##############################################################################################
profiler.start()
stock_price_list = stockPriceCrawler.getStockPrice_Multithread(company_list, 16)
profiler.end()

##############################################################################################
# 3. Store stock prices into Database
##############################################################################################
config_path = os.path.dirname(__file__) + '/config.json'

#print(config_path)

with open(config_path) as f:
    config = json.load(f)

HOST = config['DATASOURCE']['HOST']
USERNAME = config['DATASOURCE']['USERNAME']
PASSWORD = config['DATASOURCE']['PASSWORD']

stockdao = StockDao(HOST, USERNAME, PASSWORD)
stockdao.insertStockPriceListBatch(stock_price_list)




