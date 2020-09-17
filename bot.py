from bs4 import BeautifulSoup
import urllib.request as urllib
ipltablepage = "https://www.iplt20.com/points-table/2020"
ipltableData = urllib.urlopen(ipltablepage)
soup = BeautifulSoup(ipltableData, 'html.parser')
iplTable = soup.find('table', attrs={'class':'standings-table'})
#print(iplTable.prettify())
iplTableByPos = iplTable.find_all('tr')
print(iplTableByPos[1].find_all('td')[0].contents)


