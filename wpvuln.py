import urllib3
import requests
import json
import sys
import urllib.request as urllib
import xlrd
import xlwt
from bs4 import BeautifulSoup
urllib3.disable_warnings()
import os
http = urllib3.PoolManager()
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.97 Safari/537.36'
headers = { 'User-Agent' : user_agent }
file = open("vulnurls.txt", "r")
for line in file:
    dir="static/files/"+line[line.find('://www.')+7:line.find('.',line.find('://www.')+7)]
    print(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

    open(dir+"/themes.xls", "w")
    open(dir+"/vulnthemes.xls", "w")
    open(dir+"/plugins.xls", "w")
    open(dir+"/vulnplugins.xls", "w")

    f = open(dir+"/urls.txt", "w")
    f1 = open(dir+"/plugins.txt", "w")
    f2 = open(dir+"/themes.txt", "w")
    loc1 = (dir+"/plugins.xls")
    loc2 = (dir+"/themes.xls")
    loc3 = (dir+"/vulnplugins.xls")
    loc4 = (dir+"/vulnthemes.xls")
    wb1 = xlwt.Workbook()
    sheet1 = wb1.add_sheet("Sheet1",cell_overwrite_ok=True)
    wb2 = xlwt.Workbook()
    sheet2 = wb2.add_sheet("Sheet1",cell_overwrite_ok=True)

    queue = set()
    crawled = list()
    plugins = set()
    themes = set()
    plugins1 = set()
    themes1 = set()
    j=0
    i=0
    l=0
    m=0

    homepage=line[:len(line)-1]#"https://www.pomalyst.com"
    url=homepage
    queue.add(url)
    while 1:
        if l==1:
            for l in crawled:
                if l[-1]!='/':
                    queue.discard(l+'/')
                queue.discard(l)
            if len(queue)==0 or m>5:
                break
        l=1
        m+=1
        url=str(queue.pop())
        print(url)
        f.write(url+"\n")
        crawled.append(url)
        r = http.request('GET', url, headers=headers, redirect=False)
        soup = BeautifulSoup(r.data, "html.parser", from_encoding="iso-8859-1")

        for u in soup.find_all('a'):
            b=str(u.get('href'))
            if "?" in b:
                continue
            elif "&" in b:
                continue
            elif "#" in b:
                continue
            elif ".pdf" in b:
                continue
            elif b=="":
                continue
            elif homepage[8:] in b:
                queue.add(b)
            elif b[0]=='/':
                queue.add(homepage+b)

        for u in soup.find_all('script'):
            b=str(u.get('src'))
            if "wp-content" in b or True:
                if "plugins" in b:
                    plugins.add(b)
                    start = b.find('plugins') + 8
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    plugins1.add(c+"\t"+d)
                    i+=1
                elif "themes" in b:
                    themes.add(b)
                    start = b.find('themes') + 7
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    themes1.add(c+"\t"+d)
                    j+=1

        for u in soup.find_all('link'):
            b=str(u.get('src'))
            if "wp-content" in b or True:
                if "plugins" in b:
                    plugins.add(b)
                    start = b.find('plugins') + 8
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    plugins1.add(c+"\t"+d)
                    i+=1
                elif "themes" in b:
                    themes.add(b)
                    start = b.find('themes') + 7
                    end = b.find('/', start)
                    c=b[start:end]
                    d=str(u.get('ver'))
                    if "ver=" in b:
                        start = b.find('ver=') + 4
                        d=b[start:]
                    themes1.add(c+"\t"+d)
                    j+=1

    for a in range(len(plugins)):
        f1.write(plugins.pop()+"\n")
    for a in range(len(themes)):
        f2.write(themes.pop()+"\n")
    #for a in range(len(crawled)):
    #    f.write(crawled[a]+"\n")
    print(i)
    for x in range(len(plugins1)):
        pl=plugins1.pop()
        print(pl)
        sheet1.write(x,0,pl.split()[0])
        sheet1.write(x,1,pl.split()[1])
        wb1.save(loc1)
    print(j)
    for x in range(len(themes1)):
        th=themes1.pop()
        print(th)
        sheet2.write(x,0,th.split()[0])
        sheet2.write(x,1,th.split()[1])
        wb2.save(loc2)

    wb1 = xlrd.open_workbook(loc1)
    sheet1 = wb1.sheet_by_index(0)
    wb2 = xlrd.open_workbook(loc2)
    sheet2 = wb2.sheet_by_index(0)
    wb3 = xlwt.Workbook()
    sheet3 = wb3.add_sheet("Sheet1",cell_overwrite_ok=True)
    wb4 = xlwt.Workbook()
    sheet4 = wb4.add_sheet("Sheet1",cell_overwrite_ok=True)

    c=0
    sheet3.write(c, 0, "ID")
    sheet3.write(c, 1, "Type")
    sheet3.write(c, 2, "Title")
    sheet3.write(c, 6, "Fixed In")
    sheet3.write(c, 7, "Link")
    wb3.save(loc3)
    ####
    sheet4.write(c, 0, "ID")
    sheet4.write(c, 1, "Type")
    sheet4.write(c, 2, "Title")
    sheet4.write(c, 6, "Fixed In")
    sheet4.write(c, 7, "Link")
    wb4.save(loc4)
    c=1
    l=0
    print("**********")
    for j in range(sheet1.nrows):
        f1=1
        url="https://wpvulndb.com/api/v2/plugins/"+ sheet1.cell_value(j, 0)
        headers = {'User-Agent': 'WPVulnCLI-Client'}
        req = urllib.Request(url, headers=headers)
        req1 = urllib.Request("https://wpvulndb.com/api/v2/plugins/eshop", headers=headers)
        res = json.loads(urllib.urlopen(req1).read().decode('utf-8'))
        try:
            res = json.loads(urllib.urlopen(req).read().decode('utf-8'))
        except IOError:
            f1=0
            print(sheet1.cell_value(j, 0)+"| not found in db")
        if f1==1:
            if not bool(res[next(iter(res.keys()))]["vulnerabilities"]):
                print(sheet1.cell_value(j, 0)+"| mentioned in db")
                continue
            sheet3.write(c, 0, sheet1.cell_value(j, 0))
            sheet3.write(c, 3, "latest version : "+res[next(iter(res.keys()))]["latest_version"])
            c+=1
            for vuln in res[next(iter(res.keys()))]["vulnerabilities"]:
                v=str(vuln)
                u=v[v.find('url')+8:v.find("'",v.find('url')+8)]
                if vuln.get("fixed_in") is None:
                    fixed = "Unfixed"
                    sheet3.write(c, 0, str(vuln.get("id")))
                    sheet3.write(c, 1, vuln.get("vuln_type"))
                    sheet3.write(c, 2, vuln.get("title"))
                    sheet3.write(c, 6, fixed)
                    sheet3.write(c, 7, u)
                    c+=1
                    l=1
                else:
                    fixed = vuln.get("fixed_in")
                if  sheet1.cell_value(j, 1)!= "None":
                    if sheet1.cell_value(j, 1) in vuln.get("title"):
                        sheet3.write(c, 0, str(vuln.get("id")))
                        sheet3.write(c, 1, vuln.get("vuln_type"))
                        sheet3.write(c, 2, vuln.get("title"))
                        sheet3.write(c, 6, fixed)
                        sheet3.write(c, 7, u)
                        c+=1
                        l=1
                else:
                    sheet3.write(c, 0, str(vuln.get("id")))
                    sheet3.write(c, 1, vuln.get("vuln_type"))
                    sheet3.write(c, 2, vuln.get("title"))
                    sheet3.write(c, 6, fixed)
                    sheet3.write(c, 7, u)
                    c+=1
                    l=1
                    #print( str(vuln.get("id")) + " | " + vuln.get("vuln_type") + " | " + vuln.get("title") + " | " +str(vuln.get("fixed_in")) + " | https://wpvulndb.com/vulnerabilities/" + str(vuln.get("id")))
            c+=1
            if l==1:
                print(sheet1.cell_value(j, 0)+"| has vulnerabilities")
            else:
                print(sheet1.cell_value(j, 0)+"| version not found")
    wb3.save(loc3)
    c=1
    l=0
    print("##########")
    for j in range(sheet2.nrows):
        f1=1
        url="https://wpvulndb.com/api/v2/themes/"+ sheet2.cell_value(j, 0)
        headers = {'User-Agent': 'WPVulnCLI-Client'}
        req = urllib.Request(url, headers=headers)
        req1 = urllib.Request("https://wpvulndb.com/api/v2/themes/sydney", headers=headers)
        res = json.loads(urllib.urlopen(req1).read().decode('utf-8'))
        try:
            res = json.loads(urllib.urlopen(req).read().decode('utf-8'))
        except IOError:
            f1=0
            print(sheet2.cell_value(j, 0)+"| not found in db")
        if f1==1:
            if not bool(res[next(iter(res.keys()))]["vulnerabilities"]):
                print(sheet2.cell_value(j, 0)+"| mentioned in db")
                continue
            sheet4.write(c, 0, sheet2.cell_value(j, 0))
            sheet4.write(c, 3, "latest version : "+res[next(iter(res.keys()))]["latest_version"])
            c+=1
            for vuln in res[next(iter(res.keys()))]["vulnerabilities"]:
                v=str(vuln)
                u=v[v.find('url')+8:v.find("'",v.find('url')+8)]
                if vuln.get("fixed_in") is None:
                    fixed = "Unfixed"
                    sheet4.write(c, 0, str(vuln.get("id")))
                    sheet4.write(c, 1, vuln.get("vuln_type"))
                    sheet4.write(c, 2, vuln.get("title"))
                    sheet4.write(c, 6, fixed)
                    sheet4.write(c, 7, u)
                    c+=1
                    l=1
                else:
                    fixed = vuln.get("fixed_in")
                if  sheet2.cell_value(j, 1)!= "None":
                    if sheet2.cell_value(j, 1) in vuln.get("title"):
                        sheet4.write(c, 0, str(vuln.get("id")))
                        sheet4.write(c, 1, vuln.get("vuln_type"))
                        sheet4.write(c, 2, vuln.get("title"))
                        sheet4.write(c, 6, fixed)
                        sheet4.write(c, 7, u)
                        c+=1
                        l=1
                else:
                    sheet4.write(c, 0, str(vuln.get("id")))
                    sheet4.write(c, 1, vuln.get("vuln_type"))
                    sheet4.write(c, 2, vuln.get("title"))
                    sheet4.write(c, 6, fixed)
                    sheet4.write(c, 7, u)
                    c+=1
                    l=1
                wb4.save(loc4)
                #print( str(vuln.get("id")) + " | " + vuln.get("vuln_type") + " | " + vuln.get("title") + " | " +str(vuln.get("fixed_in")) + " | https://wpvulndb.com/vulnerabilities/" + str(vuln.get("id")))
            c+=1
            if l==1:
                print(sheet2.cell_value(j, 0)+"| has vulnerabilities")
            else:
                print(sheet2.cell_value(j, 0)+"| version not found")
    wb4.save(loc4)
