#!/Users/dkluffy/anaconda/envs/py27/bin/python
# -*- coding: utf-8 -*-

#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

"""
nt tick_history http://quotes.money.163.com/cjmx/2017/20170626/1000766.xls
"""
TICK_PRICE_URL_NT = "http://quotes.money.163.com/cjmx/%s/%s/%s.xls"
TICK_COLUMNS = ['time', 'price', 'change', 'volume', 'amount', 'type']

SRC_URL = {
            "nt": {"tk":TICK_PRICE_URL_NT,},

            }

if __name__ == '__main__':
    srcurl = SRC_URL['nt']['tk'] % ( '2017','20170627','1000766' )
    print srcurl

