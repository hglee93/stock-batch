import json

import pandas as pd
import ssl
import json
from urllib.request import urlopen, Request
from urllib import request

class StockCodeParser:
    def __init__(self):
        self.url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&marketType=stockMkt'
        self.ssl_context = ssl._create_unverified_context()

    # 종목 코드 다운로드
    def parse(self):
        response = request.urlopen(self.url, context=self.ssl_context)
        html = response.read()

        df_stock_code = pd.read_html(html, header=0)[0]
        df_stock_code.종목코드 = df_stock_code.종목코드.map('{:06d}'.format)
        stock_code_list = df_stock_code.종목코드.values.tolist()
        return stock_code_list

class StockPriceParser:
    def __init__(self):
        self.base_url = "https://api.finance.naver.com/service/itemSummary.nhn?itemcode={}"
        self.ssl_context = ssl._create_unverified_context()

    def read(self, stock_code_list):

        stock_object_list = []

        for stock_code in stock_code_list:
            req_url = self.base_url.format(stock_code)
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            req = Request(url=req_url, headers=headers)
            result = urlopen(req, context=self.ssl_context).read()
            stock_object = json.loads(result)
            stock_object_list.append(stock_object)

        return stock_object_list

def lambda_handler(event, context):
    # TODO implement
    scparser = StockCodeParser()
    spparser = StockPriceParser()
    
    sc_list = scparser.parse()
    stock_price_list = spparser.read(sc_list)

    print(stock_price_list)

    return {
        'statusCode': 200,
        'body': json.dumps(stock_price_list)
    }