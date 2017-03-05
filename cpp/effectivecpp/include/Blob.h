#ifndef BLOB_H_INCLUDED
#define BLOB_H_INCLUDED

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
    std::shared_ptr<std::vector<T>> data;
    void check(size_type i, const std::string &msg) const;
};

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

#endif // BLOB_H_INCLUDED
