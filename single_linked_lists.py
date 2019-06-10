class Node:  
  def __init__(self, data):
    self.item = data
    self.ref = None

class LinkedList:  
  def __init__(self):
    self.start_node = None

  def insert_at_start(self, data):
    new_node = Node(data)
    new_node.ref = self.start_node
    self.start_node= new_node    

  def traverse_list(self):  
    if self.start_node is None:
      print("List has no element")
      return
    else:
      n = self.start_node
      
      while n is not None:
        print(n.item , " ")
        n = n.ref
  
  def insert_at_end(self, data):
    new_node = Node(data)
    
    if self.start_node is None:
      self.start_node = new_node
      return
    
    n = self.start_node
    
    while n.ref is not None:
      n= n.ref
    
    n.ref = new_node


snl = LinkedList()
snl.insert_at_end('Tony')
snl.insert_at_end('Stacy')
snl.insert_at_end('Garret')
snl.insert_at_end('Allison')
snl.traverse_list()

