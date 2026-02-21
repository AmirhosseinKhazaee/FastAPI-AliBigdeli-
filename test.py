from contextlib import contextmanager

@contextmanager
def generator():
    try:
        # خود generator به جای لیست کامل
        g = (i for i in range(1,10))  # generator expression
        yield g
    finally:
        print("___End___")

with generator() as g:
    print(next(g))  # 1
    print(next(g))  # 2xx