## Steam 

### 市场交易

https://steamcn.com/t148350-1-1

市场上标出的价格都是买方最终购买支付的价格，其中包括厂商的10%和Value的5%抽成。

不同的地区最小交易价格不同。例如美元区为0.03$

- 厂商费用和V社费用由买方支付，所以都是以买方的货币为单位进行计算
- 厂商费用和V社费用在计算的过程中使用向下取整
- 厂商费用和V社费用最低为一个货币单位，注意是买方的货币单位，所以买方的货币越廉价，在购买低价物品时，越有可能节省费用
- 在处理不同货币时，转换的核心是”原价“，也就是卖方获得的那部分，使用当前的汇率进行转换，转换完之后会基于买方的最低货币单位向上取整，因为是向上取整，所以V社在这里也能坑到一些零头

##### 举例

人民币0.15元的原价，V社需要把不低于0.15元的金额存入卖方的钱包，所以美区用户看到的”原价“肯定不能低于这个物品在卖方货币下的”原价“ 。通过汇率转换，可以得到0.15元相当于0.024美元，美元的最低单位是1美分，也就是0.01美元，V社不能贴钱，所以需要向上取整，得到新的”原价“0.03美元。使用新的原价计算出美区的交易费用和最终价格 

厂商费用：0.03美元 x 10% = 0.003美元 这个数值低于买方货币的最低单位，按照1单位计算，也就是：0.01美元 

V社费用： 0.03美元 x 5% = 0.0015美元 这个数值低于买方货币的最低单位，按照1单位计算，也就是：0.01美元 

总价格为：”原价“ 0.03美元 + 厂商费用 0.01美元 + V社费用 0.01美元 = 总价格 0.05美元 



以当前美元对人民币为6.8755，人民币总价在0.22时和0.21卖家得到的一样，而买家付出的少。而在0.16到0.23之间的总价，对于美元区的用户看到的价格始终是0.05$.因此如果以卖美元区为主，则可以把价格标为0.23。

人民币的空档有0.22 、0.33、0.44、0.45、0.56、0.67、0.68、0.80、0.90、0.91、1.02

```bat
卖家       买家        卖家       买家
--------------------
cny:0.07 cny_t:0.09 usd:0.02 usd_t:0.04 
cny:0.08 cny_t:0.10 usd:0.02 usd_t:0.04 
cny:0.09 cny_t:0.11 usd:0.02 usd_t:0.04 
cny:0.10 cny_t:0.12 usd:0.02 usd_t:0.04 
cny:0.11 cny_t:0.13 usd:0.02 usd_t:0.04 
cny:0.12 cny_t:0.14 usd:0.02 usd_t:0.04 
cny:0.13 cny_t:0.15 usd:0.02 usd_t:0.04 
--------------------
cny:0.14 cny_t:0.16 usd:0.03 usd_t:0.05 
cny:0.15 cny_t:0.17 usd:0.03 usd_t:0.05 
cny:0.16 cny_t:0.18 usd:0.03 usd_t:0.05 
cny:0.17 cny_t:0.19 usd:0.03 usd_t:0.05 
cny:0.18 cny_t:0.20 usd:0.03 usd_t:0.05 
cny:0.19 cny_t:0.21 usd:0.03 usd_t:0.05 
cny:0.20 cny_t:0.23 usd:0.03 usd_t:0.05 
--------------------
cny:0.21 cny_t:0.24 usd:0.04 usd_t:0.06 
cny:0.22 cny_t:0.25 usd:0.04 usd_t:0.06 
cny:0.23 cny_t:0.26 usd:0.04 usd_t:0.06 
cny:0.24 cny_t:0.27 usd:0.04 usd_t:0.06 
cny:0.25 cny_t:0.28 usd:0.04 usd_t:0.06 
cny:0.26 cny_t:0.29 usd:0.04 usd_t:0.06 
cny:0.27 cny_t:0.30 usd:0.04 usd_t:0.06 
--------------------
```

* 计算程序

```python
# -*- coding: utf-8 -*-

import math

def calc_local(price):
    dev_fee = convert_floor(price*0.1)       # developer got
    value_fee = convert_floor(price*0.05)    # Value got
    total_price = price + dev_fee + value_fee
    return total_price

def convert_floor(val):
    '''向下取整'''
    threshold = 0.01
    if val < threshold:
        val = threshold
    else:
        val = math.floor(val*100)/100

    return val

def exchange_local_to_other(price, rate):
    price /= rate
    '''向上取整'''
    price = math.ceil(price*100)/100
    return price

def test_cal():
    last_usd = 0
    for x in range(1, 100):
        x = x/100
        usd = exchange_local_to_other(x, 6.8755)
        total = calc_local(x)
        usd_total = calc_local(usd)
        if usd_total!=last_usd:
            last_usd = usd_total
            print('-'*20)
        print("cny:{:.2f} cny_t:{:.2f} usd:{:.2f} usd_t:{:.2f} ".format(x, total, usd, usd_total))

def cal_other_base_local(price, rate):
    '''以本地价格计算美区价格总价'''
    usd = exchange_local_to_other(price, rate)
    return calc_local(usd)

def cal_max_other_price(price, rate):
    local_total = calc_local(price)
    other_price = cal_other_base_local(price, rate)
    # 只要没有超出原始的价格，就可以一次加一个最小单位，直到换算的美区价格变化
    while other_price == cal_other_base_local(price, rate):
        price += 0.01
    return (local_total, price)

if __name__ == '__main__':
    test_cal()
    print(cal_max_other_price(0.20, 6.8755))
```

