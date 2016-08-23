from bs4 import BeautifulSoup
from urllib import urlopen
import re
from graph import Graph
import pickle
from sendmail import send_mail


def getlinks(sublink, deepth=1):
    try:
        graph_file = open('wiki' + sublink[5:] + '.pickle', 'r')
        page_list = []
        graph = Graph(pickle.load(graph_file).get_neighbour())
        for v in graph.vertices():
            if graph.get_degree(v)['out'] == 0:
                page_list.append((v, deepth))
        send_mail('506759765@qq.com', 'Task: scrapying ' + sublink + ' continuing', 'with deepth:' + str(deepth))
    except:
        # None exist
        page_list = [(sublink, deepth)]
        graph = Graph()
        send_mail('506759765@qq.com', 'Task: scrapying ' + sublink + ' started', 'deepth:' + str(deepth))

    # while page_list is not empty
    while page_list:
        page = tuple(page_list.pop())
        (page,page_deepth) = page

        # if reach max deepth, ignore it
        if page_deepth is 0:
            continue

        req = urlopen(wikiurl+page)
        content = req.read()
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
                page_list.append((page,page_deepth-1))
            graph.add_edge([parent_page, page])
    graph_file = open('wiki'+sublink[5:]+'.pickle','wb')
    pickle.dump(graph,graph_file,2)
    graph_file.close()
    v_num = len(graph.vertices())
    send_mail('506759765@qq.com','The scrapy for '+sublink+' is done!',str(v_num)+' vertices was reached!\n')

wikiurl = "http://en.wikipedia.org"
print wikiurl
getlinks('')


