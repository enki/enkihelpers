import threading
import time
import traceback
import random

def unhandled_exc_handler():
    traceback.print_exc()

def buchtimer(maxtime=0.2):
    def wrap1(func):
        def wrap2(*args,**kwargs):
            starttime = time.time()
            result = func(*args, **kwargs)
            timediff = time.time() - starttime
            if timediff > maxtime:
                print 'Func %s took %s seconds (maxtime=%s).' % (func, timediff, maxtime)
        return wrap2
    return wrap1

class MagicThread(object):
    def __init__(self):
        self.event = threading.Event()
        self.thread = None
    
    def spawnThread(self, func, *args, **kwargs):
        name = func.func_name + '#%x' % int((16**10)*random.random())
    
        self.thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=name)
        self.thread.start()
    
def timebox(maxtime=0.5):
    def wrap1(func):
        def wrap2(*args, **kwargs):
            def timeboxed(mthread, args, kwargs):
                result = func(*args, **kwargs)
                mthread.event.set()
            mthread = MagicThread()
            mthread.spawnThread(timeboxed, mthread, args, kwargs)
            return mthread
        return wrap2
    return wrap1

@timebox()
@buchtimer()
def takeyourtime():
    print 'making tea'
    time.sleep(0.4)
    print 'aaah.. green jasmine.'

def main():
    mthread = takeyourtime()
    mthread.event.wait()
    print 'BACK'

if __name__ == '__main__':
    main()