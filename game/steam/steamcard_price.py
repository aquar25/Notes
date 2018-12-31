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
    for x in range(1, 300):
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