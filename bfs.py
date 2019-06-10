from collections import deque

class Node():
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children = {}

    def add(self, name):
        self.children[name] = Node(self, name)
        return self.children[name]

def print_path(node):
    results = []    
    if node.parent:
        x = print_path(node.parent)
        results.extend(x)
    else:        
        results.append(node.name)
    
    return results
 
def traverse(depth, node):
    indent = ' ' * depth * 2
    print('%s%s'%(indent, node.name))    
    for key in node.children:
        ele = node.children[key]
        traverse(depth+1, ele)

class Crawler():
    def __init__(self):
        self.topics = {}  # store all topics pages
        self.queue = deque([])
        self.visited_list = []
        self.stack = []
        
    def bfs(self, node):    
        #self.stack.append(node.name)
        #print('%s %s'%('->'.join(self.stack), node.name))

        self.visited_list.append(node.name)
 
        for key, child in node.children.items():
            #print(key, child.children)
            flag = 0
            
            # Check if the URL already exists in the queue
            for j in self.queue:
                if j.name == key:
                    flag = 1
                    break

            # If not found in queue
            if flag == 0:
                if (self.visited_list.count(key)) == 0:                    
                    self.queue.append(child)

        # Pop one URL from the queue from the left side so that it can be crawled
        if self.queue:
          current = self.queue.popleft()
          #print('%s'%(current.name))
          my_path=[]
          print_path(current, my_path)
          print(my_path)

          #print('%s %s'%(current.parent.name, current.name))

          #self.stack.pop()
          self.bfs(current)
        else:
          return

root = Node(None, 'a')
node_b = root.add('b')
node_c = root.add('c')
node_d = root.add('d')

node_b.add('f')
node_b.add('g')

node_e = node_b.add('e')
node_e.add('e-1')

node_c.add('h')
node_i = node_c.add('i')
node_i.add('i-1')
node_c.add('j')

node_d.add('l')
node_d.add('m')
node_n = node_d.add('n')

my_path=print_path(node_e)    
print(my_path)

#traverse(0, root)
#crawler = Crawler()
#crawler.bfs(root)