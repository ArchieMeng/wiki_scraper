def static_var(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

if __name__ == '__main__':
    # the same as f = static_var(count=1)(f)
    @static_var(count=1)
    def f():
        f.count+=1
        print "count is " + str(f.count)

    f()
    f()
    f()
    f()