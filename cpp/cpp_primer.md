### 模板

#### 函数模板

模板定义以关键字template开始，<>中包含一个模板参数列表，里面是一个逗号分隔的一个或多个模板参数。

模板的定义类似函数的定义，编译器根据实际调用的参数类型编写出对应类型的函数，并编译这个函数。

模板需要在编译期直到数据的类型，而多态则不用

```c++
template<typename T>
int compare(const T& left, const T& right)
{
    if (left < right) return -1;
    if (left > right) return 1;
    return 0;
}
```

T 时模板类型参数，可以看作类型说明符，可以用typename或class来声明，在模板参数列表中可以同时使用这两个关键字，效果一模一样。但是使用typename关键字更直观，不会被误解。模板类型参数前必须有typename的修饰

```c++
template <typename T, class U>
T calc(const T& a, const U& b)
{
    T tmp = a + b;
    return tmp;
}
```

模板还可以使用非类型参数，它标识一个值，而非一个类型。非类型参数的模板实参必须时常量表达式，因为模板在编译期被实例化为一个具体的函数，此时需要知道具体的值才能实例化。

```c++
template<unsigned N, unsigned M>
int compare(const char (&p1)[N], const char (&p2)[M])
{
    return strcmp(p1, p2);
}
```

当调用`compare("good", "god");`时，编译器会使用字面常量的大小代替N和M，此处为：

`int compare(const char (&p1)[5], const char (&p2)[4])`

一个非类型参数可以是一个整型，或者一个指向对象或函数类型的指针或(左值)引用。绑定到指针或引用非类型参数的实参必须具有静态的生存期。不能使用一个普通的(非static)局部变量或动态对象作为指针或引用非类型模板参数的实参。指针可以使用nullptr或值为0的常量表达式来实例化。

#### 编写类型无关代码

* 将模板函数的参数设定为const引用，保证函数可以用于不能拷贝类型。
* 函数体内对数据类型的操作要求最少，例如不是所有的类型都实现了所有运算符，所以对实参类型要求越少，就越通用

#### 模板编译

编译器只会在我们实例化模板的一个特定版本时，才会生成代码。

当调用一个普通函数时，编译器只需要掌握函数的声明，使用一个类类型对象时，类的定义必须是可用的，但其中的成员函数的定义不必已经出现，因此一般把类的定义和函数声明放在头文件中，类成员函数和普通函数的定义放在源文件中。

模板的头文件通常包括声明和定义：编译器需要掌握函数模板或类模板成员函数的定义才能实例化一个模板的版本。

当使用模板时，所有不依赖于模板参数的名字都必须是可见的，当模板被实例化时，模板的定义，包括类模板成员的定义，都必须时可见的，这是有模板的提供者保障的。

用来实例化模板的所有参数、类型以及与类型关联的运算符的声明都必须是可见，这是由模板的使用者来保证的。

#### 类模版

编译器不能为类模板推断模板参数的类型，因此在使用类模板时，需要明确指出类型信息，例如`vector<string>`

在类模板及其成员的定义中，我们将模板参数当作替身，代替使用模板时用户提供的类型或值。

类模版的名字不是一个类型名，它是用来实例化一个类型的。如果一个类模板中使用了另一个模板，通常不将一个实际类型或值的名字用作其模板实参，而是将模板自己的参数当作被使用模板的实参。

```c++
template <typename T>
class Blob
{
public:
    typedef T value_type;
    typedef typename std::vector<T>::size_type size_type;

    Blob();
    Blob(std::initializer_list<T> il);

    size_type size() const { return data->size(); }
    bool empty() const { return data->empty(); }
    void push_back(const T &t) { data->push_back(t);}
    void push_back(T &&t) { data->push_back(std::move(t)); }
    void pop_back();

    T& back();
    T& operator[](size_type i);

private:
    // 将模板测参数作为内部使用的模板的实参
    std::shared_ptr<std::vector<T>> data;
    void check(size_type i, const std::string &msg) const;
};
```

##### 类模板成员函数

定义在类模板内的成员函数被隐式声明为内联函数。默认情况下，对于一个实例化的类模板，其成员只有在使用时才被实例化。

定义在类外部的成员函数，一样需要符合`ret-type class_type::member-name(param-list)`范式。

```c++
template <typename T>
Blob<T>::Blob():data(std::make_shared<std::vector<T>>())
{
    //构造函数中分配一个空vector，并将vector的指针保存在data中
}

// use: Blob<string> words = { "a", "an", "the"};
template <typename T>
Blob<T>::Blob(std::initializer_list<T> il):data(std::make_shared<std::vector<T>>(il))
{

}

template <typename T>
void Blob<T>::pop_back()
{
    check(0, "pop_back on empty Blob");
    data->pop_back();
}

template <typename T>
T& Blob<T>::back()
{
    check(0, "back on empty Blob");
    return data->back();
}

template <typename T>
T& Blob<T>::operator[](size_type i)
{
    check(i, "subscript out of the range");
    return (*data)[i];
}

template <typename T>
void Blob<T>::check(size_type i, const std::string &msg) const
{
    if (i >= data->size())
        throw std::out_of_range(msg);
}
```

##### 使用类模板

```C++
Blob<int> squares = {0, 1, 2, 3, 4, 5};
for (size_t i = 0; i != squares.size(); i++)
{
    squares[i] = i*i;
}
```

在类代码内简化模板类名的使用

在类模板自己的作用域中，我们可以直接使用模板而不提供实参。

```c++
template <typename T>
class BlobPtr
{
public:
    BlobPtr(): curr(0) {}
    BlobPtr(Blob<T> &a, size_t sz = 0):wptr(a.data), curr(sz) {}

    T& operator*() const
    {
        auto p = check(curr, "dereference past end");
        return (*p)[curr];
    }
    // 前置运算符
    // 编译器自动会处理实参类型，不需要显式说明BlobPtr<T>&
    BlobPtr& operator++()
    {
        check(curr, "dereference past end");
        ++curr;
        return *this;
    }
    BlobPtr& operator--();
    BlobPtr operator++(int);

private:
    //返回一个指向vector的shared_ptr
    std::shared_ptr<std::vector<T>> check(std::size_t, const std::string&) const;
    // 保存一个weak_ptr,标识底层vector可能被销毁
    std::weak_ptr<std::vector<T>> wptr;
    std::size_t curr; // 数组总当前的位置
};

// 后置：递增对象但返回原值，此处返回值不是引用
// 在类的作用域外，就需要完整的参数声明
template <typename T>
BlobPtr<T> BlobPtr<T>::operator++(int)
{
    //此时又再类的作用域内
    BlobPtr ret = *this; // save curr value
    ++*this;  // 推进一个元素;前置++检查递增是否合法
    return ret;
}
```





