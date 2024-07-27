
import requests
from bs4 import BeautifulSoup
import time 
import pandas as pd
from colorama import init, Fore, Style


def linkScraper():
    business = input("Enter Search Keyword: ")
    location = input("Enter Search Location: ")
    url = "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}".format(business,location)
    r = requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.content,"html.parser")
    dataContainer = soup.find_all("div",{"class":'srp-listing'})
    pagination_number = soup.find("div",{'class':'pagination'}).find("span",{"class":'showing-count'}).text.split(" of ")[1].replace("More info","")
    pageCount = 3 #round(int(pagination_number) / 30)
    print(pageCount)
    for page in range(1,pageCount+1):
        print("Running Page {}".format(page))
        url = 'https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}'.format(business,location,page)
        r = requests.get(url)
        if r.status_code != 200:
            url = 'scraperapi.com/?api_key=3263989e407c6303bde15458736c006c&url=https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}'.format(business,location,page)
            r = requests.get(url)
            
        soup = BeautifulSoup(r.content,"html.parser")
        dataContainer = soup.find_all("div",{"class":'srp-listing'})
        for data in dataContainer:
            try:
                name = data.find("div",{"class":'info'}).find('a',{"class":'business-name'}).find("span").text
                print(name)
            except:
                name = ""
            try:
                link = "https://www.yellowpages.com"+data.find("div",{"class":'info'}).find('a',{"class":'business-name'}).get('href')
            except:
                link = ""     
            try:    
                phone  = data.find("div",{'class':'info-section info-secondary'}).find("div",{'class':'phones phone primary'}).text
            except:
                phone= ""
            try:    
                addresses = data.find("div",{'class':'adr'})
            except:
                addresses= ""
            try:    
                streetAddress = addresses.find("div",{'class':'street-address'}).text
            except:
                streetAddress= ""
            try:    
                locality = addresses.find("div",{'class':'locality'}).text
            except:
                locality = ""
            
            dataDict = {
                "Name":name,
                "Phone": phone,
                "Street Address":streetAddress,
                "Locality":locality,
                "Input Address":location,
                "Url":link
            }
            if dataDict not in dataList:
                dataList.append(dataDict)
                pd.DataFrame(dataList).to_csv("Links.csv",index=False)
    # print("----------------Wait For Email Scraper---------------")
    print(Fore.RED + Style.BRIGHT + "----------------Wait For Email Scraper---------------")

    dataScraper()

def dataScraper():
    df = pd.read_csv("Links.csv")
    links = df["Url"].values.tolist()
    names = df["Name"].values.tolist()
    phones = df["Phone"].values.tolist()
    street = df["Street Address"].values.tolist()
    local = df["Locality"].values.tolist()
    inputs = df["Input Address"].values.tolist()
    allData = []
    
    for url in range(len(links)):
        r = requests.get(links[url])
        if r.status_code!=200:
            r = requests.get("http://api.scraperapi.com/?api_key={}&".format(_key)+links[url])
        
        soup = BeautifulSoup(r.content,"html.parser")
        try:
            email = soup.find("a",{'class':'email-business'}).get('href').replace("mailto:","")
        except:
            email = "" 

        name = names[url]    
        print(name)
        phone = phones[url]
        streetAddress = street[url]
        input_key = inputs[url]
        locality = local[url]

        dataDict = {
            "Name":name,
            "Phone": phone,
            "Email":email,
            "Street Address":streetAddress,
            "Locality":locality,
            "Input Address":input_key,
        }
        if dataDict not in allData:
            allData.append(dataDict)
            pd.DataFrame(allData).to_csv("Data/Data.csv",index=False)

        

if __name__=="__main__":
    
    dataList = []
    linkScraper()
    # dataScraper()
    _key = "3263989e407c6303bde15458736c006c"

