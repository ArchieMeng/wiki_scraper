import random
from time import sleep, time


def static_var(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def randomize(min_dur=0, max_dur=5):
    # this function will not delay when min_dur > max_dur
    method_delay = True
    if min_dur > max_dur:
        method_delay = False

    def decorate(func):
        def new_func(*args, **kwargs):
            if method_delay:
                random.seed(time())
                sleep(random.randint(min_dur, max_dur))
            return func(*args, **kwargs)
        return new_func
    return decorate

if __name__ == '__main__':
    # the same as f = static_var(count=1)(f)
    @static_var(count=1)
    def f():
        f.count+=1
        print "count is " + str(f.count)

    @randomize(6)
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