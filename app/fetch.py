import os, sys
import urllib
import re

from urllib.parse import urljoin

import codecs
from datetime import datetime
import argparse
import requests
from bs4 import BeautifulSoup
from pywebcopy import save_webpage

def countLink(soup):
    tags = ['a', 'link']

    info = set()
    for t in tags:
        for x in soup.findAll(t,attrs = {'href' : True}):
            info.add(x['href'])

    return len(info)

def countImg(soup):
    tags=['img','meta']
    formats = ['png']

    info=set()
    for t in tags:
        for x in soup.findAll(t):
            strx = str(x)
            for f in formats:
                findw = '[^ =,\n"]+'+f
                matches = re.findall(findw, strx)
                for m in matches:
                    info.add(m)

    return len(info)

def get_last_fetch(path):
    last_fetch_ts = os.path.getmtime(path)
    dt = datetime.utcfromtimestamp(last_fetch_ts)
    date = datetime.utcfromtimestamp(last_fetch_ts).strftime('%d %Y %H:%M UTC')
    weekday = dt.strftime('%a')
    month = dt.strftime('%b')
    return weekday + ' ' + month + ' ' + date

def resolve_html(path,download_folder_name, url):
    if download_folder_name:
        path = os.path.join(path, download_folder_name, url, url, "index.html")
    else:
        path=path+'/'+url+'.html'

    f = codecs.open(path, 'r', 'utf-8')
    soup = BeautifulSoup(f.read(), "html.parser")
    last_fetch=get_last_fetch(path)


    img_count = countImg(soup)
    link_count=countLink(soup)

    print("site: ",url)
    print("num_links: ",link_count)
    print("images: ",img_count)
    print("last_fetch: ",last_fetch)


def save_page(url, path, filename):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    html_save_path=path+'/'+filename+'.html'
    with open(html_save_path, 'w') as file:
      file.write(soup.prettify())

def download_whole_html(url,path,urlsavename):
    kwargs = {'bypass_robots': True, 'project_name': urlsavename, 'open_in_browser': False}
    save_webpage(url, path, **kwargs)
def check_valid(url):
    if not url.lower().startswith("http"):
        print("url error, please try : python fetch.py https://www.google.com https://stackoverflow.com")
        sys.exit(-1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata', type=str, nargs='+',
                        help='resolve exist html meta data')
    parser.add_argument('--metadata_download', nargs='+',
                        help='resolve exist downloaded whole html meta data')
    parser.add_argument('urls', nargs='*')
    parser.add_argument('--download', type=str, nargs='+',
                        help='download whole page')
    args = parser.parse_args()

    #url='https://autify.com'
    #urls=['https://stackoverflow.com/','https://www.google.com']
    urls=[]

    download_folder_name = 'test'
    path=os.getcwd()

    if not urls:
        if args.download:
            urls=args.download
            path = os.path.join(path, download_folder_name)
            for url in urls:
                check_valid(url)
                download_whole_html(url, path, url.split('//')[1])
        elif args.metadata:
            urls=args.metadata
            for url in urls:
                check_valid(url)
                resolve_html(path, None, url.split('//')[1])
        elif args.metadata_download:
            urls = args.metadata_download

            for url in urls:
                check_valid(url)
                resolve_html(path, download_folder_name, url.split('//')[1])
        else:
            urls=args.urls
            for url in urls:
                check_valid(url)
                save_page(url, path, url.split('//')[1])



    # session = requests.Session()
    # response = session.get('https://www.google.com')
    # url='https://www.google.com'


    #response = urllib.request.urlopen(url)
    #print(response)

    #savePage(response, 'google')

    # from __future__ import division, unicode_literals




