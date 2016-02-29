#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://api.money.126.net/data/feed/1002092,money.api

tdlist = {
    "week":["下跌趋势","上升趋势"],
    "day":["低开","高开"],
    "now":["低走","高走"],}


def getTrend(oldp,newp,cyc):
    a = tdlist[cyc]

    if oldp < newp:
        return tdlist[cyc][1]
    return tdlist[cyc][0]

#parr=[yestclose,open,price,high,low,byestclose]
def calclose(parr):
    maxclose = parr[0]*1.1
    minclose = parr[0]*0.9
