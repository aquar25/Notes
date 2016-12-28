

# python study

### Start

REPL: read-eval-print-loop, describes an interactive programming tool that lets you experiment with snippets of code to your heart's desire.

`from module import function`, functions are inside modules which inside the standard library.  

*Python programmers prefer not to create the temporary variable unless it's needed at some point later in the program.*

Instead of referring to a code "block", Python programmers use the word "suite". Any suit can contain any number of embedded suites, which also have to be indented.

Most programmers configure editor to replace a tap of the *Tab* key with *four spaces*.

Python is object-based as opposed to purely object-oriented. 

Everything in python is an object, so anything can be assigned to a variable.

#### Idiom

* `__name__` stand for  the current module. Python use "double underscore, name, double underscore" phrase to name some special use. "dunder name" is shorthand for  "double underscore, name, double underscore". "wonder" is shorthand for "one underscore"
* `__main__` if a Python code is executed directly by Python, the active namespace is `__main__`. However, if the code is imported as a module,  the `__name__`is the name of imported module.

#### PEP

PEP is shorthand for Python Enhancement Protocol. The details of PEP documents can be very technical and esoteric. The vast majority of Python programmers are aware of their existence but rarely interact with PEPs in detail. PEP 8 is the style guide for Python code. PEP 8 documentation states that readability counts, and that code is read much more often than it is written. You should try to ensure your code to conform to the PEP 8 guidelines.

##### PEP 8 Check

1. Install pytest and pep8 `python3 -m pip install pytest` and `python3 -m pip install pytest-pep8`
2. In the same folder of your python file, run `py.test --pep8 commonfun.py`
3. modify the file as the message



### Operator

python supports `+= , -=` but`++, --`

### Statement

#### Condition

In python, `True` and `False` are the two boolean keywords.

```python
minute = datetime.datetime.today().minute

if minute > 30:
    print("later of hour")
elif minute == 30:
    print("half of hour")
else:
    print("first of hour")
```

Python also supports write condition statements in one line. `x = 10 if y>3 else 20` But it is not used widely, as it's hard to read.

Every object in Python has a truth value associated with it. Use built-in function `bool(object)`to check the truth of the object. Any non-empty data structure evaluates to TRUE.

##### In 

`in` 可以用来判断一个元素是否在一个collection中，同理`not in`判断这个元素不在一个collection中

#### Loop

for循环有三种主要用途：

1. 遍历一个list中的所有元素
2. 遍历一个序列中的所有元素，例如字符串
3. 循环num次数

* range()函数用法，只有一个参数时，默认start为0, step为1，序列为[start, stop)，注意得到的时range对象，可以使用list(range(5))，将其转换为list

range(stop) -> range object

range(start, stop[, step]) -> range object

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
import time
import random

for i in range(10):
    second = datetime.today().second
    if second > 30:
        print("later of min")
    elif second == 30:
        print("half of min")
    else:
        print("first of min")

    randtime = random.randint(1,60)
    print(randtime)
    time.sleep(randtime)
```

for循环支持遍历list和list的切片

```python
mylist = [1,2,3,4,5,6,7,8]
for x in mylist[:6:2]:
    print(x) #输出1,3,5
```



#### import

import用来将一个module加入当前的namespace中，python支持两种方式的import:

1. `from datetime import datetime` 从一个模块中引入一个函数或子模块到当前namespace，后续使用时不需要使用`datetime.datetime.today()`的方式来调用函数
2. `import time` 只是导入模块，调用模块函数需要使用dot-notation syntax，e.g. `time.sleep(5)`

在python shell中，可以使用`dir(obj)`来显示一个obj的所有属性，这个obj可以是python中的任何对象，包括模块。

在python shell中，可以使用`help(fun)`来显示一个fun的帮助信息

###list

list is an ordered mutable collection of objects. list的大小可以动态变化。一个list中的数据类型也可以不同。mutable意味数据在运行时可以动态改变。

#### 方法

mylist = [1, 2, 3, 4]

* 添加一个元素 `mylist.append(obj)`
* `mylist.remove(obj)`删除list中第一次出现obj的元素，如果没有这个obj将会raise一个error
* `mylist.pop(index)`删除list中索引为index的元素，并将元素作为返回值返回，如果没有传入参数index，则删除list最后一个元素
* `mylist.extend(hislist)`将hislist的元素全部添加到mylist中。`mylist.extend([])`将不会添加任何元素到现有的list中，但是`mylist.append([])`会添加一个空list到当前list的最后。
* `mylist.insert(index, obj)`在索引index之前插入一个元素obj
* `herlist = mylist`赋值语句只是将herlist也引用到了mylist，它们还都是同一个list，如果要copy，需要使用copy方法，`newlist = mylist.copy()`


* sorted() 函数接受一个列表并将它排序后返回。默认情况下，它按字母序排序
  sorted([12, 2, 13, 4]) # [2, 4, 12, 13]
  sorted(["12", "2", "132", "4"], key=len) # ['2', '4', '12', '132']
  对列表的每一个元素执行key中指定的方法进行排序

#### list slice

list的最后一个元素的索引是`-1`，依次往前为`-2,-3...`

`newlist = mylist[start:stop:step]`，使用切片的方式获取一个新的list，其中start表示开始的索引位置，stop表示结束索引位置，不包含这个stop索引对应的值，step表示每几个取一个元素，step默认值为1.

```python
mylist = [1,2,3,4,5,6,7,8]
newlist = mylist[1:7:2] # [2, 4, 6]
newlist = mylist[-3:] #[6, 7, 8] 获取最后三个元素
newlist = mylist[::-1] # [8, 7, 6, 5, 4, 3, 2, 1] 当step为负数时，表示从后向前步进
newlist = mylist[6:2:-1] # [7, 6, 5, 4]
```

python中的所有sequence都支持slice操作，不止list

#### 列表解析

a_list = [x**2 for x in range(10) if x % 2==0]
得到 [0, 4, 16, 36, 64]，先执行for遍历一个列表（0-9十个数字），在判断满足if条件的元素，最后将满足条件的元素执行平方操作，得到一个新的列表。其中x**2可以是任何可以执行的表达式

###元组

Tuple is an ordered immutable collection of objects.

元组是不可变的列表，速度比列表快，可以用作字典的key。Perhaps you have a large constant list and you're worried about performance.
可以使用元组作为函数的返回值，因为元组可以进行元素的一一赋值，如  
(a, b, c) = range(3)
a: 0
b: 1
c: 2

* every tuple needs to include at least one comma between the parentheses. 当一个元组中只有一个元素是，需要在这个元素后面加上`,` 否则编译器会认为这个支持一个()包围起来的普通数据。`t = ('value')`, the type of `t` is `str`. 正确的写法应该是`t=('value',)` 当元组作为函数的参数和返回值时，也要保证这一点。

### 字典

Dictionary is an unordered set of key/value pairs. 字典是mutable

Python's dictionary is implemented as a resizeable hash table.

Python's *for* loop can be used to iterate over a dictionary. On each iteration, the key is assigned to the loop variable, which is used to access the data value.

#### 方法

* 通过调用内建函数`sorted(dict)`可以将dict的数据按key进行排序.`sorted()` built-in function doesn't change the ordering of the data you provide to it, but instead returns an ordered copy of the data.

* `dict.items()`returns a list of the key/value pairs. 

  ```python
  mydict = {'name':'GoT', 'producer':'HBO', 'lang':'eng'}
  for k,v in sorted(mydict.items()):
      print(k+' is: '+v)
  ```

* `dict.setdefault('key', 'defaultvalue')` This method guarantees that a key is always initialized to a default value before it's used. This method does nothing if a key already exists.

  ```python
  mydict = {'name':'GoT', 'producer':'HBO', 'lang':'eng'}
  mydict.setdefault('date',2016) # makesure that key 'date' is initialized
  mydict['date'] = 2010 # we dont need to check the 'date' is in the dict now
  ```

* 如果直接访问一个字典的key，如果字典中还没有添加这个key，会出现KeyError。因此当一个key对应的值为boolean类型时，可以通过判断这个key是否在字典中来判断是否为true，如果需要将key值设置为false，则通过调用pop(key)方法来将key弹出字典中，使用`key in dict` 的方式来判断

* ​




###集合

Set is an unordered set of unique objects.

集合中的元素没有重复的. Set is much faster than list when lookup is the primary requirement. As lists always perform slow sequential searches, sets should always be preferred for lookup.
* 统计字符串中出现的字母

  ```
  mystring = &quot;How time flies!&quot;
  print(set(mystring))  # {'m', 'e', '!', 'o', 'i', 's', 'f', 'w', ' ', 'l', 't', 'H'}
  ```

* list 和set之间可以相互转换，`myset = set(mylist)` or `mylist = list(myset)`

* `myset.union(hiset)` 获取两个集合的并集

* `myset.difference(hiset)` 获取两个集合的差集，myset有的而hiset中没有的

* `myset.intersection(hiset)` 获取两个集合的交集

* 当一个集合为空时，此时解释器使用set()来表示它。因为{}标识一个空的字典




###编码

由于世界上的各各个语言的字符太多，而在同一个文本文件中，可能存在多种语言的字符，因此需要一种编码可以覆盖所有语言的所有字符。Unicode就是做这个事情，UTF-32使用4个字节表示所有字符，但是实际上大部分语言一共也没有用到65535个字符，而4个字节的UTF-32中却却存在一堆不是你当前使用语言需要的字符。为了节省空间就定义了utf-16，使用两个字节来表示一个字符字符中，两个字节构成的0-65535之间的每一个数字映射到一个字符。  
但是使用两个字节表示一个字符又有新问题，不同的系统设备上字节顺序不同，例如俩个字节 12 34 在另一个系统中可能就是34 12的顺序，因此需要字节顺序定义Byte Order Mark(BOM)在文档中定义，如果打开一个以字节FF FE开头的UTF-16文档，你就能确定她的字节顺序是单向的了，如果是以FE FF开头则说明那个字节序时反向的

utf-8是一个变长的unicode编码方案，前128个字符和ascii一样，扩展的拉丁字符如法语中的特殊字符，使用两个字节表示，而汉字则使用3个字节表示，更少用的字符使用4个字节表示，没有字节序的问题。

python3中所有的字符都是unicode的，例如
s = '中国man'
len(s) # 5
s[0]  # 中

python3 文件的默认编码为utf-8, in python2, it uses ascii.
```
#!/usr/bin/python3
#-*- coding: utf-8 *-
```

###字符串

python中可以使用`""`或`''`来标识字符串，一般如果一个字符串中有`'`符号时，才会使用`""`来标识字符串，这样可以避免在字符串中使用`\'`来转义一个字符串符号。例如`strs = "what's ur hope?"`

`"""`or`'''`包围起来的字符串可以跨多行，大部分人偏好用前者。通常用于类或函数的docstrings.

* rstrip() 字符串方法移除每一行尾部的空白
* lstrip() 方法移除头部的空白
* strip() 方法头尾都移除



### 文件

`fd = open('filename', 'r+b')` read from and write to new binary file.

文件打开方式，除了`r`之外，如果文件不存在，其他模式会自动创建一个文件：

* `r` 默认的文件打开方式，以读方式打开文件，文件必须存在
* `w` 以写方式打开，如果文件中存在内容，则清空文件中的内容
* `a` 追加的方式打开文件，在文件最后追加内容
* `x`创建一个新文件用来写数据，如果文件已经存在，则返回失败

默认文件以文本模式打开，如果要以二进制打开需要指明选项`b`.

在文件打开后，要记得调用close方法关闭文件，因此通常使用with语句来打开文件，在执行完代码块后，解释器会自动释放资源，调用close。

```python
fd = open('yourname')
print('something', file=fd, end='|') # 将内容写入到文件中,使用指定的结束符
print('thing1', 'things2', 'things3', file=fd, sep='|') # 将所有的字符使用sep指定的分隔符分隔开
close(fd)
```



### with

Context management protocol dictates that any class you create must define at least two magic methods:`__enter__` and `__exit__`. When you adhere to the protocol, your class can hook into the with statement. A protocol is an agreed procedure (or set of rules) that is to be adhered to.

The interpreter invokes the object's `__enter__` method before the with statement's suite starts. The  `__enter__` can return a value to the with statement. As the with suite ends, the interpreter always invokes the object's `__exit__` method.  As the code in the with statement's suite may fail (and raise an exception), dunder exit has to be ready to handle this if it happens. 

 `__exit__`  method accepts another 3 arguments `__exit__(self, exc_type, exc_value, exc_trace)` for handle the exception in the with statement.

 With statement manages the context with in which its suite runs.

```python
with open("pythonstudy.py", encoding="utf-8") as demofile:
	for line in demofile:
		print(line)
```

自定义上下文管理协议类

```python
import sqlite3

# db_config = {
#     'dbname':DB_FILE,
#     'tbname':LOG_TABLE_NAME
#     }

class UseDatabase(object):
    """docstring for UseDatabase"""
    def __init__(self, config: dict)->None:
        super(UseDatabase, self).__init__()
        self.config = config

    def __enter__(self) -> 'cursor':
        self.conn = sqlite3.connect(self.config['dbname'])
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

# use it in a with statement
with UseDatabase(app.config['dbconfig']) as cursor:
        _sql = "select year, month, day, address, browser from "  + LOG_TABLE_NAME
        cursor.execute(_sql)
        contents = cursor.fetchall()
```



### 

###正则表达式
pattern = r'^k?M{0,4}(\bDK\b|K?)$'
re.search(pattern, "Mmm")	

r表示忽略字符串中的转义字符
^表示开头
$表示结束
\b 单词边界，如\bDK\b 匹配的是 " DK "
k? k出现1次货0次
M{0,4} M出现0次到4次之间的所有情况，如MM MMM MMMM ,其中0表示最少出现的次数，4表示最多出现的次数
(a|b|c) 单独匹配 a b c 中的任何一个


phonePattern = re.compile(r'^(\d{4})-(\d{8})')
find = phonePattern.search("0398-44556677-yy").groups() # ('0398', '44556677')

phonePattern = re.compile(r'^(\d{4})-(\d{8})-(\D*)')
find = phonePattern.search("0398-44556677-").groups() #('0398', '44556677', '')


\d 任意单个数字 
\d{4} 任意单个数字出现4次，必须是连续4次
(\d{4}) 匹配4个数字为一分组，groups()方法会返回匹配过程中满足所有分组的一个元组('0398', '44556677')，如果没有匹配的分组，则会返回空，通过使用分组可以找到匹配分组的值

\D 任意单个非数字
+ 匹配一个或多个
* 匹配0个或多个
  [sxz] 匹配s x z其中之一
  re.sub('[ove]', 'i', "Lofe") # Lifi 实现基于正则的替换，原来字符串中的o和e被替换为i
  re.sub('[^aeiou]y$', 'ies', 'funny') #funies []中的^表示非的意思，以y结束，且y的前面不是aeiou中的任何一个字母，则将匹配的字符串替为ies，但此时会发现y前面匹配的n也被替换掉了，可以使用分组进行改进
  `re.sub('([^aeiou])y$', r'\1ies', 'funny')` # funnies  
  在上面的语句中([^aeiou])是一个分组，而替换字符串中的\1代表了第一个分组的内容即n，

temp = re.findall(r'giv.?', 'mom give me money'); # ['give']
findall():返回满足查询正则表达式的所有字符串，对于重叠的匹配，则不返回

### Function



```python
def cal_fib(max:int) -> int : # annotation tells that this function recevies an int argument and returns an int value.
    """function's docstring"""
	x, y = 0, 1
	while x < max:
		yield x
		x, y = y, x+y
```

PEP 8 suggests that words in a function's name should be separated by an underscore.

Python 3 supports a notation called annotations or  type hints. Function annotations are optional and informational. 即使一个函数增加了注解，解释器也不会检测这个函数的参数和返回值是否符合预期，注解只是为了方便调用者使用的说明，可以通过调用`help(fun_name)`来查看函数的注解信息

```python
def letter_in_phrase(phrase:str, letters:str='aeiou') -> set :
    """Get the letters in the phrase"""
    return set(letters).intersection(set(phrase))
```

Python中传入参数除了和其他语言一样按照顺序传入，还可以支持使用keyword赋值方法，将指定的参数给形参，不需要关心参数的顺序。例如

```python
print(letter_in_phrase('james blunt is a good singer', 'life'))
print(letter_in_phrase(letters='life', phrase='james blunt is a good singer'))
```

Python中对于list/dict/set这些mutable可变类型的参数是引用传递，对于str/int/tuple这些immutable参数是值传递，因为这些参数类型本来就不能被修改。

```python
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
```

上面例子中，虽然对于double()传入的是一个list，但是函数内部在执行时，先执行了=的右侧的乘法运算，并得到一个对新产生对象的引用，这个引用覆盖了作为参数引用arg（arg原来指向函数外部的list，现在指向了新生成的对象）而原来的对象并没有被修改。而函数change()则是直接修改了arg引用的list。

#### Built-in functions

* `type(obj)` 查看一个对象的类型
* `id(obj)` displays information on an object's memory address (which is a unique identifier used by the interpreter to keep track of your objects)
* `hex(int)` convert an integer into a hexadecimal number

### Module

Module is any file that contains functions.

Python中查找module的路径有三个：

1. Your current working directory
2. Your interpreter's site-packages locations
3. The standard library locations

**site-packages** contain any third-party Python modules which you may have installed.

##### Install Module to site-packages

Python 3.4 includes a module called *setuptools* , which can be used to add any module into site-packages.

1. Create a distribution description which defines the module we want setuptools to install.

   新建一个文件夹用来放模块的文件，并在该文件夹下创建两个文件`setup.py` `README.txt`.其中readme文件用来描述模块的功能，内容可以为空。`setup.py`文件描述模块并调用setuptools中setup函数。

   ```python
   #!/usr/bin/env python
   # -*- coding:utf-8 -*-

   from setuptools import setup

   # call the setup() function
   setup(
       name='commonfun',
       version='1.0',
       description='Common functions',
       author='myname',
       author_email='myemail@mail.com',
       url='xxx.com',
       py_modules=['commonfun'], # a list of '.py' files to include in the package.
       )

   ```

   ​

2. Generate a distribution file. 在模块的问加夹下执行`$python3 setup.py sdist` 生成一个压缩包`commonfun-1.0.tar.gz`

3. Install the distribution file. Using pip (Package Installer for Python) to install a distribution file.

   `python3 -m pip install commonfun-1.0.tar.gz`

在安装过自定义的模块后，就可以在任意目录import这个模块了。

最后，可以将自己编写的module放到[PyPI](https://pypi.python.org/pypi)(pronounced "pie-pee-eye", short for the Python Package Index)上.

###Generator

生成器是一个特殊的迭代器
"yield" 暂停一个函数的执行，"next()"从生成器暂停处恢复执行

def fib(max):  # define a generator
```python
x, y = 0, 1
while x < max:
	yield x  #执行到这里暂停，返回x的值
	x, y = y, x+y
```


for x in fib(10):  # for 会对fib()这个生成器循环执行执行next()
```python
print(x, end=" ")  # 0 1 1 2 3 5 8   end=" "，表示每次输出以空格结束，不是换行
```

#####生成器表达式
`gen_exp = (a for a in range(15) if a % 3 == 0) #0 3 6 9 12`
生成器表达式使用()来定义，返回的也是一个迭代器，可以使用for遍历,next(gen_exp)或者调用tuple/set/list来得到相应的容器  
`print(tuple(gen_exp)) # (0, 3, 6, 9, 12)`

### Decorator

A function decorator adjusts the behavior of an existing function without you having to change that function's code. Although decorators can also be applied to classes as well as functions, they are mainly applied to functions, which results in most Python programmers referring to them as function decorator.

通过装饰器，可以将多个函数中公共的处理逻辑提取出来，这样每个被装饰的函数只需要关心自己特有的逻辑处理，例如判断用户登录操作，在多个请求处理函数中，都是共用的，此时就可以通过装饰器来处理。通过装饰器还可以对已有的函数增加行为，而不用修改已有的函数。

* Decorator is a function
* Decorator takes the decorated function as an argument
* Decorator returns a new function, and invoke the decorated function.
* Decorator maintains the decorated function's signature, the returned function take the same number and type of arguments as expected by the decorated function.
* import `functools` module's `wraps()` function which is also a decorator.



For example, the route decorator in Flask arranges for the web server to call the function when a request for the URL arrives at the server. The route decorator then waits for any output produced by the decorator function before returning the output to the server, which then returns it to the waiting web browser.

当一个函数作为参数传入另一个函数时，接收函数内部可以调用作为参数的函数

当在一个函数内部定义一个新函数时，只能在外部函数的suite范围内调用内部定义的函数

```python
def outter_fun():
    def inner_print():
        print('xxx')

    print('call inner fun:')
    inner_print()
```

#### 闭包

从一个函数return出另一个内部函数

```python
def outter_fun():
    def inner_print():
        print('xxx')

    print('return inner fun:')
    return inner_print()
```

使用`*`来定义接收任意个数参数的函数，例如`myfun(*args)`其中，`*`代表任意个数参数，args是一个tuple。其中args的数据类型可以为不同的。如果将一个list作为参数传递给一个函数，默认这个函数只接受了一个参数，可以通过在调用这个函数时，将list参数前增加`*`从而将list的每一个元素作为参数

```python
def show_fun(*args):
    for arg in args:
        print(arg)   
        
show_fun(1, 'one', 2, 'two')
# define a list 
args = [1, 'one', 2, 'two']    
show_fun(*args)
```

使用`**`来定义接收任意个数keyword的参数。`**`可以看作是将一个字典扩展为keys和values，通常使用`**kwargs`作为参数名称。通过在一个字典参数前增加`**`使得参数被当作多个参数传入函数

```python
def show_dict(**kwargs):
    for k, v in kwargs.items():
        print(k, v, sep='->', end=' ')
        
show_dict(a=10, b=20, c=60)
kwargs = {'a':10, 'b':20, 'c':60}
show_dict(**kwargs)
```

接收任意个数和任意类型的函数参数

```python
def show_any_args(*args, **kwargs):
    if args:
        for arg in args:
            print(arg)
    print()
    if kwargs:
        for k, v in kwargs.items():
            print(k, v, sep='->', end=' ')

show_any_args(a=10, b=20, c=60)
show_any_args(1, 2, 3)
show_any_args(1, 2, 3, a=10, b=20)
```



##### A decorator template code

```python
import functools import wraps

def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Code to execute before calling the decorated function.

        # 2. Call the decorated function as required, returning its results if needed.
        return func(*args, **kwargs)
        # 3. Code to execute Instead of calling the decorated function.

    return wrapper
```





###类

在Python中，习惯使用CamelCase来命名一个类，有全部小写来命名函数。Class behavior is shared by each of its objects, whereas state is not. Each object maintains its own state. 当一个类对象调用类的函数时，python解释器会将代码转为`ClassName.method(obj)`，例如c时`CountFromBy`的对象，执行`c.increase()`，实际执行的是`CountFromBy.increase(c)`,代码中可以直接以解释器的方式调用，但是没人那样用。由于解释器会将对象作为参数传入类的方法，因此在定义类方法时，必然会有一个参数self来指向对象自身。在方法中通过self可以方法对象的属性值。

子类从object类中继承的以双下划线开始的默认方法被称为"The magic methods"

```python
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

class FibIterator():
	"""docstring for FibIterator"""
	ins_count = 0;
	def __init__(self, max):
		super(FibIterator, self).__init__()
		self.max = max  # self.max 是实例变量，是一个对象实例中成员变量

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
print(fibIter.__class__)  # <class '__main__.FibIterator'>
print(fibIter.__doc__)  # docstring for FibIterator
for x in fibIter:
	print(x, end=" ")  # 0 1 1 2 3 5 8
```



#### Class Method

* `__init__(self, para)`，按照约定，这个是类中第一个定义的方法，同时也是对象创建后第一个执行的方法，和其他语言的构造方法不同，执行`__init__(self, para)`时，对象已经创建完成了。一般通过这个方法来初始化对象中的属性值，否则在其他方法中使用对象的属性值时，该属性还没有被初始化。

* 创建一个对象时，需要把`__init__(self, para)`需要的参数para传入

* 每一个类的成员方法的第一个参数都是对象的引用，self并不是python的保留字，只是一种约定的习惯，在方法定义的时候需要给出，但在调用时，python会默认传入对象的引用给第一个参数

* `__repr__(self)` specify how your objects are represented by the interpreter.

* 迭代器：定义了`__iter__()`方法的类，`__iter__()`方法返回定义了`__next__()`的类对象，可以是类自身对象也可以是其他任何迭代器对象，如果一个类中没有`__next__()`方法，则会报类型错误

* for 会自动调用iter()会执行`__iter__()`方法返回一个迭代器，然后循环调用`next()`方法，执行对象的`__next__()`

* 改变对象的属性值，不会影响类的属性值
  ```python
  fibIter = FibIterator(10)
  fibIt = FibIterator(100)
  fibIt.ins_count = 3  
  print(fibIter.__class__.ins_count)   # class still 0
  fibIt.__class__.ins_count = 6        # change the class value
  print(fibIter.__class__.ins_count)   # 6
  print(fibIter.ins_count)             # 6 use class's attribue
  print(fibIt.ins_count)               # fibIt's own ins_count override class's ins_count, so still 3
  ```


###断言

`assert 1 > 2, "1 bigger than 2 when in a game"` 

output:

`AssertionError: 1 bigger than 2 when in a game`

###迭代器
`itertools.permutations([1, 2, 3], 2) `
permutations() 函数接受一个序列(这里是 3 个数字组成的列表) 和一个表示你要的排列的元素的数目的数字。即1 2 3这三个数字两两排列的情况
`itertools.combinations('ABC', 2)`
itertools.combinations()函数返回包含给定序列的给定长度的所有组合的迭代器。

itertools.groupby()函数接受一个序列和一个 key 函数, 并且返回一个生成二元组的迭代器。每一个二元组包含
key_function(each item)的结果和另一个包含着所有共享这个key 结果的元素的迭代器。

迭代器没有“重置”按钮。你一旦耗尽了它，你没法重新开始。

* eval() 并不限于布尔表达式。它能处理任何Python表达式并且返回任何数据类型。但是这个执行表达式的方法，容易被黑客攻击，传入特殊的字符串表达式，从而执行他们想要的操作
  `print(eval('"A" + "B"'))  # AB`
  `eval('1 + 1 == 2') # True`
  `eval('["*"] * 5') # ['*', '*', '*', '*', '*']`
  `eval("pow(5, 2)") # 25`


### Database

#### Step of using database

1. Define your connections characteristics
2. Import your database driver
3. Establish a connection to the server
4. Open a cursor
5. Do the SQL thing.

```python
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
```

#### SQL Statement

* 查询一个表有多少行 `select count(*) from req_log;`

* 查询都有哪些浏览器 `select distinct browser from req_log;`

* 查询哪个浏览器使用的最多

  ```sql
  select  browser, count(browser) as 'count' 
  from req_log
  group by browser
  order by count desc
  limit 1;
  ```

  ​

### Standard Library

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

# get the current system
print(sys.platform)

import os
# get current path
print(os.getcwd())

# get system environment variables
print(os.environ)
# get value of a system environment variable
print(os.getenv('HOME'))

import datetime, time
# get today 
print(datetime.date.today())
# get current time in 24h format
print(time.strftime("%H:%M"))

import pprint
got = {'name':'GoT', 'producer':'HBO', 'lang':'eng'}
hoc = {'name':'House of Card', 'producer':'Netflix', 'lang':'eng'}
tvs = {}
tvs['got'] = got
tvs['hoc'] = hoc
pprint.pprint(tvs)
```

标准库中的`pprint()`方法可以将任何数据结构以更适合阅读的格式打印出来，例如`pprint(dict)`

#### Other Library

Pypi is [here](http://pypi.python.org)

### Flask

#### Web

Http  is stateless. Every web request is independent of what came before it, as well as what comes after. Http协议要求网络为无状态主要考虑性能问题。一个web服务器处理的工作可以最小化，这样当有大量的请求时，可以通过扩大服务器的规模来处理大量的请求。如果服务器要维护一系列请求之间的联系的话，会给服务器带来很大的资源消耗，不便于在多个服务器之间分散处理请求。Web服务器一般都被设计为可以快速应答，并快速忘记上次请求的机制，因为它不记录请求之间的状态。

不要将Webapp的状态保存在全局变量中，例如用户的登录信息，因为服务器可能在任何时候重新启动了webapp，导致之前保存的全局变量值被清空。

Session可以看作在无状态web之上的一层，通过将用户的认证信息存储在浏览器内的cookie中，并在服务端保存一份和这个cookie关联的session id。

Flask中提供了一个全局字典变量`session`，可以保存webapp的一些状态。Flask ensures that any data stored in session exists for the entire time your webapp runs (no matter how many times your web server loads and reloads your webapp code). Additionally, any data stored in session is keyed by a unique browser cookie, which ensures your session data is kept away from that of every other user of your webapp. From the webapp's perspective, it's as if there are multiple values of user in the session dictionary(keyed by cookie). From each browser's perspective, it's as if there is only ever one value of user (the one associated with their individual, unique cookie).

通过设置app.secret_key，Flask可以使用这个key字符串对发送到浏览器之前的cookie进行加密

Template engines let programmers apply the object-oriented notions of inheritance and reuse to the production of textual data, such as web pages. The template engine shipped with Flask is called Jinja2.

Flask comes with a function called `render_template` , which when provide with the name of a template and any required arguments, returns a string of HTML when invoked.

Flask comes with a built-in object called request that provides easy access to posted data. The request object contains a dictionary attribute called *form* that provides access to a HTML form's data posted from the browser.

Flask can associate more than one URL with a given function, which can reduce the need for redirections.

由于浏览器会自动解析带有`< >`标签的数据，因此如果要显示的数据中有tag标签时，需要将内容进行转义。Flask中提供了`escape()`函数将传入的字符串进行转义，escape返回的时一个Markup对象

Flask的`app.config` 是一个标准的Python字典，调用者可以将任何自己需要在webapp范围使用的配置存储在这个变量中。

A simple web app：

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, escape

app = Flask(__name__)

LOG_FILE = 'req_log.txt'

@app.route('/')
def home() ->'302':
    # redirect to the future page
    return redirect('/future')

@app.route('/f')
@app.route('/future') # GET method by default
def future_page():
    return render_template('future.html', the_title='Forsee the Future')

@app.route('/calc', methods=['POST']) # supports only the POST method
def calc_page() ->'html':
    month = int(request.form['month'])
    day = int(request.form['day'])
    result = get_constellation(month, day)
    log_req(request)
    return render_template('result.html', the_title='Your Future is here', result=result)

@app.route('/reqlog')
def show_log():
    contents = []
    with open(LOG_FILE) as logfile:
        for line in logfile:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote Addr', 'User Agent')
    return render_template('reqlog.html',
                            the_title = 'View Logs',
                            the_row_titles=titles,
                            the_data=contents,)

def log_req(req:'flask_request') -> None:
    with open(LOG_FILE, 'a') as logfile:
        print(req.form, req.remote_addr, req.user_agent, file=logfile, sep='|')

def letter_in_phrase(phrase: str, letters: str='aeiou') -> set:
    """Get the letters in the phrase"""
    return set(letters).intersection(set(phrase))

def get_constellation(month, day):
    days = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
    constellations = ('Capricorn', 'Aquarius', 'Pisces', 'Aries', 
        'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 
        'Scorpio', 'Sagittarius','Capricorn')
    if day < days[month-1]:
        return constellations[month-1]
    else:
        return constellations[month]

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
```



#### Jinja2

在Jinja2简单语法

* `{{ var_name }}` 来指出这个变量的值通过render传入的

* 定义一个块，这个块可以被继承子模板文件覆盖

  ```
  {% block block_name %}

  {% endblock %}
  ```

  ​

* 定义一个基类模板，可以套用到整个网站中

  ```html
  <!DOCTYPE html>
  <html>
  <head>
  	<title>{{ the_title }}</title>
  	<link rel="stylesheet" type="text/css" href="static/base.css">
  </head>
  <body>

  {% block body %} 
   
  {% endblock %}

  </body>
  </html>
  ```

  ​

* 一个子模板继承自基类模板，子类中body替换了基类模板中的body

  ```html
  {% extends 'base.html' %}

  {% block body %} 

  <h2>{{ the_title }}</h2>

  <form method="post" action="/calc">
  	<table>
  		<p>
  			Calculate the future of your life, please input your birthday:
  		</p>
  		<tr><td>Year:</td><td><input type="text" name="year" width="20"></td></tr>
  		<tr><td>Month:</td><td><input type="text" name="month" width="20"></td></tr>
  		<tr><td>Day:</td><td><input type="text" name="day" width="20"></td></tr>
  	</table>
  	<p>Click to see the future!</p>
  	<p><input type="submit" value="Go!" width="20"></p>
  </form>

  {% endblock %}
  ```

* 在Jinja中使用for循环语句，`the_data`是一个list的list

  ```html
  {% extends 'base.html' %}

  {% block body %} 

  <h2>{{ the_title }}</h2>

  <table>
  	<tr>
  		{% for row_title in the_row_titles %}
  			<th>{{ row_title }}</th>
  		{% endfor %}
  	</tr>
  	{% for log_row in the_data %}
  		<tr>
  		{% for item in log_row %}
  			<td>{{item}}</td>
  		{% endfor %}
  		</tr>
  	{% endfor %}
  </table>

  {% endblock %}
  ```

  ​

#### Publish Online

* PythonAnywhere [website](https://www.pythonanywhere.com/)

  可以将开发的Flask程序发布到PythonAnywhere上，有免费空间

  1. 点击到Web标签，创建一个flask web app，先不要点击reload按钮

  2. 切换到Files标签，将自己的webapp目录压缩为zip文件，将zip压缩包上传到根目录，对于依赖的第三方或自己的module包也可以将其tar.gz文件直接上传到根目录

  3. 点击`Open a bash console here`,打开一个bash终端

  4. 在终端中执行`python3 -m pip install your_private_module.tar.gz --user`来安装自定义的模块。注意最后有--user参数，因为PythonAnywhere只允许给当前用户安装模块

  5. 执行`unzip webapp.zip`解压工程到根目录，再执行`mv webapp/* mysite/`将工程文件拷贝到创建的web app目录中

  6. 在Web标签中，点击`WSGI configuration file`,在打开的文件中编辑最后一行的`flask_app` 为自己webapp的python模块名称，系统将主程序的app导入为application使用，记得点击保存

     ```python
     import sys

     # add your project directory to the sys.path
     project_home = u'/home/memorywalker/mysite'
     if project_home not in sys.path:
         sys.path = [project_home] + sys.path

     # import flask app but need to call it "application" for WSGI to work
     from webapp import app as application
     ```

  7. 回到Web标签，点击reload按钮，启动自己的应用程序，访问usrname.pythonanywhere.com可以看到自己的应用程序

#### Http

##### status code

codes: 100-199 are informational message: all is OK, and the sever is providing details related to the client's request.

codes: 200-299 are success messages: the server has received, understood and processed the client's request.

codes 300-399 are redirection messages: the sever is informing the client that the request can be handled elsewhere.

codes 400-499 are client error messages: the server received a request from the client that it does not understand and can't process.

codes in the 500-599 range are server error message: the server received a request from the client, but the server failed while trying to process it.

### 开发环境

#### virtualenv

通过一个独立的虚拟环境目录，来将不同的python隔离开来，可以把这个目录当作一个全新的安装
virtualenv 在2.6-3.4都可使用，默认安装了pip和easy_install
python 3.3以后系统内建了该功能pyvenv：

- windows上使用命令 python -m venv mydir  //创建mydir为根目录的python虚拟环境
  通过执行该目录下 mydir\Scripts\active     // 启动该虚拟环境
  通过执行该目录下 mydir\Scripts\deactive     // 退出该虚拟环境
  在该虚拟环境中可以像使用系统环境一样使用，只是安装依赖的库是独立于系统的
  在虚拟环境中安装模块  >pip install douban-client
- why use virtualenv?
  有些库程序需要vc编译环境，但是本机没有，只能到[地址](http://www.lfd.uci.edu/~gohlke/pythonlibs/)下载已经编译好的库程序文件.whl文件，而该文件只能通过pip安装，easy_install无法使用.因此在使用buildout时，只能悲剧的在全局系统python中安装了Pillow库。


通过编写requirements.txt，并执行pip install -r requirements.txt来安装依赖的所有库
通过在该环境下执行：`pip freeze > requirements.txt` 来导出该环境已经安装的依赖库，方便移植

- 在pycharm中使用virtualenv
  setting---Project Interpreter---齿轮图标---add local---选择自己已经创建好的虚拟环境中的python.exe
  不要使用pycharm来创建新的virtualenv(版本比较老，还不好用)

#### Buildout

Buildout is a python build system like 'Maven' for Java. 每一个python的工程有一套自己的编译环境，这样项目可以在不同的编译环境中独立运行。

[HomePage](http://www.buildout.org/en/latest/install.html)

##### Install

1. 每个工程独立安装。通过执行工程目录下的 `python bootstrap.py`(需要先创建一个空白的配置文件buildout.cfg，否则执行该语句会失败),这个buildout.cfg文件中不能有中文字符。
   例如本机的编码是cp936，这个文件就要是gbk格式的
   查看本机的编码：命令提示符下 chcp 
   python在使用open方法打开文件时，默认会使用系统默认编码（locale.getpreferredencoding() 这个方法的返回值）打开文件，如果这个文件是utf8的，就会提示gbk无法解码某个字符解码错误。
   在安装完buildout后，就可以修改buildout.
2. 安装到系统默认的python环境中，从而方便用来创建工程 `pip install zc.buildout` pip在python3.4中是默认安装的  
   然后，在需要使用buildout的工程根目录下执行 buildout init

- 对于系统中安装了多个python的环境，可以使用指定python版本的目录来生成当前工程需要的python解释器。例如
  `>D:\Python34\python.exe bootstrap-buildout.py` 则会使用3.4的python解释器生成buidout.exe，后续在配置依赖的库时，就会默认使用3.4版本的库程序。因为在编译时执行的\bin\buildout 可执行程序中已经包含了当前的python的版本信息以及系统python的目录，不需要再手动指向3.4python的系统目录了。

##### Directory

```
project/
   bootstrap.py  // should under version control
   buildout.cfg  // should under version control
   .installed.cfg
   parts/
   develop-eggs/
   bin/
       buildout
       mypython
   eggs/
   downloads/
```

- bulidout.cfg 编译的描述信息，包括依赖，目标结果等，类似makefile
- installed.cfg builout工具用来同步最新的工程描述信息
- parts/ recipe(食谱，方法，配方)用来安装或卸载part，开发者不需要更改
- develop-eggs/ 这个目录对应于编译描述文件中的`develop = DIRS`，里面是工程中用到的系统中其他程序的超链接，可以看作include路径
- bin/ 保存buildout生成的可执行脚本
- bin/mypython 一个python的解释器，包含了指定的parts，名字任意，而且可以有多个
- eggs/ 工程中使用的egg，可以多个工程公用
- downloads/ 下载的临时文件，可以公用

##### buildout.cfg

配置文件的最顶层是[buildout]段，ini格式的配置文件，以[]开始一个新段

```
[buildout]
develop = .
parts =
  test
  xprompt

[test]
recipe = zc.recipe.testrunner
eggs = xanalogica.tumbler

[xprompt]
recipe = zc.recipe.egg:scripts
interpreter = xprompt
eggs = xanalogica.tumbler
```

这个配置文件中有两个part，两个名字分别是test和xpromt，每一个part的名字是任意自定的，一些recipe会使用part的名字作为创建文件的前缀。每一个part描述段下的key=value都是在recipe在编译时传入的参数。例如recipe = zc.recipe.testrunner和eggs = xanalogica.tumbler

对应于xprompt段，说明了它需要一个名为xanalogica.tumbler的egg。 “interpreter =” 说明了使用一个名称为xprompt的解释器将这个egg映射到系统的path路径上。

“develop =” 设置buidout将当前目录下setup.py定义的egg也加入到当前的候选egg列表中，系统会默认优先使用当前本地的egg，而不是网络上的同名的egg。此处适用于开发模块的场景。

##### 另一个例子

```
[buildout]
# 每个buildout都要有一个parts列表，也可以为空。
# parts用来指定构建什么。如果parts中指定的段中还有parts的话，会递归构建。
parts = tools

[tools]
# 每一段都要指定一个recipe, recipe包含python的代码，用来安装这一段,
# zc.recipe.egg就是把一些把下面的egg安装到eggs目录中
recipe = zc.recipe.egg
# 定义python解释器
interpreter = python
# 需要安装的egg
eggs =
    pyramid # 依赖库pyramid
```

- 然后执行 bin\buildout.exe 来执行构建

##### 自定义解释器

```
[buildout]
parts =
  parse

[parse]
recipe = zc.recipe.egg:script
eggs = beautifulsoup4
interpreter = webpy  #指定使用解释器的名称
```

然后就可以使用bin\webpy作为工程独立的解释器，而不影响系统的python了

#### Ubuntu下使用python

Ubuntu16.04默认安装了python2.7.11和python3.5,系统目录下
/usr/bin/python ---2.7
/usr/bin/python3 ---3.5
安装pip
`$ sudo apt-get install python-pip`
但是使用pip 安装依赖包时，此时pip命令默认使用的时3.5的pip因此安装的依赖包都是3.5的，为了避免混乱还是最好使用virtualenv创建独立的python环境。
`$ sudo pip install virtualenv` 
此时由于pip时3.5的因此virtualenv默认创建的也是3.5版本的环境，这个信息可以通过
`virtualenv -h`
查看-p参数的描述
因此如果要创建一个2.7的环境，则可以使用`virtualenv -p=python2.7 virPy27`
激活虚拟环境使用
`~$ source virPy27/bin/activate`
此时终端状态变成了
`(virPy27) xxx@aquarius:~$ `
再次查看pip -V就可以看到pip的版本信息了。退出这个虚拟环境使用
`~$ deactivate`
卸载virtualenv
`$ sudo pip uninstall virtualenv`
卸载pip 
`$ sudo apt-get remove python-pip`