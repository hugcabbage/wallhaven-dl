########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  Dated- 26 June 2016                 #
#                 Update - 11 June 2019                #
########################################################

import os
import getpass
import re
import requests
import tqdm
import time
import urllib
import json

os.makedirs('Wallhaven', exist_ok=True)
BASEURL=''
cookies=dict()
pgstart=0

def category():
    global BASEURL
    print('''
    ****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ').lower()
    ctags = {'all':'111', 'anime':'010', 'general':'100', 'people':'001', 'ga':'110', 'gp':'101' }
    ctag = ctags[ccode]

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw':'100', 'sketchy':'010', 'nsfw':'001', 'ws':'110', 'wn':'101', 'sn':'011', 'all':'111'}
    ptag = ptags[pcode]

    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + "&categories=" +\
        ctag + '&purity=' + ptag + '&page='

def toplist():
    global BASEURL
    print('Downloading toplist')
    topListRange = '1M'
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&topRange=' +\
        topListRange + '&sorting=toplist&page='
    
def latest():
    global BASEURL
    print('Downloading latest')
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY +\
        '&sorting=date_added&page='

def hot():
    global BASEURL
    print('Downloading hot')
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY +\
        '&sorting=hot&page='
    
def random():
    global BASEURL
    print('Downloading random')
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY +\
        '&sorting=random&page='

def search():
    global BASEURL
    query = input('Enter search query: ')
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&q=' +\
        urllib.parse.quote_plus(query) + '&page='

def link():
    global BASEURL, pgstart
    link = input('Enter link(must contain \'search\'): ')
    if 'search?' not in link:
        print('link error')
    else:
        if '&page=' in link:
            pgstart = int(link.split('&page=')[1])
        link_body = '&' + link.split('search?')[1].split('&page=')[0]
        BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY +\
            link_body + '&page='

def downloadPage(pageId, totalImage):
    url = BASEURL + str(pageId)
    urlreq = requests.get(url, cookies=cookies)
    pagesImages = json.loads(urlreq.content);
    pageData = pagesImages["data"]

    for i in range(len(pageData)):
        currentImage = (((pageId - 1) * 24) + (i + 1))

        url = pageData[i]["path"]
        
        filename = os.path.basename(url)
        osPath = os.path.join('Wallhaven', filename)
        if not os.path.exists(osPath):
            imgreq = requests.get(url, cookies=cookies)
            if imgreq.status_code == 200:
                print("Downloading : %s - %s / %s" % (filename, currentImage , totalImage))
                with open(osPath, 'ab') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)
            elif (imgreq.status_code != 403 and imgreq.status_code != 404):
                print("Unable to download %s - %s / %s" % (filename, currentImage , totalImage))
        else:
            print("%s already exist - %s / %s" % (filename, currentImage , totalImage))

def main():
    global pgstart
    Choice = input('''Choose how you want to download the image:

    Enter "category" for downloading wallpapers from specified categories
    Enter "toplist" for downloading toplist wallpapers
    Enter "latest" for downloading toplist wallpapers
    Enter "hot" for downloading toplist wallpapers
    Enter "random" for downloading toplist wallpapers
    Enter "search" for downloading wallpapers from search
    Enter "link" for downloading wallpapers from search

    Enter choice: ''').lower()
    while Choice not in ['category', 'toplist', 'latest', 'hot', 'random', 'search', 'link']:
        if Choice != None:
            print('You entered an incorrect value.')
        choice = input('Enter choice: ')

    if Choice == 'category':
        category()
    elif Choice == 'toplist':
        toplist()
    elif Choice == 'latest':
        latest()
    elif Choice == 'hot':
        hot()
    elif Choice == 'random':
        random()
    elif Choice == 'search':
        search()
    elif Choice == 'link':
        link()

    if pgstart == 0:
        pgstart = int(input('Which page you want to start downloading from: '))
    pgnumber = int(input('How many pages you want to download: '))
    totalImageToDownload = str(24 * pgnumber)
    print('Number of Wallpapers to Download: ' + totalImageToDownload)
    for j in range(pgstart, pgstart + pgnumber):
        downloadPage(j, totalImageToDownload)

if __name__ == '__main__':
    with open('api_key.txt', encoding='utf-8') as f:
        APIKEY = f.read().strip()
    main()
