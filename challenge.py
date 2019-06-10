
import time

'''

if n is even then:
  n = n /2
else
  n = 3 * n + 1
  
13 -> 40 -> 20 - > 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
n=13
n=40

400 

# find an n such that 
  if n = n/2 
  
  
'''

cache = {}
def save(n,ans):
  if n not in cache:
    cache[n]=ans

def foo(n):
  counter = 0
  
  if n == 1:
    counter += 1
    return counter

  if n in cache:
    ans = cache[n]
  else:
    if (n % 2) == 0:
      ans = n/2    
    else:
      ans = 3 * n + 1
      
  cache[n]=ans
  
  #print(n)
  counter += 1
  x = foo(ans)
  counter += x
  
  #print(results)

  return counter

results=[]

for x in range(2,1000000):
  results.append((x, foo(x)))


sort = sorted(results, key=lambda x:x[1] )

#start = timeit.timeit()
start_time = time.time()
print(sort[len(sort)-1])
#end = timeit.timeit()
#print(end - start)
elapsed_time = time.time() - start_time

print(elapsed_time)


# your code



'''

time python run.py
'''
  
  
