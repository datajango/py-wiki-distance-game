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
import Levenshtein

# Levenshtein distance (LD) is a measure of the similarity between two strings,
# which we will refer to as the source string (s) and the target string (t). 
# The distance is the number of deletions, insertions, or substitutions required 
# to transform s into t. For example,

# The Levenshtein distance algorithm has been used in:
# Spell checking
# Speech recognition
# DNA analysis
# Plagiarism detection

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
      return False # topic isn't even in the Graph

  # debug print the graph
  def dump(self):
    for topic in self.graph.keys():
      print(topic)


def calc_levenshtein_distance(graph, wiki_page, target):
  
  target_topics = target.lower()      
  target_topics_words = target_topics.split(' ')

  levenshtein_matches = []
  # reorder order list based on the target
  for link in wiki_page.links:
    page_topics = link.replace('(', '')
    page_topics = page_topics.replace(')', '')
    page_topics = page_topics.replace(')', '')
    page_topics = page_topics.lower()      
    page_topics_words = page_topics.split(' ')
    #print(wiki_page.title, page_topics_words)
    #print(target_topics_words)
    intersection = set(target_topics_words).intersection(set(page_topics_words))
    if bool(intersection):        
      dist = Levenshtein.distance(link.lower(), target.lower())
      #print(link, intersection, dist)
      levenshtein_matches.append([link, dist])        
      # sort the matches by the levenshtein distance

  if levenshtein_matches:
    sorted_links = sorted(levenshtein_matches, key=lambda x: x[1])
    #print(sorted_links)    
    return sorted_links

  return None

def check_links(graph, sorted_links, target):

  for link in sorted_links:      
    #print(link[0])
    child_page = wiki_fetch(link[0])
    if child_page:
      graph.add_topics(child_page)
      if graph.check_topic_links_for_target(child_page.title, target):
        topic_stack.append(link[0])
        topic_stack.append(target)
        return ' -> '.join(topic_stack)

  return None

graph = WikiTopicGraph()
#bfs = deque()
topics = {}  # store all visited pages
topic_stack = []  # list used as a stack to push and pop topics as the recursion happens
visited = {}  # store all visited pages

# This function is a kinder-gentler Wiki Media API fetch because is uses a page cache.
def wiki_fetch(id):
    filename = os.path.join('cache', id + ".obj")

    if os.path.exists(filename):
        # using cache wikipedia
        topic = pickle.load(open(filename, "rb"))
        return topic
    else:
        # hitting wikipedia
        #print('hitting wikipedia for %s'%(id))
        try:
            topic = wikipedia.page(id)
            pickle.dump(topic, open(filename, "wb"))
            return topic
        except:
            print('Wiki Fetch Error!')
            return None


# this function is not complete.
# I want to add a real breadth first search to it 
# Right now I optimize by looking for Levenstein distance between the link topics
# on each page and the target topics/

# I feel I could make this alot better

# First I want to add a real breadth first search
# Then I want to augment it with the Levenstein distance 
# then I want to use NLTK and add some smarts to the set intersection function.
#   right now intersection = set(target_topics_words).intersection(set(page_topics_words)) is 
#   a boolean..  I want it to be fuzzy based on word meanings.
#   maybe I load a good corpus and get that feature going.

def crawl(start, target):

    if start in visited:
        return None
    else:
        visited[start] = True
    topic_stack.append(start)

    wiki_page = wiki_fetch(start)

    graph.add_topics(wiki_page)

    if graph.check_topic_links_for_target(wiki_page.title, target):
      topic_stack.append(target)
      return ' -> '.join(topic_stack)

    # load all topics on the current page but do not recurse into them just yet
    #print('There are %d links on topic page %s'%(len(wiki_page.links), start))
    
    sorted_links = calc_levenshtein_distance(graph, wiki_page, target)
    if sorted_links:      
      #print('page %s has some levenstien matches'%(wiki_page.title))
      #print(sorted_links)
      match = check_links(graph, sorted_links, target)
      if match:
        return match

    for index, link in enumerate(wiki_page.links):
      #print(index+1, link)
      child_page = wiki_fetch(link)
      if child_page:
        #print('add_topics for child_page %s'%(child_page.title))        
        graph.add_topics(child_page)
        if graph.check_topic_links_for_target(child_page.title, target):
          topic_stack.append(link)
          topic_stack.append(target)
          return ' -> '.join(topic_stack)

        # now check if there are any link on the page with a close levenstien distance
        sorted_links = calc_levenshtein_distance(graph, child_page, target)
        if sorted_links:
          #print('child page %s has some levenstien matches'%(child_page.title))
          topic_stack.append(child_page.title)
          match = check_links(graph, sorted_links, target)
          if match:
            return match
          topic_stack.pop()

      else:
        print('Error with topic %s'%(link))

    for link in wiki_page.links:      
      results = crawl(link, target)
      if results:
        return results

    topic_stack.pop()
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('start')
    parser.add_argument('target')
    args = parser.parse_args()

    if not args.start:
        print('Please specify a starting page.')

    if not args.target:
        print('Please specify a target page.')

    if not os.path.exists('cache'):
        os.makedirs('cache')

    start = args.start.replace('_', ' ')
    target = args.target.replace('_', ' ')

    path = crawl(start, target)
    if path:
        print(path)
