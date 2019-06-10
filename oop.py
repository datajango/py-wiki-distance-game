class Mammal:
  species = ''
  greeting = ''

  def __init__(self, name):
    self.name = name

  def greet(self):
    print("%s %s says %s"%(self.species, self.name, self.greeting))

class Cat(Mammal):
  species = 'feline'
  greeting = 'meow'

  def __init__(self, name):      
    super(Cat, self).__init__(name)

class Dog(Mammal):
  species = 'canine'
  greeting = 'woof'

  def __init__(self, name):      
    super(Dog, self).__init__(name)

animals = []
animals.append(Dog('Scout'))
animals.append(Cat('Ginger'))

for animal in animals:
  animal.greet()


