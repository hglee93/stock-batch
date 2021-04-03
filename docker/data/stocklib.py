import pandas as pd
import ssl
import json
from urllib.request import urlopen
from urllib import request
import time
from threading import Thread

class CompanyCodeCrawler:
    def __init__(self):
        self.url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType=stockMkt'
        self.ssl_context = ssl._create_unverified_context()

    # Download CompanyCode
    def getCompanyCode(self):
        response = request.urlopen(self.url, context=self.ssl_context)
        html = response.read()

        df_stock_code = pd.read_html(html, header=0)[0]
        df_stock_code.종목코드 = df_stock_code.종목코드.map('{:06d}'.format)
        stock_code_list = df_stock_code.종목코드.values.tolist()
        
        return stock_code_list

class StockPriceCrawler:
    def __init__(self):
        self.base_url = "https://api.finance.naver.com/service/itemSummary.nhn?itemcode={}"
        self.ssl_context = ssl._create_unverified_context()

    def getStockPrice(self, stock_code_list):
        stock_object_list = []
        for stock_code in stock_code_list:
            req_url = self.base_url.format(stock_code)
            result = urlopen(req_url, context=self.ssl_context).read()
            stock_object = json.loads(result)
            stock_object["company"] = stock_code
            stock_object_list.append(stock_object)

        return stock_object_list

    ##############################################################################################
    # MultiThread Version
    # when max_threads is 16, the execution time of this function is shorter 16 times than that of single thread 
    ##############################################################################################
    def getStockPrice_Multithread(self, stock_code_list, max_threads):
        stock_object_list = list()
        threads = list()

        step = len(stock_code_list) / max_threads

        for i in range(max_threads):
            start = int(i * step)
            end = int((i + 1) * step)
            sub_list = stock_code_list[start:end] if i < max_threads - 1 else stock_code_list[start:]
            threads.append(Thread(target=self.work, args=(sub_list, stock_object_list)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return stock_object_list

    def work(self, target_list, stock_object_list):
        for target_code in target_list:
            req_url = self.base_url.format(target_code)
            result = urlopen(req_url, context=self.ssl_context).read()
            stock_object = json.loads(result)
            stock_object["company"] = target_code
            stock_object_list.append(stock_object)

class Profiler:

    def start(self):
        self.startTime = int(round(time.time() * 1000))
    
    def end(self):
        self.endTime = int(round(time.time() * 1000))
    
    def getResult(self):
        return self.endTime - self.startTime

