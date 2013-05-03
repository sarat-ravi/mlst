class unionFind():
    def __init__(self,lst):
        self.mappings = dict(zip(lst,range(len(lst))))
        self.sizes = [1 for i in range(len(lst))]
        self.items = lst[:]
    def find(self,item):
        ind = self.mappings[item]
        while ind != self.mappings[self.items[ind]]:
            self.mappings[self.items[ind]] = self.mappings[self.items[self.mappings[self.items[ind]]]]
            ind = self.mappings[self.items[ind]]
        return self.items[ind]
    def size(self,item):
        return self.sizes[self.mappings[self.find(item)]]

    def union(self,a,b):
        (big, little) = (a,b) if self.size(a) > self.size(b) else (b,a)
        littleSize = self.size(little)
        bigParent,littleParent = self.find(big), self.find(little)
        self.mappings[littleParent] = self.mappings[bigParent]
        self.sizes[self.mappings[bigParent]] += littleSize
    def display(self):
        print"==============="
        print "MAPPINGS: ", self.mappings
        print "sizes: ", self.sizes
        print "items: ", self.items
        print"==============="