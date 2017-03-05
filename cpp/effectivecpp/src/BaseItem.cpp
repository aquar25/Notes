#include <iostream>
//#include <cstdlib>
#include <cstring>
#include "BaseItem.h"

using namespace std;

const float BaseItem::PIE = 3.14;

BaseItem::BaseItem():m_nID(0)
{
    //ctor
    cout<<"default constructor...."<<endl;
    memset(m_szName, 0, sizeof(m_szName));
}

BaseItem::BaseItem(int id)
{
    cout<<"constructor with an integer..."<<endl;
    m_nID = id;
    memset(m_szName, 0, sizeof(m_szName));
}
BaseItem::~BaseItem()
{
    //dtor
    cout<<"destructor ..."<<endl;
}

BaseItem::BaseItem(const BaseItem& other)
{
    //copy ctor
    cout<<"BaseItem copy constructor..."<<endl;
    m_nID = other.m_nID;
    strncpy(m_szName, other.m_szName, strlen(m_szName));
}

BaseItem& BaseItem::operator=(const BaseItem& rhs)
{
    // this是=左侧的对象指针
    cout<<"BaseItem assignment ..."<<endl;
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    m_nID = rhs.m_nID;
    strncpy(m_szName, rhs.m_szName, strlen(m_szName));
    // 返回指向=左侧对象的引用，从而实现连锁赋值
    return *this;
}

void BaseItem::SetName(char* val)
{
    strncpy(m_szName, val, strlen(m_szName));
}

void BaseItem::Print()
{
    cout<<"id: "<<m_nID<<endl;
}

Game::Game():type(0)
{

}

Game::~Game()
{

}

Game::Game(const Game& rhs)
:BaseItem(rhs),//调用基类的拷贝构造
type(rhs.type) // 子类本地成员
{
    cout<< "Game copy constructor" << endl;
}

Game& Game::operator=(const Game& rhs)
{
    cout<< "Game's = function..." << endl;
    if (&rhs == this) return *this;
    BaseItem::operator=(rhs); //调用基类的赋值
    type = rhs.type;  //子类本地成员
    return *this;
}
