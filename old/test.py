import concurrent.futures

def add(a,b):
    return a+b

with concurrent.futures.ThreadPoolExecutor() as ex:
    future = ex.submit(add,1,2)
    future1 = ex.submit(add,2,2)
    future2 = ex.submit(add,3,2)
    print(future.result(), future1.result(), future2.result())