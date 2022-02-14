class Count():
    count = 0
    def __init__(self):
        Count.count += 1
        self.__count = Count.count
    
    def get_count(self):
        
        return self.__count
    
    def set_count(self, count):
        self.__count = count
