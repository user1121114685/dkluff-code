#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import json
import re
import requests
from lxml.html import fromstring

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

def fmt(arr,lot_type=1):
    tt_nums=len(arr)

    rs=[]
    j=-1
    if lot_type == 1: j=7
    if j<0: return rs
    #lot grouo count
    lg=int(tt_nums/j)

    rs=[[ 0 for col in range(j)] for row in range(lg) ]
    i=0
    while i<lg:
        for k in range(j):
            rs[i][k]=arr[lg*k+i]
        i+=1

    return rs

def match_balls(myb,opb):
    c=0
    r=[]
    for b in myb:
        if b in opb:
            c+=1
            b="*"+b
        r.append(b)
    return [r,c]


def check_lot(arr,lotser,lot_type=1):
    urls={1:"http://caipiao.163.com/award/dlt/%s.html",}
    url=urls[lot_type] % lotser

    bingo=" <-- Yes,God!! Bingo... !!!\n"
    myresult=""

    if lot_type == 1:
        r=requests.get(url)
        doc=fromstring(r.text).get_element_by_id("zj_area")

        redb=[el.text_content() for el in doc.find_class('red_ball')]
        blueb=[el.text_content() for el in doc.find_class('blue_ball')]
        print("DrawWin:",redb,blueb)
        if redb[0] == "": return ["Wait for draw...!"]

        for ar in arr:
            print("Matching: ",ar)
            redm=match_balls(ar[:-2],redb)
            bluem=match_balls(ar[-2:],blueb)
            if bluem[1] >= 2 or bluem[1]+redm[1] >=3:
                a=""
                for i in redm[0]+["+"]+bluem[0]:
                    a+=str(i)+" "
                a+=bingo
                myresult+=a
                

    return myresult


if __name__ == "__main__":
    usage="""
        Usage: ./chklot.py filename ser type
               type list:
                    1 - 体彩／超级大乐透
    """
    print(usage)

    image=sys.argv[1]
    lot_ser=sys.argv[2]
    lot_type=int(sys.argv[3])
    
    #start testblock
   # print("testing...")
   # txt=[1,2,3,4,'35','08','09',8,'1',10,'08',12,'09',14]
   # print(check_lot(fmt(txt),lot_ser,1))
   # sys.exit(1)
    #end testblock


    print("Loading...")
    r=""
    r=ocr_space_file(filename=image,api_key='key')
    r=json.loads(r)

    txt=r["ParsedResults"][0]["ParsedText"]
    txt=re.sub("[^0-9 ]","",txt).split()

    print(check_lot(fmt(txt),lot_ser,1))



