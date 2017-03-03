from Data import *
import aiohttp
import asyncio
from aiohttp import ClientSession
from urllib.parse import urljoin, urldefrag, urlsplit, urlparse
from bs4 import BeautifulSoup
import sqlite3
import time
from Data import *

# Settings so that it's possible to pause & resume crawls. 3 Crawl modes, list, crawl, web

Project = 'sdsds'
Threads = 100
crawl_type = 'crawl'
domains = set()
queue = []
root_url = "http://www.zoopla.co.uk/"
list_file = 'list.txt'
queue.append(root_url)
crawled_urls, url_hub = [], [root_url]
now = time.strftime('%Y-%m-%d %H:%M')
db = sqlite3.connect('{}{}'.format(Project,'.db'))
cursor = db.cursor()
create_tables(db, cursor)
into_campaigns(Project,now,cursor,db)

def resume():
    c = cursor.execute('SELECT DOMAIN FROM DOMAINS WHERE ID = "{c}"'.format(c=Project))
    list = c.fetchall()
    list = [x[0] for x in list]
    [domains.add(i) for i in list]

    d = cursor.execute('SELECT URL FROM QUEUE WHERE id = "{c}"'.format(c=Project))
    list1 = d.fetchall()
    list1 = [x[0] for x in list1]
    [queue.append(i) for i in list1]

resume()
print(len(queue))
if len(queue) == 1:
    finder = load_queue(root_url,crawl_type)
    [queue.append(i) for i in finder.page_links()]

def get_urls(html):
    new_urls = [url.split('"')[0] for url in str(html).replace("'",'"').split('href="')[1:]]
    return [urljoin(root_url, remove_fragment(new_url)) for new_url in new_urls]

async def get_body(url):
    async with ClientSession() as session:
        async with session.get(url, timeout=30) as response:
            response = await response.read()
            #print(response)
            return response

async def handle_task(task_id, work_queue,Project):
    while not work_queue.empty():
        queue_url = await work_queue.get()
        print('Now crawling ' + queue_url + " | there are "+ str(len(queue)) + " links in queue")
        crawled_urls.append(queue_url)
        try:
            body = await get_body(queue_url)
            data = bloggers(queue_url, body, Project,cursor,db)
            for new_url in get_urls(body):
                domain = "{0.scheme}://{0.netloc}/".format(urlsplit(new_url))
                if new_url in crawled_urls:
                    pass
                elif new_url in queue:
                    pass
                elif domain == root_url and crawl_type == 'crawl':
                    now = time.strftime('%Y-%m-%d %H:%M')
                    into_queue(Project, new_url, now, cursor, db)
                    queue.append(new_url)
                    q.put_nowait(new_url)
                elif domain not in domains and crawl_type == 'web':
                    now = time.strftime('%Y-%m-%d %H:%M')
                    into_queue(Project, new_url, now,cursor,db)
                    queue.append(new_url)
                    q.put_nowait(new_url)

            now = time.strftime('%Y-%m-%d %H:%M')
            domain = "{0.scheme}://{0.netloc}/".format(urlsplit(queue_url))
            domains.add(domain)
            if domain not in domains:
                into_domains(Project, domain, now, cursor, db)
        except Exception as e:
            pass
            print(e)

def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url

if __name__ == "__main__":
    q = asyncio.Queue()
    #print('working')
    [q.put_nowait(url) for url in queue]
    loop = asyncio.get_event_loop()
    tasks = [handle_task(task_id, q,Project) for task_id in range(Threads)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
