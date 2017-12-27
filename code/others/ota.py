#!/root/anaconda2/bin/python2
# -*- coding: UTF-8 -*-

import sys
import csv
import xlrd
import codecs

HEAD_SUBTAB = "级别,子件行号,工序行号,工序名称,子件编码,子件名称,子件规格,子件计量单位,基本用量,基础数量,子件损耗率,辅助单位,换算率,辅助基本用量,辅助使用量,固定用量,供应类型,使用数量,子件生效日,子件失效日,偏置期,计划比例,产出品,产出类型,成本相关,可选否,选择规则,仓库名称,领料部门名称,定位符,备注"

HEAD_MTAB = "母件编码,母件名称,母件规格,母件计量单位,母件损耗率,版本代号,版本说明,版本日期,状态"

def Excel2CSV(ExcelFile,CSVFile):
     workbook = xlrd.open_workbook(ExcelFile)
     worksheet = workbook.sheets()[0]
     csvfile = open(CSVFile, 'wb')
     wr = csv.writer(csvfile)
     #wr = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)

     for rownum in xrange(worksheet.nrows):
         wr.writerow( list( x for x in worksheet.row_values(rownum)))
         #wr.writerow( list(x.encode('utf-8') if type(x) == type(u'') else x
                  #for x in worksheet.row_values(rownum)))

     csvfile.close()


def tab2csv(tab,outfile,fields=""):
    csvfile = open(outfile, 'wb')
    wr = csv.writer(csvfile)

    if len(fields)>0:
        wr.writerow(list(x for x in fields))
    for l in tab:
        #wr.writerow(list(x.encode('gb2312') if isinstance(x,unicode) else x for x in l))
        wr.writerow(list(x for x in l ))

    csvfile.close()


def fmtcsv(csvfile):
    f = open(csvfile)
    mc_str = "母件编码"
    mtable = []

    subtable = []

    mc = ""
    for l in f:
        sl = l.split(",")[:-1]
        if mc != "" and ("+" in sl[0]):
            subtable.append([mc]+sl)

        if mc_str in sl[0]:
            m_i = f.next()
            mtable.append(m_i.split(",")[:-1])
            mc = m_i.split(",")[0]

    return mtable,subtable

def ReadFile(filePath,encoding="utf-8"):
    with codecs.open(filePath,"r",encoding) as f:
        return f.read()

def WriteFile(filePath,u,encoding="gbk"):
    with codecs.open(filePath,"w",encoding) as f:
        f.write(u)

def convtfile(src,dst,codec="gb18030"):
    content = ReadFile(src,encoding="utf-8")
    WriteFile(dst,content,encoding=codec)


def test():
    #Excel2CSV("a.xlsx","tg.csv")
    #m,s = fmtcsv("tg.csv")
    #print s[0][6],[x.decode("utf-8").encode("gb2312") for x in s[0] ]
    #tab2csv(s,"sub1.csv",list(HEAD_SUBTAB.split(",")) )

    convtfile("sub1.csv","gb.csv")

if __name__ == "__main__":

	test()






