###Dive into python 3

#####Basic knowledge

#####系统
* import路径：sys.path中的所有目录，类似C++默认的include，通过print(sys.path)查看该列表
* sys.path.insert(0, new_path) 插入一个新的目录到sys.path列表的第一项，从而在python搜索目录的的开头可以先搜索自己添加的目录，进而屏蔽python自带的一些库。
* python中所有的内容都是对象，包括函数
* 当import了一个模块后可以使用 模块名.方法名等方式调用模块中的方法
* python中所有的变量必须赋值，不能仅仅只是声明
* 所有的东西都区分大小写

#####模块
* 一个py文件就是一个模块，所有的模块也是对象，每个模块有个默认的属性__name

#####函数

* 参数在传递时，可以使用参数名=参数值的方式传入，因此没有顺序，这种传入参数的方法称作命名参数，在命名参数的右侧所有参数也必须是命名参数。
* 在方法定义的第一行使用'''方法说明'''，来编写方法的文档。通过 函数名.__doc__可以查看函数的这个说明信息


#####异常
* 使用try...except...来处理异常，使用raise来抛出异常，例如：raise ValueError("non-zero value is accepted.")
* 捕获导入错误
	当导入的模块不再系统import的目录时，需要做一些异常判断或者使用不同的库进行替代，这个时候可以使用try...except来实现
    ```
    try:
    	import chardet
    except ImportError:
    	chardet = None
        
    if chardet:
        # do something
	else:
		# continue anyway
    ```
    或者根据不同的库使用相同的导入名称，例如：
    ```
    try:
		from lxml import etree
	except ImportError:
		import xml.etree.ElementTree as etree
    ```
    当用户没有安装第三方的库lxml时，使用系统自带的xml库，但导入的名字都是etree，这样程序的代码就可以使用etree中的公共api