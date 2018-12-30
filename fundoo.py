#Scrapes data from Fundoodata
#This will scrape data from all pages of results on Fundoodata for the city given.
#It takes about 1-2 minutes per page, may vary, so plan accordingly.

#Only two parameters need to be changed to get data for different city. 1) The "mainPageLink" variable.  2)The last line of code in this file.

#BeatifulSoup4 needs to be installed on the system running this script. Go to the Python directory, open command prompt or bash there and execute-
# pip install beautifulsoup4


from bs4 import BeautifulSoup
import urllib.request
import xlwt
import math
import time
import datetime

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Index")
sheet1.write(0, 1, "Company Name")
sheet1.write(0, 2, "Industry")
sheet1.write(0, 3, "Sub Industry")
sheet1.write(0, 4, "Company Type")
sheet1.write(0, 5, "Level Of Office")
sheet1.write(0, 6, "Location")
sheet1.write(0, 7, "Phone Number")
sheet1.write(0, 8, "Website")

#To calculate number of pages-

mainPageLink = "https://www.fundoodata.com/companies-in/dhanbad-l28"   #Change this link to whichever city is required.
page=urllib.request.urlopen(mainPageLink).read()
soup = BeautifulSoup(page, "html.parser")
resultQuantity= soup.find("div", {"class":"search-page-right-pannel"}).find("div", {"class":"title"}).find("span").text.split(" ")
totalPages = math.ceil((int(resultQuantity[len(resultQuantity)-1])) /21)

print(totalPages)

#Starting scraping
lineNumber=1
pageNumber=1
mainPageLink = mainPageLink + "?&pageno="
while(pageNumber<=totalPages):
    wiki = mainPageLink + str(pageNumber)
    page=urllib.request.urlopen(wiki).read()
    soup = BeautifulSoup(page, "html.parser")
    prettysoup=soup.findAll("div",{"class": "search-result-left"})
    for x in prettysoup:
        sheet1.write(lineNumber, 0, lineNumber)
        heading = x.find("div", {"class":"heading"})
        if heading:
            sheet1.write(lineNumber, 1, heading.text)
        everyColumn= x.findAll("td", {"class":""})
        i=0
        while i < len(everyColumn):
            if(everyColumn[i].text.split(None, 1)[0] == "Industry"):
                sheet1.write(lineNumber, 2, everyColumn[i+1].text[3:])
                i=i+2
            elif(everyColumn[i].text.split(None, 1)[0] == "Sub"):
                sheet1.write(lineNumber, 3, everyColumn[i+1].text[3:])
                i=i+2
            elif(everyColumn[i].text.split(None, 1)[0] == "Company"):
                sheet1.write(lineNumber, 4, everyColumn[i+1].text[3:])
                i=i+2
            elif(everyColumn[i].text.split(None, 1)[0] == "Level"):
                sheet1.write(lineNumber, 5, everyColumn[i+1].text[2:])
                i=i+2
            elif(everyColumn[i].text.split(None, 1)[0] == "Location"):
                sheet1.write(lineNumber, 6, everyColumn[i+1].text[2:])
                i=i+2
        for link in x.findAll('a', href=True):
            print(link)
            secPage=link['href']
            page2=urllib.request.urlopen(secPage).read()
            soup2=BeautifulSoup(page2, "html.parser")
            try:
                link=soup2.find("div", {"class":"search-page-right-pannel"}).findAll("div", {"class":"detail-line"})
                for l in link:
                    phone= l.text.partition("\n")[0]
                    sheet1.write(lineNumber, 7, phone)
                    sheet1.write(lineNumber, 8, str(l.text)[len(phone):])
            except:
                print (secPage, " has no details of Phone and Website")
        lineNumber = lineNumber+1
    print("PAGE NUMBER: ", pageNumber, " DONE!")
    pageNumber = pageNumber + 1

print("COMPLETE!")

filename=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')+'.xls'
book.save(filename)   #Specify the full path of the location where the xls file is to be created, along with the name for the xls file.


