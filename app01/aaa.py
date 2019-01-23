import time
def show_time(f):
    t1 = time.time()
    def inner(*args):
        f()
        t2 = time.time()-t1
        print(t2)
    return inner

@show_time
def add():
    ret = 1
    for i in range(10000100):
        ret+=1
    print(ret)


@show_time
def mul(x,y):
    x = x**y
    print(x)

mul(23,28)