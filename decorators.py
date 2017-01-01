from time import sleep,time
import random


def static_var(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def randomize(max_dur=5):
    def decorate(func):
        def new_func(*args, **kwargs):
            random.seed(time())
            sleep(random.random() % max_dur)
            func(*args, **kwargs)
        return new_func
    return decorate

if __name__ == '__main__':
    # the same as f = static_var(count=1)(f)
    @static_var(count=1)
    def f():
        f.count+=1
        print "count is " + str(f.count)

    @randomize(4)
    def delay(string="world"):
        print "hello"+" "+string

    f()
    f()
    f()
    f()

    delay()
    delay("str")
    delay(string="gf")
    delay()