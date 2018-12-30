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

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Index")
sheet1.write(0, 1, "Company Details")
sheet1.write(0, 2, "Address")
sheet1.write(0, 3, "Website")

#To calculate number of pages-

mainPageLink = "https://www.fundoodata.com/search_results.php?city_id=-1&industry_id=-1&search_type=1&43430&startW=Z&pageno=5&tot_rows=454&total_results=454&no_of_offices=0"   #Change this link to whichever city is required.
page=urllib.request.urlopen(mainPageLink).read()
soup = BeautifulSoup(page, "html.parser")
resultQuantity= soup.find("div", {"class":"search-page-paid-pannel"}).find("table", {"class":"title"}).find("span").text.split(" ").reverse()[0]
print(resultQuantity);
# totalPages = math.ceil((int(resultQuantity[len(resultQuantity)-1])) /21)
totalPages=math.ceil(resultQuantity/20)

print(totalPages)

#Starting scraping
lineNumber=1
pageNumber=5
# mainPageLink = mainPageLink + "?&pageno="
#main-container > div.main-container-up.inner-pages > div.search-page-full-pannel > div.search-page-paid-pannel > form > div:nth-child(1) > div > ul > li:nth-child(7) > a
nextPage='start'
while(pageNumber<=totalPages):
    wiki = mainPageLink + str(pageNumber)
    page=urllib.request.urlopen(wiki).read()
    soup = BeautifulSoup(page, "html.parser")
    nextPage=soup.find("div", {"class":"search-page-paid-pannel"}).find("ul").find("li").reverse()[0].find("a", href=True)['href']
    prettysoup=soup.find("div", {"class":"search-page-paid-pannel"}).find("table")
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

filename=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')+'.xls'
book.save("C:/Users/MUJ/Desktop/Dhanbad.xls")   #Specify the full path of the location where the xls file is to be created, along with the name for the xls file.


