from BOWInverted import *

import pylru


class LRUCache(object):
    def __init__(self, size=32):
        self.cache = pylru.lrucache(size)

    def has(self, key):
        return key in self.cache

    def get(self, key):
        return self.cache[key]

    def set(self, key, value):
        self.cache[key] = value


class BOWInvertedIndexEngineWithCache(BOWInvertedIndexEngine, LRUCache):
    def __init__(self):
        super(BOWInvertedIndexEngineWithCache, self).__init__()
        LRUCache.__init__(self)

    def search(self, query):
        if self.has(query):
            print('cache hit!')
            return self.get(query)

        result = super(BOWInvertedIndexEngineWithCache, self).search(query)
        self.set(query, result)

        return result


search_engine = BOWInvertedIndexEngineWithCache()
main(search_engine)

"""
它的代码很简单，LRUCache 定义了一个缓存类，你可以通过继承这个类来调用其方法。
LRU 缓存是一种很经典的缓存（同时，LRU 的实现也是硅谷大厂常考的算法面试题，
这里为了简单，我直接使用 pylru 这个包），它符合自然界的局部性原理，可以保留最近使用过的对象，而逐渐淘汰掉很久没有被用过的对象。
"""
