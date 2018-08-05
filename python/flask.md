###Flask Document

####Install
* make an independent python environment
`virtualenv ~/py3.5`
active the environment
`source ~/py3.5/bin/activate`
In the same terminal `(py35) edison@aquarius:~/py35$ ` change to the project's path
`(py35) edison@aquarius:~/py35$ cd /media/edison/data/code/python/flaskstudy/`

* Install flask
`pip install Flask`

####Quick Start

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```

####Flask Web Development
当客户端给应用发送一个请求时，flask会产生一个request请求对象，这个对象中封装了http请求的信息，应用程序的请求处理函数中接收这个对象，然后相应处理用户的请求。但是这样会导致所有的请求处理函数都要有个request参数，如果一个处理函数还需要其他参数，就会非常混乱。
Flask中使用了Context让一些确定的变量在一个线程的范围内是全局可访问的，request就是其中一个，这样request就不用通过参数传人每一个处理函数中。（web服务器每次处理一个请求时，都会从当前的线程池中取出一个线程来处理这个请求，在一个线程中执行的指令是顺序的）
Flask中有两种Contexts：application context and request context
* application context中有两个全局变量
    1. current_app:当前活动application的实例
    2. g:可以用来临时存储数据的全局变量，每一次请求这个变量都会重置
* request context中有两个全局变量
    1. request:封装的http请求的全部信息对象
    2. session:字典，保存用户会话之间的数值信息，下次请求，上次设置的值还会传过来
Flask在派发一个客户端请求之前激活application context and request context，在请求处理后删除他们。当一个上下文出入激活状态时，这个上下文中的变量在当前线程中就是全局可用的，否则会出现访问错误。

Flask使用了一个map保存了url地址和对应的处理函数，通过`app.url_map`可以查看当前app的所有映射表。可以使用`app.route decorators`或`app.add_url_rule()`来注册一个映射

Flask提供了Hook的方式在一个请求前或后执行一些操作，这些hook通过decorator的方式提供。例如可以在`@before_first_request`装饰器修饰的函数中初始化数据库，获取一个用户信息表，将这个用户信息通过g.user传递给后续的request中使用。

在处理函数中使用`make_response()`函数来创建一个Response对象，这个对象可以设置状态码和cookie
    ```
    @app.route('/time')
    def showTime():
        response = make_response(datetime.datetime.now().strftime("%Y-%m-%d %H:%S:%M"))
        response.set_cookie('time',str(1))
        return response
    ```
####模板
如果直接在一个view的request处理函数中返回应答的html页面字符串信息会使业务逻辑和显示逻辑混合在一起。因此可以使用模板，模板中存在一些占位符，应用程序中将变量传入模板实现显示内容。

Flask使用Jinja2作为模板引擎。Jinja在日语中是神社的意思。

####扩展
#####flask-bootstrap
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

