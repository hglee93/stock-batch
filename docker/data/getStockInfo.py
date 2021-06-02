import ssl
import json
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

from stocklib import CompanyCodeCrawler
from stocklib import StockPriceCrawler
from stocklib import Profiler

from stockdaolib import StockDao

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
print("%0.2f seconds" % (profiler.getResult() / 1000))

##############################################################################################
# 3. Store stock prices into Database
##############################################################################################
stockdao = StockDao("localhost", "root", "1234")
stockdao.insertStockPriceListBatch(stock_price_list)

print("Completed!")




