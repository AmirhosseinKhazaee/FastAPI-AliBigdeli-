from contextlib import contextmanager

# @contextmanager
def generator():
    try:
        x = 0
        while True:
            yield x
            x+=1
    finally:
        print("___End___")
        
g= generator()
for i in range(2):
    print(next(g))