#include <iostream>
#include <BaseItem.h>
#include <vector>
#include <memory>
#include <tr1/memory>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "Blob.h"

using namespace std;

void ShowItem(BaseItem& item)
{
    cout<<"Item id: "<<item.GetID()<<endl;
}

void ShowItem(int data)
{
    cout<<"Show integer: "<<data<<endl;
}

#define MAX_VALUE(a, b) ShowItem((a) > (b) ? (a) : (b))

template<typename T>
inline void MaxValue(const T& a, const T& b)
{
    ShowItem(a > b ? a : b);
}

template<typename T>
int compare(const T& left, const T& right)
{
    if (left < right) return -1;
    if (left > right) return 1;
    return 0;
}

template<typename T, class U>
T calc(const T& a, const U& b)
{
    T tmp = a + b;
    return tmp;
}

template<unsigned N, unsigned M>
int compare(const char (&p1)[N], const char (&p2)[M])
{
    return strcmp(p1, p2);
}

void ManageObjects(int count)
{
    std::tr1::shared_ptr<BaseItem> pItem(new BaseItem(5));
    std::tr1::shared_ptr<BaseItem> pItem2(pItem); // pItem2指向对象，pItem也指向对象，引用计数为2
    pItem = pItem2;  // pItem2指向对象，pItem也指向对象
    pItem2->Print();
    pItem->Print();
    //....
    if(0 == count)
    {
       return ;
    }
}


int main()
{

    char szInfo[50] = {0};
    float fValue = 6.625f;
    int nPresion = 2;
    //fValue += 5/pow(10,nPresion+1);
    sprintf(szInfo, "%.*f", nPresion, fValue);
    cout << szInfo << endl;

    //ShowItem(34);
    Game cod;
    Game gta(cod);
    gta.SetName("gta");
    cod = gta;
    ManageObjects(0);

    compare("good", "god");

    Blob<int> squares = {0, 1, 2, 3, 4, 5};
    for (size_t i = 0; i != squares.size(); i++)
    {
        squares[i] = i*i;
    }

    getchar();
    return 0;
}
