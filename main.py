import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"
request = requests.get(alba_url)

soup = BeautifulSoup(request.text, "html.parser")
MainSuperBrand = soup.find("div", attrs={"id":"MainSuperBrand"})
goodsBox = MainSuperBrand.find("ul", attrs={"class":"goodsBox"})
goodsBox_info = goodsBox.find_all("a", attrs={"class":"goodsBox-info"})

companyList = []
for i in range(0,len(goodsBox_info)):
  name = goodsBox_info[i].find("span", attrs={"class":"company"}).text
  url = goodsBox_info[i].get("href")
  # 일반채용정보가 없는 url 제외, 특수 url 제외
  if url[-11:] == "alba.co.kr/":
    url = url + "job/brand/"
    companyList.append([name, url])

def saveToCsv(name, articles):
  try:
    with open("./jobs/"+name+".csv", 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(articles)
  except:
    print(f"{name} -> create csv file failed")

def getArticles(name, url):
  articles = [["local ", "title ", "workTime ", "pay ", "writeDate"]]
  request = requests.get(url)
  soup = BeautifulSoup(request.text, "html.parser")

  jobCount = soup.find("p", attrs={"class":"jobCount"}).text
  jobCount = jobCount[:-1]
  jobCount = jobCount.replace(",","")
  # url은 있지만 채용 게시글이 없으면 예외
  # jobCount, pagesize를 이용해 페지네이션 없이 한번에 크롤
  if int(jobCount) > 0:
    url = url + "?pagesize=" + jobCount
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    NormalInfo = soup.find("div", attrs={"id":"NormalInfo"})
    tbody = NormalInfo.find("tbody")    
    tr = tbody.find_all("tr")

    print(f"\n\n====== {name} / ({jobCount}) ======")
    for i in range(0,len(tr)):
      try:
        local = tr[i].find("td", attrs={"class":"local first"}).text
        title = tr[i].find("span", attrs={"class":"company"}).text
        workTime = tr[i].find("td", attrs={"class":"data"}).text
        pay = tr[i].find("td", attrs={"class":"pay"}).text
        writeDate = tr[i].find("td", attrs={"class":"regDate last"}).text
        print(local, title, workTime, pay, writeDate)
        articles.append([local, title, workTime, pay, writeDate])
      except:
        pass

    saveToCsv(name, articles)
    print("Save Complete")

for i in range(0,len(companyList)):
  getArticles(companyList[i][0],companyList[i][1])

print("All Done !")