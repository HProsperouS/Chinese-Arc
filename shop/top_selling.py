from heapq import nlargest

class Top_selling:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
    def getName(self):
        return self.name
    def getQuantity(self):
        return self.quantity

def getTopSelling(productList):
    top = nlargest(3, productList, key= lambda product:product.getQuantity())