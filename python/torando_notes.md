##Tornado tutorial

Tornado 实现了异步非阻塞网络，适用于长期轮巡，websockets以及每一个用户需要一个长链接的场景。

主要分为4个组件：
1. A web framework (including RequestHandler which is subclassed to create web applications, and various supporting classes).
2. Client- and server-side implementions of HTTP (HTTPServer and AsyncHTTPClient).
3. An asynchronous networking library including the classes IOLoop and IOStream, which serve as the building blocks for the HTTP components and can also be used to implement other protocols.
4.A coroutine library (tornado.gen) which allows asynchronous code to be written in a more straightforward way than chaining callbacks.

一般网络程序中用户与web服务之间时长链接，传统的同步模式的服务会给每一个用户分配一个线程，这样的代价很高。Tornado中使用了单线程的事件循环机制，因此使用tornado的代码必须都是异步和非阻塞的，因为单线程一次只能执行一个操作。

* 阻塞：一个函数直到它等待的事件发生时才返回。等待的事件可能为网络IO,磁盘IO，互斥锁等。一个极端例子bcrypt库使用了几百毫秒的cpu时间，此时其他程序都会处于阻塞状态。一个函数在不同的配置情况下，可以为阻塞也可以为非阻塞。
* 异步：一个函数在执行完成之前就返回了，通常还有一些任务是在后台线程完成的。异步接口有多种：
1. Callback argument，将一个回调函数作为参数传入，实际任务完成后回调该函数
2. Return a placeholder (Future, Promise, Deferred)
3. Deliver to a queue
4. Callback registry (e.g. POSIX signals)
无论使用那种方式，都没有一个简便的方法将一个同步函数以异步的方式执行，同时对于调用者还是透明的。

###Coroutines
协程，可以将它看成一个用户态的线程（一般来它也提供了入口函数、调用的参数，以及你放置局部变量的栈），只不过它是你自己调度的，而且不同coroutine的切换不需要陷入内核态，效率比较高。
linux有提供了getcontext swapcontext等接口来实现coroutine，windows貌似也有相关的。一般来说coroutine用在异步的场景比较好，异步执行一般需要维护一个状态机，状态的维护需要保存在全局里或者你传进来的参数来，因为每一个状态回调都会重新被调用。有了coroutine(stackfull)的话你可以不用担心这个问题，你可以像写同步的代码那样子，但其实底层还是异步的，只不过你在等待数据时执行的上下文会暂时被保存起来，等到数据来临再将上下文恢复继续执行。还有一种coroutine是stackless，它本质上也是状态机实现的，并不能在它上面让不同的状态共享局部变量，貌似boost.asio.coroutine就是这种。
协程是函数基础上，一种更加宽泛定义的计算机程序模块(函数可以看做协程的特例)，它可以有多个入口点，允许从一个入口点，执行到下一个入口点之前暂停，保存执行状态，等到合适的时机恢复执行状态，从下一个入口点重新开始执行，这也是协程应该具有的能力。

协程代码块：一个入口点和下一个入口点(或者退出点)中的代码。
协程模块:由n个入口点代码，和n个协程代码块组成。第一个入口点通常是一个函数入口点。其组织形式如：函数入口点->协程代码块->入口点->协程代码块…，入口点和代码块相间。

生成器是一个含有yield表达式的函数，此时该函数叫生成器。一个生成器永远是异步的，即使生成器模块中含有阻塞代码。因为调用一个生成器，生成器的参数会绑定到生成器，结果返回是一个生成器对象，它的类型是types.GeneratorType，不会去执行生成器主模块中的代码。

在pep342中，对Generator进一步加强，增加了GeneratorType的send方法，和yield表达式语义。yield表达式，可以作为等号右边的表达式。如果对Generator调用send(None)方法，生成器函数会从开始一直执行到yield表达式。那么下一次对Generator调用send(argument),Generator恢复执行。那么可以在生成器函数体内获得这个argument，这个argument将会作为yield表达式的返回值。




