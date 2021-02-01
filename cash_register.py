#!/usr/bin/env python

import pandas as pd
import unittest

class Buy():
    list = []
    subtotal = 0
    total = 0
    iva = 0
    payment = 0
    
    def add(self,product):
        self.list.append(product)
        self.subtotal = product.final_price + self.subtotal
        self.iva = self.subtotal * 0.19
        
    def total_calculation(self):
        self.total = self.subtotal + self.iva
    
    def customer_payment(self, payment):
        self.change = payment - self.total

    def __str__(self):
        return " Subtotal: {:7.1f}".format(self.subtotal)


class Product():
    def __init__(self, product, code, price, discount):
        self.product = product
        self.code = int(code)
        self.price = float(price)
        self.discount = float(discount)  # in percentage
        self.discount_currency = self.discount * self.price  # currency
        self.final_price = self.price - self.discount_currency

    def __str__(self):
        return "Product:  {:25s}   \n  Price: {:7.1f}  |    Discount: -  {:3.2f}  ({:3.2f} %) | Final Price: {:7.1f}  |" \
            .format(self.product.values[0], self.price, self.discount_currency,self.discount, self.final_price)

class ProductTest(unittest.TestCase):
    # final price product 26
    def test_Item_26(self):
        self.product = Product('Refined salt',26,339,0.2)
        self.assertEqual(271.2,self.product.final_price)

    # subtotal of two products, items 26 y 28
    def test_Items_26_28(self):
        self.buy = Buy()
        self.buy.add(Product('Refined salt',26,339,0.2))
        self.buy.add(Product('Ground cumin',28,239,0))
        self.assertEqual(510.2,self.buy.subtotal)

    # change products 26 y 28 by paying 1000
    def test_Items_26_28_change(self):
        self.buy = Buy()
        self.buy.add(Product('Refined salt',26,339,0.2))
        self.buy.add(Product('Ground cumin',28,239,0))
        self.buy.total_calculation()
        self.buy.customer_payment(1000)
        self.assertEqual(392.9,round(self.buy.change,1))

df = pd.read_csv('products.txt',',', index_col=False,header = 0, skiprows = 0 )


def run():
    buy = Buy()
    p = []
    flag = True
    i = 0
    print(df.head())
    while flag == True:
        print('  Enter the product code:')
        code = input()
        if len(code) < 1: continue
        elif 't' == code.lower():
            buy.total_calculation()
            print('The total is:')
            print('*****************************************')
            print(buy)
            print('*****************************************')
            print(" Iva: {:5.1f}   TOTAL: {:7.1f}".format(buy.iva, buy.total))
            print('*****************************************')
            print('Enter the amount paid per customer:')
            payment = input()
            while len(payment)<1:
                print('Enter the amount paid per customer:')
                payment = input()
                continue
            payment = float(payment)
            buy.customer_payment(payment)
            while buy.change < 0: 
                print('The amount must be greater than the total')            
                payment = float(input())
                buy.customer_payment(payment)
            print("Change: {:7.1f}".format(buy.change))
            print('*****************************************')
            flag = False

        else:
            df_find = df[df['Code'] == int(code)]
            if len(df_find) == 0: 
                print ('The code does not exist') 
                continue
            product = df_find.Product
            price = df_find.Price
            discount = df_find.Discount
            p.append(Product(product,code,price,discount))
            buy.add(p[i])
            print(buy.list[i],buy)
            i += 1

run()

if __name__ == '__main__':
    unittest.main()