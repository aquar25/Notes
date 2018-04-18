## The art of Readable Code##

代码要容易理解，最好能让其他人可以用最少的时间理解你的代码。

可读的标准：以别人阅读理解你的代码的时间作为衡量代码可读性的标准，我们的目标是减小这个时间。`Time-Till-Understanding`

理解的标准：别人能够有效的更改你的代码，或者指出代码中的bug，明白你的代码是怎么和系统中的其他代码交互的。

别人：其他同事，6个月之后的你自己

理论上，代码越少，理解代码所用的时间也就越少，和读书类似，所以这本书就很少吧。但是，这不是绝对的，一些被简化的逻辑，如果写的时候优化了原来复杂的逻辑，直接看懂就会花费很长时间。这时加上一句简单的注释就可以提高很多效率。

代码可读的基本准则高于本书中的其他所有原则。

### 表面上的改进

#### 见名知意

* 选择具体的/明确的词，例如使用`DownloadPage()`，而不是宽泛的`GetPage()`。要根据功能的具体特点取名字，可以区分这个函数的功能和其他的特别之处。也可以选择使用行业相关的专业词汇。英语词汇量是个问题。
* 使用更有表现力的词汇。可以通过在词典中找同义词的方法。
  * send: deliver, dispatch, announce, distribute, route
  * find: search, extract, locate, recover
  * start: launch, create, begin, open
  * make: create, setup, build, generate, compose, add, new, fill
* 使用具体的名字名字来描述事物，清晰明确的词汇比卡哇伊/空洞的词汇好。
* 给变量名带上必须的细节，循环变量可以加前缀区分是用来遍历哪个数据
* 名字优先表达实际作用，其次时使用场景，因为使用场景可能有多种
* 名字附带有效的关键信息，例如单位(time_s)/数据类型(p)/格式(utf8)
* 作用域大的名字要更具体，作用域小的可以简短的名字
* 利用名字的格式来传递含义。遵守统一的命名规范。CameCase标识类名，lower_separated表示变量名。名字格式使用大小写或下划线分隔，或者表示一种类型的变量，例如成员/静态/常量
* 如果要缩写，要用业内公认的缩写方式，例如str，doc，而且每种语言也不同

#### 避免歧义

* 起一个名字时，反问自己别人是否能理解这个名字，是否会联想到其他含义。可能自己的词汇量匮乏，对一个单词只了解一个意思，而其他人知道更多的含义。尽量不用单词的生僻含义。
* 动词作为方法名时，加上宾语可以更明确的表达一个行为的结果
* 边界值使用max和min的修饰，用first和last标识范围，明确范围的开闭区间，对于开闭区间[ )使用begin和end的组合，和STL的一致
* bool变量加上is/has/can/should前缀，明确条件是什么，避免使用正常逻辑的反义，例如XXXNoSignal
* 坚持一个语言的命名风格，例如get和set对于java bean都是访问函数，大家都知道里面不会有复杂的运算，因此可多次调用。list的size()函数原来实现是遍历链表获取个数O(N)，如果用作循环变量中就会严重影响效率了(最新的标准库实现为O(1))。

美化代码

* 一致的布局，等宽字体列对齐，注释也要对齐
* 相似的代码看上去相似，重复的代码用一个公共函数统一实现
* 相关的代码分块放一起形成一个段落，每个段落一个注释
* 变量和函数的声明的顺序：与界面显示或其他地方的定义一致，重要到不重要，字母顺序（没有必要）
* 一致的风格比正确的风格更重要