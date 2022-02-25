import pandas as pd
import datetime as dt

def get(historical=False):
    return fetch_suspensions() if not historical \
    else   fetch_historical_suspensions()
         
def fetch_suspensions():
    df = pd.read_csv('https://www.nyse.com/api/trade-halts/current/download')
    tm = pd.Series(pd.to_datetime('now')).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')[0]
    df['timestamp'] = tm

    df = df.set_index('Symbol')
    df.index.name='ticker'

    print('  [{}] Halts       {}'.format(str(dt.datetime.today().time())[:-10], df.shape))

    return df

def fetch_historical_suspensions():
    df = pd.read_csv('https://www.nyse.com/api/trade-halts/historical/download?symbol=&reason=&sourceExchange=&haltDateFrom=2020-10-02&haltDateTo=')
    tm = pd.Series(pd.to_datetime('now')).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')[0]
    df['timestamp'] = tm

    df = df.set_index('Symbol')
    df.index.name='ticker'

    print('  [{}] Halts       {}'.format(str(dt.datetime.today().time())[:-10], df.shape))

    return df
    