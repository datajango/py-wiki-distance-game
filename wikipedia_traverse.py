import bs4
import requests
import argparse
import re
import urllib.parse
import wikipedia
import os
import sys
import pickle
from collections import defaultdict
from collections import deque

 # This function is a kinder-gentler Wiki Media API fetch because is uses a page cache.
def fetch(topic, debugging):
    filename = os.path.join('cache', topic + ".obj")

    if os.path.exists(filename):
        # using cache wikipedia
        if debugging:
            print('using cache for "%s"' % (topic))
        page = pickle.load(open(filename, "rb"))
        return page
    else:
        # hitting wikipedia
        if debugging:
            print('hitting wikipedia for "%s"' % (topic))
        try:
            page = wikipedia.page(topic)
            pickle.dump(page, open(filename, "wb"))
            return page
        except:
            print('Wiki Fetch Error!')
            return None


class WikiTopicGraph():
    def __init__(self):
        self.graph = defaultdict(list)

    # add_edge - add a link to a topic
    def add_edge(self, topic, link):
        self.graph[topic].append(link)

    def add_topics(self, wiki_page):
        for link in wiki_page.links:
            self.add_edge(wiki_page.title, link)

    # check all links to see if the target is in the links for the topic
    def check_topic_links_for_target(self, topic, target):
        if topic in self.graph:
            for link in self.graph[topic]:
                if link.lower() == target.lower():
                    return True
            return False
        else:
            return False  # topic isn't even in the Graph

    # debug print the graph
    def dump(self):
        for topic in self.graph.keys():
            print(topic)


#graph = WikiTopicGraph()
class Topic():
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.children = {}
        self.parents = {}
        self.visited = False

    def add_child(self, title):
        if title not in self.children:
            self.children[title] = Topic(title)

    def add_parent(self, title):
        if title not in self.parents:
            self.parents[title] = Topic(title)

    def add_children(self, page):
      max = 3

      if page and page.links:
          for index, title in enumerate(page.links):
              self.add_child(title)
              if len(self.children) == 3:
                  break

    def visit(self):
        if not self.visited:
            self.visited = True
            page = fetch(self.title, False)
            self.add_children(page)
            
            #for index, child in enumerate(self.children):
            #    print("%d %s"%(index, child))

class Crawler():
    def __init__(self, debugging):
        self.debugging = debugging
        if not os.path.exists('cache'):
            os.makedirs('cache')
        self.topics = {}  # store all topics pages
        self.max_depth = 3
        self.current_depth = 0
        self.queue = deque([])
        self.visited_list = []
        self.stack = []
        

    def bfs_crawl(self, title):

        #self.stack.append(title)
        #print('bfs_crawl: "%s"'%(title))

        #print('bfs_crawl:', title, '->'.join(self.stack))
        #print('bfs_crawl: "%s"'%('->'.join(self.stack)))

        self.visited_list.append(title)
        #if len(queue) > 99:
        #  return
        #self.topics[title] = Topic(title)
        #self.topics[title].visit()

        topic = Topic(title)
        topic.visit()
 
        for index, child_topic in enumerate(topic.children):
            #print("\t%s %d %s"%(title, index, child_topic))
            
            flag = 0
            
            # Check if the URL already exists in the queue
            for j in self.queue:
                if j['child'] == child_topic:
                    flag = 1
                    break

            # If not found in queue
            if flag == 0:
                #if len(self.queue) > 99:
                #    return
                if (self.visited_list.count(child_topic)) == 0:
                    #print('\tadding "%s" "%s"'%(' -> '.join(self.stack), child_topic))
                    self.queue.append({"parent": title, "child": child_topic, "path": ' -> '.join(self.stack), "index": index, "total": len(topic.children)})

        # Pop one URL from the queue from the left side so that it can be crawled
        current = self.queue.popleft()
        #print(current)
        #print('"%s" "%s"'%(current["parent"], title))
        #print("'%s' '%s' '%s'"%(current["path"], title, current["child"]))
        #print("'%s' '%s'"%(current["path"], current["child"]))

        #if current["parent"] != title:        
        #            self.stack.pop()

        #    #print('pop', self.stack)
        
        #    if (self.stack[-1]!=current["parent"]):                
        #        self.stack.append(current["parent"])

        #print('\t[%s]'%(current["path"]))
        #print('"%s" -> "%s"  %d/%d'%(current["parent"], current["child"], current["index"], current["total"]))
        # Recursive call to crawl until the queue is populated with 100 URLs
        
        #self.stack.pop()
        self.bfs_crawl(current["child"])
        
                
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start')
    args = parser.parse_args()

    if not args.start:
        print('Please specify a starting page.')

    if not os.path.exists('cache'):
        os.makedirs('cache')

    start = args.start.replace('_', ' ')

    crawler = Crawler(True)
    crawler.bfs_crawl(start)
