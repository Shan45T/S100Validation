
from collections import OrderedDict

cachedict = OrderedDict()

class CacheUtillity():    
    def getItem(key):
        if key not in cachedict.keys():
            return " No Value for specified key"
        else:
            cachedict.move_to_end(key)
            return  cachedict.get(key)

    def setItem(key, value):
        if key not in cachedict.keys():
            if(len(cachedict) > 10):
                return "Reached maximum size"
            else:                
                cachedict[key] = value
                cachedict.move_to_end(key)                

# class LRUCache:
 
#     # initialising capacity
#     def __init__(self, capacity: int):
#         self.cache = OrderedDict()
#         self.capacity = capacity
 
#     # we return the value of the key
#     # that is queried in O(1) and return -1 if we
#     # don't find the key in out dict / cache.
#     # And also move the key to the end
#     # to show that it was recently used.
#     def get(self, key: int) -> int:
#         if key not in self.cache:
#             return -1
#         else:
#             self.cache.move_to_end(key)
#             return self.cache[key]
 
#     # first, we add / update the key by conventional methods.
#     # And also move the key to the end to show that it was recently used.
#     # But here we will also check whether the length of our
#     # ordered dictionary has exceeded our capacity,
#     # If so we remove the first key (least recently used)
#     def put(self, key: int, value: int) -> None:
#         self.cache[key] = value
#         self.cache.move_to_end(key)
#         if len(self.cache) > self.capacity:
#             self.cache.popitem(last = False)
 
