from bs4 import BeautifulSoup
import requests
import time
import re
from urllib.parse import urlsplit, urlparse

class load_queue():
    def __init__(self, root_url,crawl_type):
        self.links = set()
        r = requests.get(root_url,timeout=10)
        base_url = r.url
        try:
            soup = BeautifulSoup(r.text,'lxml')
        except:
            soup = BeautifulSoup(r.text,'html.parser')

        links = soup.find_all('a',href=True)
        for link in links:
            try:
                if link.startswith('/'):
                    link = ''.format('{}://{}{}'.format(base_url.scheme, base_url.netloc, link))
                if not link.startswith('http'):
                    pass
                else:
                    if crawl_type == 'crawl':
                        if urlparse(link).netloc == base_url.netloc:
                            self.links.add(link)
                    else:
                        self.links.add(link)
            except:
                continue

    def page_links(self):
        return self.links

class bloggers():

    def __init__(self, url, body, Project,cursor,db):

        try:
            soup = BeautifulSoup(body,'lxml')
        except:
            soup = BeautifulSoup(body,'html.parser')

        self.url = url
        self.project = Project
        try:
            gen = soup.find('meta', attrs={'name': 'generator'})
            type1 = 'none'
            if gen['content'] is not None:
                type1 = gen['content']
            self.now = time.strftime('%Y-%m-%d %H:%M')
            # cursor.execute('''INSERT INTO results(id,url,type,time)
            #                   VALUES(?,?,?,?)''', (Project, url, type1, self.now))
            # db.commit()
        except:
            type1 = 'None'
            self.now = time.strftime('%Y-%m-%d %H:%M')
            # cursor.execute('''INSERT INTO results(id,url,type,time)
            #                           VALUES(?,?,?,?)''', (Project, url, type1, self.now))
            # db.commit()
        try:
            meta_title = soup.title.text
            title_length = len(meta_title)
        except:
            meta_title = 'N/A'
            title_length = 'N/A'
        try:
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description['content']
            meta_description_length = len(meta_description)
        except:
            meta_description = 'N/A'
            meta_description_length = 'N/A'
        try:
            response_header = response_header
        except:
            response_header = 'N/A'
        try:
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            canonical_count = len(soup.findAll('link', attrs={'rel': 'canonical'}))
            canonical = canonical['href']
            canonical_count = canonical_count
        except:
            canonical = 'N/A'
            canonical_count = 0
        try:
            robots = soup.find('meta', attrs={'name': 'robots'})
            robots = robots['content']
        except:
            robots = 'N/A'

        cursor.execute('''INSERT INTO results(id,url,meta_title,title_length,meta_description,description_length,
        response_header,canonical,canonical_count,robots,type,time)
                                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''', (Project,url,meta_title,
        title_length,meta_description,meta_description_length,response_header,canonical,canonical_count,robots,type1,self.now))
        db.commit()


class link_finder():

    def __init__(self, url,response):
        self.url = url
        self.html = html
        self.links = set()

        base_url = urlparse(url)

        try:
            soup = BeautifulSoup(response, 'lxml')
        except:
            soup = BeautifulSoup(response,'html.parser')

        links = soup.find_all('a',href=True)

        for link in links:
            try:
                if link.startswith('/'):
                    link = ''.format('{}://{}{}'.format(base_url.scheme, base_url.netloc, link))
                if not link.startswith('http'):
                    pass
                else:
                    self.links.add(link)
            except:
                continue

    def page_links(self):
        return self.links


def create_tables(db, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns(id TEXT,
                           project TEXT, time DATETIME)''')
    db.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results(id TEXT,url TEXT,meta_title TEXT,title_length INT,meta_description TEXT,description_length TEXT,
        response_header TEXT,canonical TEXT,canonical_count INT,robots TEXT,type TEXT,time DATETIME)''')
    db.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internal_links(id TEXT, source TEXT,
                           destination TEXT)''')
    db.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains(id TEXT,
                           domain TEXT, time DATETIME)''')
    db.commit()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS queue(id TEXT,
                               url TEXT, time DATETIME)''')
    db.commit()

def into_queue(Project, new_url, now,cursor,db):
    cursor.execute('''INSERT INTO queue(id,url,time)
                                   VALUES(?,?,?)''', (Project, new_url, now))
    db.commit()

def into_domains(Project,domain, now,cursor,db):
    cursor.execute('''INSERT INTO domains(id,domain,time)
                                                          VALUES(?,?,?)''', (Project, domain, now))
    db.commit()

def into_campaigns(Project, now,cursor,db):
    cursor.execute('''INSERT INTO campaigns(id,project,time)
                              VALUES(?,?,?)''', (Project, Project, now))
    db.commit()
