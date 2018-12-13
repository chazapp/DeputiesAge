import re

from bs4 import BeautifulSoup
import sys
import requests
import os
import glob

DownloadDir = "./pages/"

class Deputy:
    def __init__(self, name, link):
        self.Name = name
        self.Link = "https://en.wikipedia.org" + link
        self.Age = 0
        self.PagePath = ""

    def get_deputy_age(self):
        pass

    def __str__(self):
        return "Deputy: " + self.Name + " Link " + self.Link + " Age: " + str(self.Age)

def get_depute_list(soup):
    tables = soup.find_all('table')
    i = 0
    deputelist = []
    for table in tables:
        items = table.find_all('tr')
        for item in items:
            tds = item.findAll('td')
            j = 0
            for td in tds:
                if j == 0:
                     links = td.findAll('a', {"class": "", "title": re.compile(r".*")})
                     for link in links:
                        title = link['title']
                        href = link['href']
                        depute = Deputy(title, href)
                        deputelist.append(depute)
                        j += 1
        i += 1
    return deputelist


def download_deputy_pages(deputies):
    os.mkdir(DownloadDir)
    for deputy in deputies:
        page = requests.get(deputy.Link)
        fd = open(DownloadDir + deputy.Name + ".html", "w+")
        if page.status_code == 200:
            fd.write(str(page.content))
        else:
            print("Wikipedia returned : " + str(page.status_code))
    return


def get_deputy_age(bs):
    bday = bs.findAll("span", {"class": "bday"})[0].string
    year = int(bday[:4])
    return 2018 - year

def get_deputies_ages_from_pages(deputies):
    for deputy in deputies:
        try:
            fd = open(DownloadDir + deputy.Name + ".html")
            htmlFile = fd.read()
            bs = BeautifulSoup(htmlFile, 'html.parser')
            deputy.Age = get_deputy_age(bs)
        except Exception:
            pass
    return deputies


def main():
    if sys.argv[1] is not None:
        print("Opening html document: " + sys.argv[1])
        fd = open(sys.argv[1], 'r', encoding="utf8")
        htmlFile = fd.read()
        bs = BeautifulSoup(htmlFile, 'html.parser')
        deputies = get_depute_list(bs)
        print("There are " + str(len(deputies)) + " deputies")
        if len(sys.argv) > 2 and sys.argv[2] == "--init":
            print("DownloadDeputiesPages")
            download_deputy_pages(deputies)
        print("GetDeputiesAgesFromPages")
        deputies = get_deputies_ages_from_pages(deputies)
        total = 0
        missed = 0
        for deputy in deputies:
            if deputy.Age != 0:
                if deputy.Age < 36:
                    print(deputy.Name)
                    print("Deputy Age: " + str(deputy.Age))
                total += deputy.Age
            else:
                missed += 1
        avg = total / (len(deputies) - missed)
        print("Deputies are " + str(avg) + " year old in average.")
    else:
        print("Usage: python3 ./deputeParser <htmlFile>")


if __name__ == "__main__":
    main()
