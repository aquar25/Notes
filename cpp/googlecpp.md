###Head File
* #define 保护 `<PROJECT>_<PATH>_<FILE>_H_`
```
#ifndef BASEITEM_H
#define BASEITEM_H
// code

#endif // BASEITEM_H
```

* 使用前置声明（forward declarations）尽量减少.h 文件中#include 的数量
在头文件如何做到使用类Foo而无需访问类的定义？(只有这种情况才能使用声明的方法，而不用引入头文件)
1) 将数据成员类型声明为 Foo * 或 Foo &；
2) 参数、返回值类型为 Foo 的函数叧是声明(但不定义实现)
3) 静态数据成员的类型可以被声明为Foo，因为静态数据成员的定义在类定义之外。
另一方面，如果你的类是 Foo 的子类，戒者吨有类型为 Foo 的非静态数据成员，则必须为乊包吨头文件。
有时使用指针成员替代对象成员的确更有意义，如果只是为了减少包含头文件，还是不要这样替代，因为使用指针的方式会降低代码的可读性和执行效率。

* 不要内联超过10行的函数，对于析构函数需要慎重，因为一些隐式成员和基类的析构函数会被调用，其实很长
* 复杂内联函数的定义应放在后缀名为-inl.h的头文件中
* 函数参数顺序：输入参数在前，输出参数在后，即使是追加新的参数也要保持这个原则
* 头文件顺序：
    1. cpp文件对应的头文件
    2. C系统文件
    3. C++系统文件
    4. 其他库头文件
    5. 本项目内头文件
    
###Scope
* 在.cc文件中，允许甚至提倡使用不具名的命名空间，避免运行时的命名冲突，不能在.h文件中使用不具名的命名空间 
```
namespace {
// namespace中的内容不缩进
enum ALGIN { RIGHT, LEFT, MIDLE};
ALGIN algin() { return RIGHT;};

} // namespace
```
* 命名空间将除文件包含/全局标识的声明/定义以及类的前置声明外的整个源文件封装起来，以同其他命名空间相区分
* 最好不要使用using指示符，以保证命名空间下的所有名称都可以正常使用
* 在.cc文件、.h文件的函数、方法或类中，可以使用using，这条原则同样适用于命名空间别名例如`namespace fbz=::foo::bar::baz`
* 嵌套类是定义在另一个类中的类，不要将嵌套类定义为public，除非它是接口的一部分，比如某个方法使用了这个嵌套类的一系列选项
```
class Container
{
// 嵌套类声明
private:
    class Transformer
    {

    public:
        Transformer();
        ~Transformer();

        void transform(BaseItem* item);
    };

public:
    Container();
    ~Container();

    void addItem(BaseItem* item);
    void doTransform();

private:
    std::vector<BaseItem* > m_vItems;
    Transformer m_transformer;
};
```

* 使用命名空间中的非成员函数或静态成员函数，尽量不要使用全局函数，否则容易出现函数名称相同，重定义的情况
* 将非成员函数和静态类成员函数作为新类的成员或许更有意义，当它们需要访问外部资源或具有重要依赖时更是如此。相比单纯为了封装若干个不共享任何静态数据的静态成员函数而创建类，不如使用命名空间。
* 如果定义的非成员函数只是在.cc文件中使用，可以使用不具名命名空间或static(static int Foo())限定其作用域
* 对于局部变量，在尽可能小的作用域中声明变量，离第一次使用越近越好，易于阅读。使用初始化的方式代替先声明再赋值的方式。
* 如果变量是一个对象，需要考虑每次进入和退出作用域时，调用其构造和析构的代价。
* class类型(包括stl中的vector，string)的全局变量是禁止的（全局变量的构造函数、析构函数、以及初始化操作的调用顺序只是被部分规定，每次生成都会有变化，从而导致难以发现的bug），只允许内建类型和由内建类型构成的没有构造函数的结构体定义的全局变量；多线程中非常数的全局变量也是被禁止的。永远不要使用函数的返回值初始化全局变量。
* 如果一定要用全局的类对象，可以使用singleton pattern
* 使用C风格的字符串全局变量，不要使用stl中的string全局字符串`const char key[] = "MOMS_CAT";`
* 大多数的全局变量应该是类的静态数据成员，或者当其在cc文件范围内使用时，将其定义到不具名命名空间中或使用静态static来限制它的作用域
* 静态成员变革两视作全局变量，所以也不能是class类型

###class
* 构造函数中只处理没有意义的初始化，实际的初始化工作单独放到Init()函数中。构造函数中不能进行太多工作的原因：
1. 不易报告错误，不能使用异常
2. 操作失败导致对象初始化构造失败，处于不确定状态
3. 构造函数中调用虚函数，调用不会派发到子类实现中
4. 如果由地方定义了全局的类对象，由于在main之前执行构造函数，会导致一下初始化条件不正确

* 如果一个类中定义了成员变量，一定要定义一个默认构造函数，否则系统自动生成的默认构造函数不会初始化成员变量
* 在但参数的构造函数前增加explicit修饰，避免造成不必要的隐式类型转换，拷贝构造函数不需要声明为显示
* 仅在代码中需要拷贝一个类对象时使用拷贝构造函数(对象进行值传递，以及stl容器要求所有内容可以拷贝和赋值)；不需要时使用DISALLOW_COPY_AND_ASSIGN，大部分的类不需要拷贝和赋值操作，引用传递效率要高很多。当使用stl容器时，可以考虑使用std::tr1::shared_ptr，使用指针指向stl容器中的对象
```
#define DISALLOW_COPY_AND_ASSIGN(TypeName) \
    TypeName(const TypeName&); \
    void operator=(const TypeName&)
    
// 在类的声明中，private声明拷贝构造和赋值
private:
    DISALLOW_COPY_AND_ASSIGN(Container);
```
* 使用组合通常比继承更合适，如果要使用继承的话，只使用public继承
* 尽管父类中已经声明了多态函数为virtual，在子类该函数的声明中还是要加上virtual，便于阅读
* 只有当所有基类除第一个外都是纯接口时才能使用多重继承。为确保它们是纯接口，这些类必须以Interface为后缀
* 一般不要重载操作符，尤其是赋值操作。如果需要的话可以定义Equals()/CopyFrom等函数。不要仅仅因为stl容器操作就重载==或operator<，取而代之，应该在声明容器的时候创建相等判断和大小比较的仿函数类型。有些stl算法确实需要重载==时，可以这么做，但需要提供文档说明原因
* 成员变量一定要私有化，并提供对应的get和set
* public在private之前，成员函数在成员变量之前
* 函数如果超过40行，可以考虑在不影响程序结构的情况下将其分割一下
* 任何情况下都不要使用auto_ptr,如果要使用智能指针的话，使用scoped_ptr，对于stl容器中的对象，应只使用std::tr1::shared_ptr。Google建议尽量避免使用智能指针，使用对象

###other cpp
* 输入参数为值或const引用，输出参数为指针；输入参数可以是const指针，但不能使用非const引用形参
* 限制使用重载函数（相同名字产生困惑；子类可能只实现了一个），如果需要重载函数，可以使用不同的函数名称，并在名称中体现不同函数的特点
* 调用函数时必须明确指明每一个参数，避免在拷贝代码时忽略不为人知的缺省参数值
* 禁止使用变长数组和alloca()，使用安全的分配器allocator，如scoped_ptr/scoped_array
* 通常将友元定义在同一个文件下
* 不要使用c++异常
    * 捕获异常可能导致函数提前结束，使得在catch之前的内存没有释放，影响程序控制流
    * 使用throw时，需要检查所有调用的地方是否有基本的异常安全保护或者程序正常结束
* 除了在单元测试中，不要使用RTTI(runtime type info)，如果程序中需要在运行时检测对象类型，说明设计有问题或者换种方式识别对象类型，考虑使用双重分发方案，如Visitor模式
* static_cast: 强制转换，指针的父类到子类的明确向上转换
* const_cast: 移除const属性
* reinterpret_cast:指针类型和整型或其他指针间不安全的相互转换，仅在你对所做一切了然于心时使用
* dynamic_cast:除测试外不要使用
* 不要使用流，除非时日志接口需要，使用printf之类的代替
* 对于迭代器和模板类型来说，要使用前置++/--。因为后置的方式要对表达式i进行一次拷贝
* 尽可能的多的使用const
* 尽可能使用sizeof(varname)，而不是sizeof(type)
* <stdint.h>中定义了int16_t/uint32_t/int64_t等整型，在需要确定大小的整型时可以使用它们代替short/unsigned long long。在C中只使用int。适当情况下使用size_t or ptrdiff_t
* 对于大整数使用int64_t;不要使用uint32_t等无符号整型，除非你是用来标识bit pattern而不是一个数值。即使数值不会为负值也不要使用无符号类型，使用断言来保护数据。比较有符号变量和无符号变量时，C的类型提升机制会导致无符号类型的行为出乎意料。
* sizeof(void*)!=sizeof(int)，如果需要一个指针大小的整数要使用intptr_t
* 64bit系统中任何拥有int64_t/uint64_t成员的类和结构体将默认处理为8字节对齐。gcc使用__attribute__((packed))，msvc使用#pragma pack()和__declspec(align())控制字节对齐
* 创建64位常量时使用LL或ULL作为后缀例如`int64_t value = 0x123456789LL;`,`uint64_t value = 3ULL <<48;`
* 不要在.h中定义宏；使用前正确#define，使用后正确#undef;不要只是对已经存在的宏使用#undef，选择一个不会冲突的名称；
* 整数使用0,实数使用0.0,字符串使用'\0',指针使用NULL
 


