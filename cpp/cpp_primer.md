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

###Chapter 12.1 

#####12.1.1 智能指针
程序中使用动态内存的地方：
1. 不知道需要多少对象，数字不是常量，而是运行时才知道的
2. 不知道具体需要哪种类型的对象，多态
3. 在多个对象之间共享数据

C++库的智能指针有三类，`shared_ptr` `unique_ptr` `weak_ptr`，以下都在`<memory>`中定义

智能指针也是通过模板来实现的，因此也需要告诉他数据类型
`shared_ptr<string> p1`定义了一个指向string类型的`shared_ptr`，默认为null.
`shared_ptr<list<int>> p2`定义了一个指向一个int类型的list的`shared_ptr`.

智能指针的用法和普通类型的指针用法一样。当最后一个指向动态内存的`shared_ptr`被释放的时候，它会释放动态内存的资源，调用其析构函数。
```c++
// 判断指针如果不为null，再判断是否是一个空字符串
if (p1 && p1->empty())
    *p1 = "hi";     // 如果是空字符串，给它赋值
```

`shared_ptr`和`unique_ptr`都支持的操作  
* `shared_ptr<T> sp` null smart pointer that can point to objects of type T
* `sp`  use sp as a condition; true if sp points to an object
* `*sp` Dereference sp to get the object to which p points
* `p->mem`   Synonym for `(*p).mem`
* `p.get()`  Return the pointer in p. 不要直接使用这个指针，它随时可能被智能指针释放
* `swap(p, q)` `p.swap(q)`  Swaps the pointers in p and q

`shared_ptr`特有的操作  
* `make_shared<T>(args)`  Returns a `shared_ptr` pointing to a dynamically allocated object of type T. Uses args to initialize the object
* `shared_ptr<T> p(q)`   p is a copy of `shared_ptr` q; 增加q里面的计数，q里面的指针必须可以转换为`T*`类型
* `p=q`   减少p里面的计数，如果p里面的计数为0释放p指向的内存；增加q中的计数，左边对象原来的减少计数，右边的增加计数。
* `p.use_count()`   返回有多少个对象和p共用，这是个耗时操作，用于调试
* `p.unique()`  returns true if `p.use_count()` is one; false otherwise

最好使用`make_shared<T>(args)`方式定义一个智能指针

```c++
// shared_ptr that points to an int with value 42
shared_ptr<int> spInt = make_shared<int>(42);
// points to a string with value 9999999999
shared_ptr<string> spStr = make_shared<string>(10, '9');
// points to an int that is value initialized to 0
auto spInt0 = make_shared<int>(); // 使用auto自动识别类型
```

`shared_ptr`之间的赋值、拷贝构造都是增加引用计数，不会重新分配内存。因此可以把函数内动态申请的内存通过`shared_ptr`作为返回值返回。

```c++
// 工厂函数返回一个指针
shared_ptr<Game> factory()
{
    return make_shared<Game>();
}

// 其他使用的地方，当执行到括号外退出作用域时，释放资源
{
    shared_ptr<Game> sp = factory();
    sp->play();
}

```

由于只要有引用存在，`shared_ptr`指向的资源就不会被释放，因此在使用时需要注意把不在用的`shared_ptr`即时释放，避免占用内存资源。例如在vector中存放的是`shared_ptr`的对象，如果vector中有一部分的对象已经不需要使用了，如果不删除，这些对象会一直占用着内存。

If you put `shared_ptr` in a container, and you subsequently need to use some, but not all, of the elements, remember to erase the elements to you no longer need.

对于vector而言，当vector自身销毁时，存放在它里面的元素也会被销毁，拷贝时，也会直接拷贝它里面的元素。例如下面的例子就无法实现在多个对象之间共享数据的目的。数据是拷贝了多次。

```c++
vector<string> v1; // empty vector
{
    vector<string> v2 = { "a", "an", "the" };
    v1 = v2; 
}// v2 is destroyed, which destroys the elements in v2
// v1 has three elements, which are copies of the ones originally in v2
```
一个对象的成员在这个对象销毁时也会被销毁，因此需要把这个成员定义为动态内存，才不会被释放。通过使用`shared_ptr`作为成员，当一个对象的成员释放后，还有其他对象的成员有这个动态内存的引用，因此不会被释放掉。

模板章节的`class Blob`就通过定义`std::shared_ptr<std::vector<T>> data`作为成员变量，达到在多个对象之间共享data的目的。当拷贝、赋值`Blob`的对象时，其内部成员data也会被直接拷贝、赋值，从而增加了data的引用计数。

下面例子中，最终b1中有4个对象，和vector的版本不同。
```C++
    Blob b1;
    {
        Blob b2 = { "a", "an", "the" };
        b1 = b2;
        b2.push_back("about");
    }
```

##### 12.1.2 直接管理动态内存
如果一个类直接管理内存，那么它的拷贝、赋值、和析构函数需要额外注意内存的拷贝。
通过new分配的对象会调用默认的构造函数，但是对于内建类型如int、复合类型如结构体，则没有初始化，是未定义的值。
当然也可以new的时候之间调用指定的构造函数
```c++
int *pi = new int(1024); // object to which pi points has value 1024
string *ps = new string(10, '9'); // *ps is "9999999999"
// C++11 vector with ten elements with values from 0 to 9
vector<int> *pv = new vector<int>{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
```
新的C++标准中auto使用初始化变量的类型类推导定义的变量的类型
```c++
auto p1 = new auto(obj); // p points to an object of the type of obj
// that object is initialized from obj. If obj is an int, then p1 is int*; if obj is a string, then p1 is a string*
auto p2 = new auto{a,b,c}; // error: must use parentheses for the initializer
```
* 可以使用new来创建常量对象，此时必须有初始化，得到的指针是指向常量的。
```c++
// allocate and initialize a const int
const int *pci = new const int(1024);
// allocate a default-initialized const empty string
const string *pcs = new const string;
```
   
* 当内存无法满足new的大小时，new会抛出`bad_alloc`异常。我们可以阻止抛出异常使用placement new.这时可以传递一个参数给new，这里传递库提供的nothrow告诉new不要抛出异常，而是返回null。需要<new>这个头文件。
```c++
// if allocation fails, new returns a null pointer
int *p2 = new (nothrow) int; 
```
* delete只能对null或动态分配的内存有效
* 编译器无法区分一个地址是动态分配的还是静态或本地变量
* 一个常量对象无法更改，但是动态分配的常量可以销毁。
```c++
int i, *pi1 = &i, *pi2 = nullptr;
double *pd = new double(33), *pd2 = pd;
delete i; // error: i is not a pointer
delete pi1; // undefined: pi1 refers to a local
delete pd; // ok
delete pd2; // undefined: the memory pointed to by pd2 was already freed
delete pi2; // ok: it is always ok to delete a null pointer  
const int *pci = new const int(1024);
delete pci; // ok: deletes a const object         
```


### Part III

#### 13.3 Swap
一个有动态分配资源的类一般会定义自己的swap函数，在stl的算法需要对对象进行排序时，交换两个元素比使用std::swap会提高效率。如果一个类定义了自己的swap函数，库就会优先匹配到当前类的swap而不是std的。

一般情况下std的swap可能会执行一次拷贝和2次赋值操作。例如HasPtr内部有一个string对象的指针，在拷贝构造时，就会给temp内部分配一份string的内存用来深拷贝，但实际上我们只是需要交换v1和v2内部string对象的指针即可，根本不需要那次多余的内存分配。
```c++
HasPtr temp = v1; // make a temporary copy of the value of v1
v1 = v2; // assign the value of v2 to v1
v2 = temp; // assign the saved value of v1 to v2
```
通常一个类swap函数如下定义，swap函数被声明为friend，这样可以访问到类的私有成员变量。同时由于swap这里是为了优化性能，因此定义为inline的。函数内部调用std的swap来直接交换两个对象指针成员ps。
```c++
class HasPtr 
{
public:
    // to access the private member
    friend void swap(HasPtr&, HasPtr&);

public:
    HasPtr(const std::string &s = std::string()) :
        ps(new std::string(s)), i(0) { }    
    // each HasPtr has its own copy of the string to which ps points
    HasPtr(const HasPtr &p) :
        ps(new std::string(*p.ps)), i(p.i) { }
    HasPtr& operator=(const HasPtr &);
    ~HasPtr() { delete ps; }    
private:
    std::string *ps;
    int i;
};

inline
void swap(HasPtr &lhs, HasPtr &rhs)
{
    using std::swap;
    swap(lhs.ps, rhs.ps); // swap the pointers, not the string data
    swap(lhs.i, rhs.i); // swap the int members
}
```

需要注意在调用时，不能用std::swap()，那样就无法调用类自己定义的swap了。
> If there is a type-specific version of swap, that version will be a better match than the one defined in std.

##### copy and swap
如果一个类定义了自己的swap函数，通常它会用swap函数来定义赋值操作。通过将左值与右值的一个拷贝进行交换。

注意这里的参数不是引用，而是值，这样在传递入参时会把=右边的对象拷贝一份为rhs。在实现内部将左值的成员与拷贝的临时变量的成员交换，从而把右值的内容复制到了左值里面，而左值原来内部的指针在临时变量rhs退出函数时释放。

```c++
// note rhs is passed by value, which means the HasPtr copy constructor
// copies the string in the right-hand operand into rhs
HasPtr& HasPtr::operator=(HasPtr rhs)
{
    // swap the contents of the left-hand operand with the local variable rhs
    swap(*this, rhs); // rhs now points to the memory this object had used
    return *this; // rhs is destroyed, which deletes the pointer in rhs
}
```
这个实现有两个好处：
1. 不用判断是否是自我赋值了，因为右值被拷贝了一份
2. 异常安全，copy构造的过程中new失败抛出异常在修改左值之前发生。










