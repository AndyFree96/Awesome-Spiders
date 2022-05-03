from urllib import response
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import time
import random
import config
import re

baseURL = "https://movie.douban.com/top250"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
            'Cookie': config.Cookie,
}
countryPattern = re.compile(r"制片国家/地区:</span>(.*?)<br/>")
languagePattern = re.compile(r"语言:</span>(.*?)<br/>")
imdbPattern = re.compile(r"IMDb:</span>(.*?)<br>")

infoDictList = []
for i in range(0, 226, 25):
    url = f"{baseURL}?start={i}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    itemList = soup.select(".article .item")
    for item in itemList:
        movieURL = item.select(".pic a")[0].attrs["href"]
        time.sleep(random.choice([3, 2, 1]))
        detailResponse = requests.get(movieURL, headers=headers)
        detailSoup = BeautifulSoup(detailResponse.text, "lxml")

        descriptionElement = item.select("p.quote")
        scripterElement = detailSoup.select("#info > span:nth-child(3) span.attrs")
        actorElement = detailSoup.select("#info > span.actor span.attrs")

        infoDict = {
            "豆瓣地址": movieURL,
            "海报地址": item.select(".pic img")[0].attrs["src"],
            "标题": item.select(".hd a")[0].text.strip(),
            "评分": item.select(".rating_num")[0].text,
            "评价人数": item.select(".star span:last-of-type")[0].text,
            "描述": descriptionElement[0].text.strip() if len(descriptionElement) else "",
            "导演": detailSoup.select("#info > span:nth-child(1) span.attrs")[0].text, 
            "编剧": scripterElement[0].text if len(scripterElement) else "",
            "主演": actorElement[0].text if len(actorElement) else "",
            "片长": detailSoup.select("span[property='v:runtime']")[0].text,
            "类型": "/".join([genre.text for genre in detailSoup.select("span[property='v:genre']")]),
            "上映日期": "/".join([releaseDate.text for releaseDate in detailSoup.select('span[property="v:initialReleaseDate"]')]),
            "制片国家/地区": countryPattern.findall(detailResponse.text)[0],
            "语言": languagePattern.findall(detailResponse.text)[0],
            "imdb": imdbPattern.findall(detailResponse.text)[0],

        }
        infoDictList.append(infoDict)
        pprint(infoDict)

df = pd.DataFrame(infoDictList)
print("Save dataframe to disk.")
df.to_csv("./top250.csv", header=True, index=False)
print("Saved Successful!")