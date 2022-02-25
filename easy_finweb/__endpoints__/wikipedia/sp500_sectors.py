import requests
import pandas as pd

from ...__utility__ import config 
from ...__utility__ import fetcher

def get(ticker):
    return snapshot().query(f"Symbol == '{ticker}'")

def snapshot():
    return pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies', header = 0)[0]


