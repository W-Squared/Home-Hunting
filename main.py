import requests
import csv
from bs4 import BeautifulSoup

housesList = list()
house = {}
scrapeURL = "https://www.zillow.com/homes/for_sale/Tacoma,-WA_rb/"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language":"en-US,en;q=0.9",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding":"gzip, deflate, br",
    "upgrade-insecure-requests":"1"
}

response = requests.get(scrapeURL, headers=headers).text
soup = BeautifulSoup(response,"html.parser")
properties = soup.find_all("div",{"class":"StyledCard-c11n-8-84-3__sc-rmiu6p-0 jZuLiI StyledPropertyCardBody-c11n-8-84-3__sc-1p5uux3-0 gHYrNO"})
csvFile = "test.csv"

for page in range(1,100):
    for i in soup.find_all('a', href = True):
        if("https://www.zillow.com/homedetails/" in i['href']):
            nextPage = requests.get(i['href'], headers=headers)
            nextSoup = BeautifulSoup(nextPage.content, 'html.parser')
            print("Next URL Title : ",nextSoup.find('title').string)
    for x in range(len(properties)):
        try:
            house["Pricing"]=properties[x].find("div",{"class":"PropertyCardWrapper__StyledPriceGridContainer-srp__sc-16e8gqd-0 kSsByo"}).text
        except:
            house["Pricing"]=None
        try:
            house["Size"]=properties[x].find("div",{"class":"StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 dbDWjx"}).text
        except:
            house["Size"]=None
        try:
            house["Address"]=properties[x].find("a",{"class":"StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link"}).text
        except:
            house["Address"]=None
        house={}
        housesList.append(house)


columnHeaders = list(housesList[0].keys())
file =  open(csvFile, 'w', newline='')
writer = csv.DictWriter(file, fieldnames=columnHeaders)

# Write the header row
writer.writeheader()

# Write data rows
for potentialHouse in housesList:
    writer.writerow(potentialHouse)
    