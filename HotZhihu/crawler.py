from wsgiref import headers
import requests
from bs4 import BeautifulSoup
import config
from pprint import pprint


URL = "https://www.zhihu.com/hot"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'Cookie': config.Cookie
           }

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "lxml")
itemList = soup.select("section.HotItem")
for item in itemList:
    infoDict = {
        "序号": item.select(".HotItem-index")[0].text,
        "标题": item.select(".HotItem-content .HotItem-title")[0].text,
        "链接地址": item.select(".HotItem-content a")[0].attrs["href"],
        "热度": item.find("div", class_="HotItem-metrics").text[:-3],
    }
    pprint(infoDict)