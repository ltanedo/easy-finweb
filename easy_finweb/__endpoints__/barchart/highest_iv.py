
import requests
from urllib.parse import unquote
import pandas as pd
import datetime as dt

def get():
    geturl=r'https://www.barchart.com/options/highest-implied-volatility'
    apiurl=r'https://www.barchart.com/proxies/core-api/v1/quotes/get'


    getheaders={

        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }

    getpay={
        'page': 'all'
    }

    s=requests.Session()
    r=s.get(geturl,params=getpay, headers=getheaders)

    headers={
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.barchart.com/options/highest-implied-volatility?page=all',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'x-xsrf-token': unquote(unquote(s.cookies.get_dict()['XSRF-TOKEN']))
    }

    apiurl ="""https://www.barchart.com/proxies/core-api/v1/options/get?fields=symbol%2CbaseSymbol%2CbaseLastPrice%2CbaseSymbolType%2CsymbolType%2CstrikePrice%2CexpirationDate%2CdaysToExpiration%2CbidPrice%2Cmidpoint%2CaskPrice%2ClastPrice%2Cvolume%2CopenInterest%2CvolumeOpenInterestRatio%2Cvolatility%2CtradeTime%2CsymbolCode%2ChasOptions\
&orderBy=volatility\
&baseSymbolTypes=stock\
&between(lastPrice%2C.10%2C)\

=&between(daysToExpiration%2C{}%2C)\
=&between(tradeTime%2C{}%2C{})\

=&orderDir=desc&between(volatility%2C60%2C)\
=&limit={}\
&between(volume%2C500%2C)\
=&between(openInterest%2C100%2C)\
=&in(exchange%2C(AMEX%2CNASDAQ%2CNYSE))\
=&meta=field.shortName%2Cfield.type%2Cfield.description&hasOptions=true&raw=1"""

    # today = (dt.datetime.today() + dt.timedelta(days=3)).strftime('%Y-%m-%d')
    daysToExpiration = "15"
    begin = (dt.datetime.today() + dt.timedelta(days=-3)).strftime('%Y-%m-%d')
    end = (dt.datetime.today() + dt.timedelta(days=3)).strftime('%Y-%m-%d')
    limit = "200"

    apiurl = apiurl.format(daysToExpiration,begin,end, limit)
    r=s.get(apiurl,headers=headers)
    j=r.json()

    df = pd.json_normalize(j["data"])
    # df.to_csv("options.csv")

    tm = pd.Series(pd.to_datetime('now')).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')[0]
    df['timestamp'] = tm

    df = df.drop(columns=['raw.symbol',
       'raw.baseSymbol', 'raw.baseLastPrice', 'raw.baseSymbolType',
       'raw.symbolType', 'raw.strikePrice', 'raw.expirationDate',
       'raw.daysToExpiration', 'raw.bidPrice', 'raw.midpoint', 'raw.askPrice',
       'raw.lastPrice', 'raw.volume', 'raw.openInterest',
       'raw.volumeOpenInterestRatio', 'raw.volatility', 'raw.tradeTime'], axis=1)

    df = df.set_index('baseSymbol')
    df.index.name = 'ticker'

    print('  [{}] Options_IV  {}'.format(str(dt.datetime.today().time())[:-10], df.shape))

    return df

# df = df['symbol'].str.split('|',expand=True).set_axis(['ticker','expiration','premium'],axis=1)
