

# python study

### Start

REPL: read-eval-print-loop, describes an interactive programming tool that lets you experiment with snippets of code to your heart's desire.

`from module import function`, functions are inside modules which inside the standard library.  

*Python programmers prefer not to create the temporary variable unless it's needed at some point later in the program.*

Instead of referring to a code "block", Python programmers use the word "suite". Any suit can contain any number of embedded suites, which also have to be indented.

Most programmers configure editor to replace a tap of the *Tab* key with *four spaces*.

Python is object-based as opposed to purely object-oriented. 

Everything in python is an object, so anything can be assigned to a variable.

### Statement

#### Condition

```python
minute = datetime.datetime.today().minute

if minute > 30:
    print("later of hour")
elif minute == 30:
    print("half of hour")
else:
    print("first of hour")
```

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

元组是不可变的列表，速度比列表快，可以用作字典的key
可以使用元组作为函数的返回值，因为元组可以进行元素的一一赋值，如  
(a, b, c) = range(3)
a: 0
b: 1
c: 2

### 字典

Dictionary is an unordered set of key/value pairs. 字典是mutable

###集合

Set is an unordered set of unique objects.

集合中的元素没有重复的
* 统计字符串中出现的字母
  mystring = "How time flies!"
  print(set(mystring))  # {'m', 'e', '!', 'o', 'i', 's', 'f', 'w', ' ', 'l', 't', 'H'}

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

* rstrip() 字符串方法移除每一行尾部的空白
* lstrip() 方法移除头部的空白
* strip() 方法头尾都移除

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

###with
```python
with open("pythonstudy.py", encoding="utf-8") as demofile:
	for line in demofile:
		print(line)
```

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


###类

```python
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

* __init__(self, para)，按照约定，这个是类中第一个定义的方法，同时也是对象创建后第一个执行的方法，和其他语言的构造方法不同，执行__init__(self, para)时，对象已经创建完成了。
* 创建一个对象时，需要把__init__(self, para)需要的参数para传入
* 每一个类的成员方法的第一个参数都是对象的引用，self并不是python的保留字，只是一种约定的习惯，在方法定义的时候需要给出，但在调用时，python会默认传入对象的引用给第一个参数
* 迭代器：定义了__iter__()方法的类，__iter__()方法返回定义了__next__()的类对象，可以是类自身对象也可以是其他任何迭代器对象，如果一个类中没有__next__()方法，则会报类型错误
* for 会自动调用iter()会执行__iter__()方法返回一个迭代器，然后循环调用next()方法，执行对象的__next__()
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
```

#### Other Library

Pypi is [here](http://pypi.python.org)



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