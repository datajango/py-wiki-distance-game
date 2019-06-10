# Fibonacci

def fib(a):
  if a <= 1:
    return a
  else:
    return(fib(a-1) + fib(a-2))

numbers = range(0,10)

for x,n in enumerate(numbers):
  print(x, fib(n))
  
  

