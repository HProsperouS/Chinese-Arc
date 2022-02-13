import shelve
from heapq import nlargest
#  TOP SELLING PRODUCT
def TopTenSellings():
    try:
        cust_order_dict = {}
        db = shelve.open('CustOrder.db', 'r')
        cust_order_dict = db['CustOrder']
    except:
        print('Unable to read data')
    finally:
        db.close()

    cust_order_list = []
    for key in cust_order_dict:
        cust_order = cust_order_dict.get(key)
        cust_order_list.append(cust_order)

    top = nlargest(10,cust_order_list, key=lambda product: key.get_order_quantity)

    print(top)



