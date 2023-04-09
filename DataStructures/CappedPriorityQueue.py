class CappedPriorityQueue:
    def __init__(self, evaluate, maxsize = 6):
        # container
        self.arr = []
        # max size of priority queue
        self.__maxsize__ = maxsize
        # function to get value of item
        self.evaluate = evaluate

    # determine if every item in queue is good enough
    def good(self, threshold):
        if (len(self.arr) < self.__maxsize__):
            return False
        for x in self.arr:
            if (self.evaluate(x) < threshold):
                return False
        return True
    
    # push item into queue from the top
    def push(self, item):
        if (len(self.arr) == 0):
            self.arr.append(item)
        else:
            done = 0
            for i, x in enumerate(self.arr):
                if (self.evaluate(item) > self.evaluate(x)):
                    self.arr.insert(i, item) 
                    done = 1
                    break

            if (not done):
                self.arr.append(item)

            # remove lowest value item if queue is overcapped
            if (len(self.arr) > self.__maxsize__):
                self.arr.pop()
    
    # print queue items
    def print(self):
        for i, x in enumerate(self.arr):
            print(x)

