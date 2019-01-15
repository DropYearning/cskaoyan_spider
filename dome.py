# coding:utf-8
import re
import requests
import pymysql
import datetime
from bs4 import BeautifulSoup

# 使用pymysql进行数据库连接
conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='cskaoyan', charset='utf8')
cur = conn.cursor()

# 字典{缩写：URL}
COLLEGE_DICT = {
    'ZGKXY': 'forum-83-1.html',
    'QINGHUA': 'forum-84-1.html',
    'BEIDA': 'forum-85-1.html',
    'BEIHANG': 'forum-86-1.html',
    'HAGONGDA': 'forum-79-1.html',
    'DBDX': 'forum-80-1.html',
    'BEIYOU': 'forum-87-1.html',
    'JLDX': 'forum-81-1.html',
    'BEILI': 'forum-90-1.html',
    'SDDX': 'forum-93-1.html',
    'TJDX': 'forum-91-1.html',
    'DLLGDX': 'forum-82-1.html',
    'NKDX': 'forum-92-1.html',
    'BGD_BKD_BJD': 'forum-89-1.html',
    'RENDA_BEISHI': 'forum-88-1.html',
    'HEBGCDX': 'forum-231-1.html',
    'ZGHYDX': 'forum-281-1.html',
    'HB_HD_OTHER': 'forum-277-1.html',
    'SHANGJIAO': 'forum-95-1.html',
    'FUDAN': 'forum-98-1.html',
    'TONGJI': 'forum-99-1.html',
    'ZHEDA': 'forum-94-1.html',
    'ZGKXJSDX': 'forum-97-1.html',
    'GFKJDX': 'forum-121-1.html',
    'HUAKE': 'forum-102-1.html',
    'WHDX': 'forum-103-1.html',
    'DNDX': 'forum-100-1.html',
    'NJDX': 'forum-96-1.html',
    'ZNDX': 'forum-104-1.html',
    'HNDX': 'forum-105-1.html',
    'ZSDX': 'forum-106-1.html',
    'HNLGDX': 'forum-107-1.html',
    'HDLGDX_HDSFDX': 'forum-138-1.html',
    'XMDX_FZDX_NCDX': 'forum-272-1.html',
    'NJLG_NJHK_NJYD': 'forum-288-1.html',
    'WHLG_HZSD_HNSD': 'forum-274-1.html',
    'ZD_AD_SD_SD_HD': 'forum-276-1.html',
    'HZ_HD_HN_OTHER': 'forum-275-1.html',
    'XAJTDX': 'forum-108-1.html',
    'DZKJDX': 'forum-113-1.html',
    'XADZKJDX': 'forum-110-1.html',
    'XBGYDX': 'forum-109-1.html',
    'SCDX': 'forum-112-1.html',
    'CQDX': 'forum-111-1.html',
    'XB_XN_OTHER': 'forum-273-1.html'
}

# 获取当前日期
DATA_NOW = datetime.datetime.now().strftime("%Y-%m-%d")
print(DATA_NOW)
# 结果列表
RESULT_LIST = []


URL = "http://www.cskaoyan.com/forum.php"
URL_DATA = requests.get(URL).text
SOUP = BeautifulSoup(URL_DATA, 'html.parser')

# 分析并存储
def func():
    for u in COLLEGE_DICT.keys():
        parent_tag = SOUP.find('a', href = COLLEGE_DICT[u]).parent
        count_tag = parent_tag.find(class_="xw0 xi1")
        if count_tag != None:
            count_num = re.findall(r'\d+', count_tag.text)[0]
            count_num = int(count_num)
        else:
            count_num = 0
        RESULT_LIST.append(count_num)

func()
RESULT_LIST.append(DATA_NOW)
print(tuple(RESULT_LIST))

# 写入数据库
cur.execute("INSERT INTO wangdao(ZGKXY,QINGHUA,BEIDA,BEIHANG,HAGONGDA,DBDX,BEIYOU,JLDX,BEILI,SDDX,TJDX,DLLGDX,NKDX,BGD_BKD_BJD,RENDA_BEISHI,HEBGCDX,ZGHYDX,HB_HD_OTHER,SHANGJIAO,FUDAN,TONGJI,ZHEDA,ZGKXJSDX,GFKJDX,HUAKE,WHDX,DNDX,NJDX,ZNDX,HNDX,ZSDX,HNLGDX,HDLGDX_HDSFDX,XMDX_FZDX_NCDX,NJLG_NJHK_NJYD,WHLG_HZSD_HNSD,ZD_AD_SD_SD_HD,HZ_HD_HN_OTHER,XAJTDX,DZKJDX,XADZKJDX,XBGYDX,SCDX,CQDX,XB_XN_OTHER,TIMESTAMP) VALUES(%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,'%s')" % tuple(RESULT_LIST))
cur.connection.commit()
# 释放数据库连接
cur.close()
conn.close()

