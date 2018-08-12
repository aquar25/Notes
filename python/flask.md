### Flask Document

#### Install

* make an independent python environment
`virtualenv ~/py3.5`
active the environment
`source ~/py3.5/bin/activate`
In the same terminal `(py35) edison@aquarius:~/py35$ ` change to the project's path
`(py35) edison@aquarius:~/py35$ cd /media/edison/data/code/python/flaskstudy/`

* Install flask
`pip install Flask`

#### Quick Start

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

### Flask基本构成

#### 请求调度-路由

Flask中使用装饰器来指出一个路由的地址和其处理函数。例如可以使用路由中的动态参数传递参数给处理函数。

```python
@app.route('/love/<name>') # name 作为参数通过地址http://127.0.0.1:5000/love/you 传入
def love_handle(name):
    return '<h1>Robot love %s !</h1>' % name # 输出 Robot love you !
```

使用`app.url_map`可以获取当前应用中的所有路由映射。

```python
if __name__ == '__main__':
    print(app.url_map)
    app.run('0.0.0.0', debug=True)
```

输出的日志如下

```
Map([<Rule '/browser' (GET, OPTIONS, HEAD) -> browser>,
 <Rule '/' (GET, OPTIONS, HEAD) -> home>,
 <Rule '/static/<filename>' (GET, OPTIONS, HEAD) -> static>,
 <Rule '/love/<name>' (GET, OPTIONS, HEAD) -> love_handle>])
```

#### 应用与请求上下文

当客户端给Flask应用发送一个请求时，flask会产生一个request请求对象，这个对象中封装了http请求的信息，应用程序的请求处理函数中接收这个对象，然后相应处理用户的请求。

但是这样会导致所有的请求处理函数都要有个`request`参数，如果一个处理函数还需要其他参数，就会非常混乱。
Flask中使用`Context`临时的把某些对象变为在一个线程的范围内是全局可访问的，`request`就是其中一个，这样`request`就不用通过参数传人每一个处理函数中。（web服务器每次处理一个请求时，都会从当前的线程池中取出一个线程来处理这个请求，在一个线程中执行的指令是顺序的）

例如：

```python
@app.route('/browser')
def browser():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
```

其中`request`直接作为一个变量使用了。

Flask中有两种Contexts：`application context` and `request context`

* `application context`中有两个全局变量
    1. `current_app`:当前活动application的实例
    2. `g`:处理请求时可以用来临时存储数据的全局对象，每一次请求这个变量都会重置
* `request context`中有两个全局变量
    1. request:封装的http请求的全部信息对象
    2. session:字典，保存用户会话之间的数值信息，下次请求，上次设置的值还会传过来

Flask在派发一个客户端请求之前激活（或推送）application context and request context，在请求处理后删除他们。当一个应用上下文被推送后，application context中的`current_app`和`g`在当前线程中就是全局可用的，否则会出现访问错误。同理，`request context`在一次请求中的两个对象是全局有效的。

Flask使用了一个map保存了url地址和对应的处理函数，通过`app.url_map`可以查看当前app的所有映射表。可以使用`app.route decorators`或`app.add_url_rule()`来注册一个映射

Flask提供了Hook的方式在一个请求前或后执行一些操作，这些hook通过decorator的方式提供。例如可以在`@before_first_request`装饰器修饰的函数中初始化数据库，获取一个用户信息表，将这个用户信息通过g.user传递给后续的request中使用。

在一个应用程序对象上调用`app.app_context()`可以获得一个应用程序上下文。

#### 请求钩子(Request Hooks)

有时需要在处理一个请求之前或之后做一些其他公共的操作。例如处理请求前验证用户的权限。Flask支持在视图函数处理之前或之后注册一个通用函数执行某些额外操作。

请求钩子通过装饰器实现。目前有以下几种钩子：

* `before_first_request`注册一个函数在请求第一次被执行前调用
* `before_request`注册一个函数在每次请求前调用
* `after_request`注册一个函数，如果没有未处理异常，则在每次请求之后调用，
* `teardown_request`注册一个函数，即使有未处理的异常，也在每次请求之后调用

钩子函数和视图函数之间使用全局变量`g`来共享数据。

#### 响应对象

视图函数处理完请求后，会把结果作为一个HTML页面应答给客户端。HTTP应答除了HTML页面还需要状态码例如404、500等。例如可以应答400给客户端，表明这是个错误请求。

```python
@app.route('/love/<name>')
def love_handle(name):
    return '<h1>Robot love %s !</h1>' % name, 400
```

在处理函数中使用`make_response()`函数来创建一个Response对象，这个对象可以设置状态码和cookie以及一些其他的响应属性。

```python
@app.route('/time')
def showTime():
    response = make_response(datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M"))
    response.set_cookie('time',str(1))
    return response
```

##### 重定向响应

重定向的状态码为302，使用`redirect()`转到对应的地址`redirect('http://www.example.com')    `

##### 错误请求响应

```python
from flask import abort

@app.route('/bad')
def bad_handle():
    abort(404)
```

`abort`函数会直接返回应答，它后面的代码不会被执行。


### 模板

如果直接在一个view的request处理函数中返回应答的html页面字符串信息会使业务逻辑和显示逻辑混合在一起。因此可以使用模板，模板中存在一些占位符，应用程序中将变量传入模板实现显示内容。

Flask使用Jinja2作为模板引擎。Jinja在日语中是神社的意思。

默认情况下，Flask在程序文件夹的templates子目录中寻找模板。

模板文件中主要是html代码的框架，其中可以传递变量和使用模板继承

一个基模板，其中`{{ the_title }}`为模版使用的变量，`{% block body %}和`{% endblock %}`之间为模板定义的代码块，由继承该模板的子模板实现填充

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

一个继承基模板的子模板，其中需要定义代码块实现基模板中的代码块

```html
{% extends 'base.html' %}  <!-- 继承哪个模板 -->

{% block body %}   <!-- 自己实现一个基模板中的代码块 -->

<h2>{{ the_title }}</h2>

<p> video link is:</p>

<video width="320" height="240" controls>
  <source src={{ result }} type="video/mp4">
</video>

{% endblock %} <!-- 代码块结束 -->
```

在视图处理函数中使用模板，只需要把**模板文件名**和**参数**传入

```python
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)  # name为给模板传递的参数
```

Jinja2模板是独立的一个模板引擎，他的内容是另一个库的功能，这里只记录简单常用的。

#### 模板变量

变量支持使用字典、列表和对象

```html
<p>A value from a dictionary: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
<p>A value from an object's method: {{ myobj.somemethod() }}.</p>
```

##### 过滤器

可以使用过滤器修改变量，过滤器在变量名称后用`|`分隔。`Hello, {{ name|capitalize }}`使用首字母大写name变量的值。

常用的过滤器：

* safe  渲染值时不转义（需要显示html的tag时使用，对于用户输入的内容不要用，避免被sql注入或恶意代码）
* capitalize 首字母大写
* lower 换为小写
* upper 换为大写
* trim 去掉首尾空格
* title 每个单词的首字母大写
* striptags 渲染之前把值中所有的HTML标签都删掉

##### 控制结构

* 条件判断

```html
{% if user %}
    Hello, {{ user }}!
{% else %}
    Hello, Stranger!
{% endif %}
```

循环语句

```html
<ul>
	{% for comment in comments %}
		<li>{{ comment }}</li>
	{% endfor %}
</ul>
```

##### 宏

宏类似函数可以被其他代码调用

```python
{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}
```

可以把宏定义到一个文件中，在其他模板中引入

```
{% import 'macros.html' as macros %}
<ul>
    {% for comment in comments %}
        {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>
```

对于多处重复使用的模板代码片段可以写入单独的文件中，再包含在所有的模板里

`{% include 'common.html' %}    `

#### 链接

直接在模板中使用路由的链接会产生依赖，导致后续更改复杂，如果python视图处理函数的路由改变，模板也需要改变。Flask提供了`url_for()`函数使程序URL映射中保存的信息生成URL。

`url_for('index', _external=True)`得到index这个视图处理函数名或端点名，第二个参数生成绝对地址。

`url_for('user', name='john' _external=True)`第二个参数是函数的参数，对应的地址为`/user/john`

`url_for('index', page=2)`使用额外的参数page，得到地址为`/?page=2`

#### 静态文件

默认下，Flask在程序根目录的static的子目录中查找静态文件。放在其他目录中的图片、视频都是无法访问到的。例如在`static/css/styles.css`放的样式表文件。

在head中定义网站的图标

```html
<head>
{% block head %}
<title>{% block title %} {% endblock %} {{ the_title }}</title>

<link rel="stylesheet" type="text/css" href="static/base.css">
<link rel="shortcut icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">
<link rel="icon" href="{{ url_for('static', filename = 'favicon.ico') }}" type="image/x-icon">

{% endblock %}
</head>
```



### 扩展

Flask支持用户选择不同的扩展来简化开发过程。例如它自身不支持数据库处理用户可以根据自己需要选择合适的扩展或自定义扩展，自由度更高。

##### flask-bootstrap

由于程序默认使用的资源是cloudflare这个cdn上的，过问访问比较慢，因此需要修改模块的初始化文件中默认值路径`/<venv>/lib/python3.5/site-packages/flask_bootstrap/__init__.py`，修改为下面地址`http://www.bootcdn.cn/`

```
        bootstrap = lwrap(
            WebCDN('//cdn.bootcss.com/bootstrap/%s/' %
                   BOOTSTRAP_VERSION), local)

        jquery = lwrap(
            WebCDN('//cdn.bootcss.com/jquery/%s/' %
                   JQUERY_VERSION), local)

        html5shiv = lwrap(
            WebCDN('//cdn.bootcss.com/html5shiv/%s/' %
                   HTML5SHIV_VERSION))

        respondjs = lwrap(
            WebCDN('//cdn.bootcss.com/respond.js/%s/' %
                   RESPONDJS_VERSION))
```

### 数据库

ORM(Object-Relational Mapper)或ODM(Oject-Document Mapper)数据库抽象层库有`SQLAlchemy`和`MongoEngine`，这些库可以直接处理Python对象，而不用处理表、查询语言。



### 应用程序项目结构

项目的结构没有固定的标准，方便维护和扩展即可

![flask_dir](./images/flask_dir.png)

4个顶层目录是：

* app Flask的应用程序
* migrations 数据库的迁移脚本
* tests 单元测试
* venv Python的虚拟环境

根目录还有几个文件

* requirements.txt 工程依赖的python包定义在这里。使用`pip freeze > requirements.txt`生成。在新的虚拟环境中运行`pip install -r requirements.txt`来安装所依赖的库。
* config.py 存储配置设置
* manage.py 启动应用程序和其他应用任务

#### 配置选项

使用不同的配置把开发、测试和 生产环境隔离开。

配置文件模板如下

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    """docstring for Config"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

    def __init__(self, arg):
        super(Config, self).__init__()
        self.arg = arg
        
class DevelopmentConfig(Config):
    """docstring for DevelopmentConfig"""
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestConfig(Config):
    """docstring for DevelopmentConfig"""
    TESTING = True    
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        

class ProductionConfig(Config):
    """docstring for DevelopmentConfig"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
```

基类中定义通用配置，子类定义专用配置。`init_app()`方法的参数是程序实例。其中可以对当前环境的配置初始化。最后使用字典注册了不同类型的配置环境。方便以后直接引用。

#### 程序包

其中app放程序的核心实现。

##### 使用程序工厂函数

如果在单个文件中开发程序，应用实例在全局作用域创建，无法动态更改配置，执行这个文件时，程序实例已经创建。因此有时需要延迟程序实例的创建。工厂函数在程序包app的构造文件`__init__.py`中定义。

构造文件导入了大多数正在使用的Flask扩展，由于尚未初始化所需的程序实例，所以没有初始化扩展。`create_app`是程序的工厂函数，接受一个参数，是程序使用的配置名。配置类在config.py中定义，其中保存的配置可以使用Flask `app.config`配置对象提供的`from_object()`方法直接导入程序。程序创建并配置好后，就能初始化扩展了。在扩展对象上调用`init_app()`可以完成初始化过程。

```python
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])    
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 附加路由和自定义的错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
```



##### 使用蓝图

使用单个脚本的程序可以直接使用全局的app对象使用`app.route`装饰器来定义路由，而使用初始化脚本的方式只有调用了`create_app()`之后才能使用`app.route`装饰器，这时定义路由太晚了。

使用蓝图也可以定义路由，只是在其中定义的路由处于休眠状态，直到蓝图注册到程序之后，路由才成为程序的一部分。蓝图可以在单个文件中定义，也可使用结构化的方式在包中的多个模块中创建。本书在`app/main/`这个目录下创建蓝图。

蓝图的构造文件在`app/main/__init__.py`

```python
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
```

通过实例化一个Blueprint类对象创建蓝图。第一个参数为蓝图的名称，第二个为蓝图所在包或模块。

程序的路由保存在`app/main/views.py`模块中，而错误处理程序保存在``app/main/errors.py``中。导入这两个模块把路由和错误处理程序关联起来。导入必须写在蓝图构造文件的末尾，避免循环导入依赖。将创建好的蓝图在app的构造中注册到app。`app.register_blueprint(main_blueprint)`

而在main包中定义的视图处理模块中使用蓝图来定义路由`app/main/views.py`，其中使用蓝图main来作为装饰器。蓝图会在所有的端点上加一个命名空间，这样在不同的蓝图中可以定义相同的视图处理函数而不会冲突。命名空间就是蓝图的名称。所以视图函数index的地址使用`url_for('main.index')`获取。如果命名空间是当前请求所在的蓝图，在可以使用`.`来代替当前的蓝图名称。

```python
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('index.html', 
                            form=form, name=session.get('name'),
                            known=session.get('known', False),
                            current_time=datetime.utcnow())
```

错误处理程序``app/main/errors.py``

```python
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

蓝图中使用`errorhandler`装饰器只有蓝图中的错误才能触发处理程序，注册程序的全局错误处理程序，必须使用`app_errorhandler`

#### 启动脚本

根目录的`manage.py`用于启动程序。

```python
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

启动程序时，执行`python manage.py`

#### 单元测试

在tests目录中是单元测试文件。

```python
import unittest
from flask import current_app
from app import current_app, db

class BasicTestCase(unittest.TestCase):
    """docstring for BasicTestCase"""
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
```

setUp方法创建测试环境，在tearDown方法中释放资源恢复状态。

在manage.py中可以增加一个命令用来执行单元测试。

```python
@manager.command
def test():
    '''unittest help info'''
    import unittests
    tests = unittests.TestLoader().discover('tests')
    unittests.TextTestRunner(verbosity=2).run(tests)
```

其中修饰函数名就是命令名，函数的文档字符串会显示在帮助信息中。执行命令`python manage.py test`