
import os, time, re

# get the path
print(os.getcwd())

# get file metainfo
metadata = os.stat("pythonstudy.py")
print(time.localtime(metadata.st_mtime))

a_list = [x**2 for x in range(10) if x % 2==0]
print(a_list)

phonePattern = re.compile(r'^(\d{4})-(\d{8})-(\D*)')
find = phonePattern.search("0398-44556677-").groups()

print(re.sub('[ove]', 'i', "Lofe"))

print(re.sub('([^aeiou])y$', r'\1ies', 'funny'))

temp = (a, b, c) = range(3)

linecount = 0
with open("pythonstudy.py") as demofile:
	for line in demofile:
		linecount+=1

def fib(max):
    """function's docstring"""
    x, y = 0, 1
    while x < max:
      yield x
      x, y = y, x+y


# for x in fib(10):
# 	print(x, end=" ")
'''
class FibIterator():
	"""docstring for FibIterator"""
	ins_count = 0;
	def __init__(self, max):
		super(FibIterator, self).__init__()
		self.max = max

	def __iter__(self):
		self.a = 0
		self.b = 1
		return self

	def __next__(self):
		fib = self.a
		if fib > self.max:
			raise StopIteration
		self.a, self.b = self.b, self.a + self.b
		return fib

fibIter = FibIterator(10)
fibIt = FibIterator(100)
fibIt.ins_count = 3
print(fibIter.__class__.ins_count)
fibIt.__class__.ins_count = 6
print(fibIter.__class__.ins_count)
print(fibIter.ins_count)
print(fibIt.ins_count)
print(fibIt.__class__.ins_count)
'''

mystring = "How time flies!"
print(set(mystring))

gen_exp = (a for a in range(15) if a % 3 == 0)
print(tuple(gen_exp))

mylist = [12, 2, 13, 4]
print(sorted(["12", "2", "132", "4"], key=len))

print(eval('"A" + "B"')) 

mydict = {'name':'GoT', 'producer':'HBO', 'lang':'eng'}
mydict.setdefault('date',2016) # makesure that key 'date' is initialized
mydict['date'] = 2010 # we dont need to check the 'date' is in the dict now

for k,v in sorted(mydict.items()):
    print(k+' is: '+str(v))

import pprint
got = {'name':'GoT', 'producer':'HBO', 'lang':'eng'}
hoc = {'name':'House of Card', 'producer':'Netflix', 'lang':'eng'}
tvs = {}
tvs['got'] = got
tvs['hoc'] = hoc
pprint.pprint(tvs)

def double(arg):
    arg = arg * 2
    print(arg) # [1, 2, 1, 2]

def change(arg):
    arg.append('data')

val = [1,2]
double(val) 
print(val) #[1, 2]

change(val)
print(val) # [1, 2, 'data']

import sqlite3

def database_work():
    # connect to the database, if file is not exist, this will create it 
    conn = sqlite3.connect('log.db')
    # create a Cursor
    cursor = conn.cursor()
    showtables = """select name from sqlite_master where type='table' order by name"""
    cursor.execute(showtables)
    result = cursor.fetchall()
    if len(result) == 0:
         # execute a sql statement
         cursor.execute('create table log (id INTEGER PRIMARY KEY AUTOINCREMENT, request varchar(50))')
    else:
        print(result)
    # insert a data
    cursor.execute("insert into log (request) values ('christmas')")
    # close the Cursor
    cursor.close()
    # commit the transaction
    conn.commit()
    # close the connect
    conn.close()

class CountFromBy(object):
    """docstring for CountFromBy"""
    def __init__(self, v: int = 0, s: int=1) -> None:
        super(CountFromBy, self).__init__()
        self.val = v
        self.step = s

    def increase(self) -> None:
        self.val += self.step

    def __repr__(self) -> str:
        return str(self.val)


def outter_fun():
    def inner_print():
        print('xxx')

    print('return inner fun:')
    return inner_print()

def show_fun(*args):
    for arg in args:
        print(arg)

def show_dict(**kwargs):
    for k, v in kwargs.items():
        print(k, v, sep='->', end=' ')  

def show_any_args(*args, **kwargs):
    if args:
        for arg in args:
            print(arg)
    print()
    if kwargs:
        for k, v in kwargs.items():
            print(k, v, sep='->', end=' ')


from functools import wraps

def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Code to execute before calling the decorated function.

        # 2. Call the decorated function as required, returning its results if needed.
        return func(*args, **kwargs)
        # 3. Code to execute Instead of calling the decorated function.

    return wrapper

class WorldNotWork(Exception):
    pass

def test_world_not_work():
    try:
        raise WorldNotWork('The world has been corrupt....') 
    except WorldNotWork as e:
        print("Some error", str(e)) #Some error The world has been corrupt....
           

def read_file():
    try:
        with open('xxx.txt') as fd:
            file_data = fd.read()
        print(file_data)
    except FileNotFoundError:
        print('file is missing.')
    except PermissionError:
        print('not allowed.')
    except Exception as err:
        print('some error occurred:', str(err))

def test_return_list():
    # text = 'key,value,keys' # ValueError: too many values to unpack
    text = 'key,value'
    k, v = text.split(',')
    print(k,v)

from datetime import datetime

def convert2ampm(time24: str) -> str:
    return datetime.strptime(time24, '%H:%M').strftime('%I:%M %p')

def gen_dest(time_table:dict):
    for k, v in time_table.items():
        yield v
        print(k) # this will be execute next time

import requests

def gen_from_urls(urls:tuple)->tuple:
    # use generator expression to request each url
    for resp in (requests.get('http://'+url) for url in urls):
        yield len(resp.content), resp.status_code, resp.url

def test_generator():
    fts = {'10:00':'Hongkong', '08:00':'NewYork', '16:00':'Hongkong', '12:00':'Taipei',}
    
    for v in gen_dest(fts):
        print(v)

    demo = [print(v) for v in gen_dest(fts)]

    
    when = {}
    for dest in set(fts.values()):
        templist = []
        for k, v in fts.items():
            if v == dest:
                templist.append(k)
                
        when[dest] = templist

    print(when)
    when2 = { dest : [k for k, v in fts.items() if v == dest] for dest in set(fts.values()) }
    print(when2)

    #list comprehension
    for i in [x*2 for x in [1, 2, 3, 4]]:
        print(i)
    print('------------------------')
    #generator
    for i in (x*2 for x in [1, 2, 3, 4]):
        print(i)
    
    urls = ('www.baidu.com', 'www.douban.com', 'www.qq.com')
    # use dict comprehension to iterator the generator function
    # the `_`underscore is Python's defualt variable name, tells the code to ignore the second value
    urls_res = { url : size for size, _, url in gen_from_urls(urls) }
    print(urls_res)

import threading
import asyncio

@asyncio.coroutine
def hello():
    print('Hello world! (%s)' % threading.currentThread())
    yield from asyncio.sleep(3)
    print('Hello again! (%s)' % threading.currentThread())

def asynDemo():
    loop = asyncio.get_event_loop()
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == '__main__':
    value = 3.14
    tag = 'is for circle'
    msg = 'Value %2.2f %s' % (value, tag)
    print(msg)
    msg = 'Value {} which {}'.format(value, tag)
    print(msg)

    fts = {'10:00':'Hongkong', '08:00':'NewYork', '16:00':'Hongkong', '12:00':'Taipei',}
    for k in sorted(fts, key=fts.get, reverse=True):
        print(k, '->', fts[k])

    asynDemo()

    
