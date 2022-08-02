"""
著作人:陳永順
"""
from xml.etree import ElementTree
import sys
import xml.etree.ElementTree as ET
import urllib.request as httplib
#  SSL  處理，  https    SSSSSS 就需要加上以下2行
import ssl
ssl._create_default_https_context = ssl._create_unverified_context    # 因.urlopen發生問題，將ssl憑證排除

######### 由網路下載 JSON 的 字串
# https://data.gov.tw/dataset/31897
# 109年男性部分時間就業者及受僱者人數
url="https://apiservice.mol.gov.tw/OdService/download/A17000000J-030256-mnK"
req = httplib.Request( url,data=None,
    headers={ 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"})
reponse = httplib.urlopen(req)               # 開啟連線動作
if reponse.code==200:                        # 當連線正常時
    contents=reponse.read()                  # 讀取網頁內容
    contents=contents.decode("utf-8")        # 轉換編碼為 utf-8
    print(contents)
    # 把取得的XML 資料，存在檔案中
    fr = open('109年男性部分時間就業者及受僱者人數.xml', 'w', encoding="utf-8")
    fr.write(contents)
    fr.close()



# 加载XML文件
root = ElementTree.fromstring(contents)
row= root.findall("row")


# 取得Tags
elemList = []
for elem in root.iter():
    elemList.append(elem.tag)

# now I remove duplicities - by convertion to set and back to list
elemList = list(set(elemList))
print(elemList)


# 取得所有資料
agoList=[]
allWorkList=[]
n=0
while n<len(row):
    # XML 解析
    topic= row[n].findall("項目別")
    ago = row[n].findall("細項")
    allWork = row[n].findall("全時工作就業者人數")
    someWork = row[n].findall("部分時間就業者人數")
    allWorkFor = row[n].findall("全時工作受僱者人數")
    someWorkFor = row[n].findall("部分時間受僱者人數")


    str1=" 項目別："+topic[0].text+\
         ",細項:"+ago[0].text +\
         " ,全時工作就業者人數："+allWork[0].text+\
         " ,部分時間就業者人數："+someWork[0].text+\
         " ,全時工作受僱者人數："+allWorkFor[0].text+\
         " ,部分時間受僱者人數："+someWorkFor[0].text

    agoList.append(ago[0].text)
    allWorkList.append(float(allWork[0].text))   # 字串轉浮點數
    print(str1)
    n=n+1





import matplotlib.pyplot as plt # 匯入matplotlib 的pyplot 類別，並設定為plt
from matplotlib.font_manager import FontProperties # 中文字體

# 換成中文的字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）



plt.plot(agoList,allWorkList, "g--",label='新台幣')
plt.legend()         # 自動改變顯示的位置

plt.title("109年男性部分時間就業者及受僱者人數")
plt.ylabel('全時工作就業者') # 顯示Y 座標的文字
plt.xlabel('年齡') # 顯示Y 座標的文字
plt.xticks(rotation=-90,fontsize=6)
plt.show() # 繪製