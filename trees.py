from collections import deque


class Node():
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children = {}

    def add(self, name):
        n = Node(self, name)        
        #print('%s parent is %s'%(name, n.parent.name))
        self.children[name] = n
        return n

def tree_path(node):  
  results = []

  if node.parent:    
      x = tree_path(node.parent)
      results.extend(x)
  
  results.append(node.name)

  return results

def traverse(node, depth):
  indent = ' ' * depth
  #print('%s%s %s'%(indent, node.name, '->'.join(tree_path(node))))
  print('%s%s'%(indent, '->'.join(tree_path(node))))
  depth+=1
  for key, ele in node.children.items():
    #print('%s%s'%(indent, key))
    traverse(ele, depth)
  depth-=1

class Crawler():
    def __init__(self):
        self.queue = deque([])
        self.visited_list = []
        self.stack = []
        
    def bfs(self, node):

        print("bfs=>'%s' %s"%(node.name, '->'.join(tree_path(node))))

        #self.stack.append(node.name)
        self.visited_list.append(node.name)
 
        for key, child in node.children.items():
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
                else:
                    print('Skipped %s'%(tree_path(child)))

        # Pop one URL from the queue from the left side so that it can be crawled
        if self.queue:
          current = self.queue.popleft()
          self.bfs(current)

        else:
          return


def create_tree():
  node = Node(None, 'a')
  node1_1 = node.add('b1')
  node1_2 = node.add('b2')
  node1_3 = node.add('b3')
  
  node2_1 = node1_1.add('c1')
  node2_2 = node1_1.add('c2')
  node2_2 = node1_1.add('c3')

  node3_1 = node2_1.add('d1')
  node3_2 = node2_1.add('d2')
  node3_3 = node2_1.add('d3')
  node3_4 = node2_1.add('b1')

  node4_1 = node1_2.add('e1')
  node4_2 = node1_2.add('e2')
  node4_2 = node1_2.add('e3')

  node5_1 = node4_1.add('f1')
  node5_2 = node4_1.add('f2')
  node5_3 = node4_1.add('f3')
  node5_4 = node4_1.add('g1')


  return node

root = create_tree()
traverse(root, 0)

crawler = Crawler()
crawler.bfs(root)



