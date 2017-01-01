from bs4 import BeautifulSoup
from urllib import urlopen
import re
from graph import Graph
import pickle
from sendmail import send_mail
from collections import deque
from decorators import *


@randomize
def random_urlopen(url):
    req = urlopen(url)
    return req.read()


def getlinks(sublink, depth=1):
    try:
        graph_file = open('wiki' + sublink[5:] + '.pickle', 'r')
        page_list = deque()
        graph = Graph(pickle.load(graph_file).get_neighbour())
        for v in graph.vertices():
            if graph.get_degree(v)['out'] == 0:
                page_list.append((v, depth))
        try:
            send_mail('506759765@qq.com',
                      'Task: scrapying ' + sublink + ' continuing',
                      'with deepth:' + str(depth))
        except:
            print "email is not sent"

    except:
        # None exist
        page_list = deque([(sublink, depth)])
        graph = Graph()
        try:
            send_mail('506759765@qq.com',
                      'Task: scrapying ' + sublink + ' started',
                      'deepth:' + str(depth))
        except:
            print "email is not sent"

    # while page_list is not empty
    while page_list:
        page = tuple(page_list.popleft())
        (page, page_depth) = page

        # if reach max deepth, ignore it
        if page_depth > 0:
            content = random_urlopen(page)
            parent_page = page

            # use lxml first
            try:
                soup = BeautifulSoup(content,'lxml')
            except:
                soup = BeautifulSoup(content)

            links = soup.findAll("a",{'href':re.compile('^(/wiki/)[^:]*?$')})
            for link in links:
                page = link.attrs['href']
                if page not in graph.vertices():
                    print '->'+page
                    page_list.appendleft((page,page_depth - 1))
                graph.add_edge([parent_page, page])

    graph_file = open('wiki'+sublink[5:]+'.pickle','wb')
    pickle.dump(graph,graph_file,2)
    graph_file.close()
    v_num = len(graph.vertices())
    try:
        send_mail('506759765@qq.com',
                  'The scrapy for '+sublink+' is done!',
                  str(v_num)+' vertices was reached!\n')
    except:
        print 'email is not sent'

wikiurl = "http://en.wikipedia.org"
print wikiurl
getlinks('', depth=5)


