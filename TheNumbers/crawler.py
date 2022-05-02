from urllib import response
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint

baseURL = "https://www.the-numbers.com/movie/budgets/all"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
           }

infoDictList = []
for i in range(1, 6202, 100):
    url = f"{baseURL}/{i}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    itemList = soup.select("#main tr + tr")
    for item in itemList:
        releaseDateElement = item.select("tr >td:nth-child(2) a")[0]
        infoDict = {
            "release_date": "Unknown" if releaseDateElement.text == "Unknown" else "/".join(releaseDateElement.attrs["href"].split("/")[-3:]), # Unknown
            "movie": item.select("tr >td:nth-child(3) a")[0].text,
            "production_budget": item.select("tr >td:nth-child(4)")[0].text.strip(),
            "domestic_gross": item.select("tr >td:nth-child(5)")[0].text.strip(),
            "worldwide_gross": item.select("tr >td:nth-child(6)")[0].text.strip(),
        }
        infoDictList.append(infoDict)
        pprint.pprint(infoDict)

df = pd.DataFrame(infoDictList)
print("Save dataframe to disk.")
df.to_csv("./movies.csv", header=True, index=False)
print("Saved Successful!")