import re
from SearchEngineBase import *


class BOWInvertedIndexEngine(SearchEngineBase):
    def __init__(self):
        super(BOWInvertedIndexEngine, self).__init__()
        self.inverted_index = {}

    def process_corpus(self, id, text):
        words = self.parse_text_to_words(text)
        for word in words:
            if word not in self.inverted_index:
                self.inverted_index[word] = []
                self.inverted_index[word].append(id)

    def search(self, query):
        query_words = list(self.parse_text_to_words(query))

        query_words_index = list()
        for query_word in query_words:
            query_words_index.append(0)

        # 如果某一个查询单词的倒序索引为空，我们就立刻返回
        for query_word in query_words:
            if query_word not in self.inverted_index:
                return []

        result = []
        while True:

            # 首先，获得当前状态下所有倒序索引的 index
            current_ids = []
            for idx, query_word in enumerate(query_words):
                current_index = query_words_index[idx]
                current_inverted_list = self.inverted_index[query_word]

                # 已经遍历到了某一个倒序索引的末尾，结束 search
                if current_index >= len(current_inverted_list):
                    return result

                current_ids.append(current_inverted_list[current_index])

            # 然后，如果 current_ids 的所有元素都一样，那么表明这个单词在这个元素对应的文档中都出现了
            if all(x == current_ids[0] for x in current_ids):
                result.append(current_ids[0])
                query_words_index = [x + 1 for x in query_words_index]
                continue

            # 如果不是，我们就把最小的元素加一
            min_val = min(current_ids)
            min_val_pos = current_ids.index(min_val)
            query_words_index[min_val_pos] += 1

    @staticmethod
    def parse_text_to_words(text):
        # 使用正则表达式去除标点符号和换行符
        text = re.sub(r'[^\w ]', ' ', text)
        # 转为小写
        text = text.lower()
        # 生成所有单词的列表
        word_list = text.split(' ')
        # 去除空白单词
        word_list = filter(None, word_list)
        # 返回单词的 set
        return set(word_list)


search_engine = BOWInvertedIndexEngine()
main(search_engine)


"""
首先我要强调一下，这次的算法并不需要你完全理解，
面向对象编程是如何把算法复杂性隔离开来，而保留接口和其他的代码不变
Inverted Index。Inverted Index Model，即倒序索引，是非常有名的搜索引擎方法
倒序索引，一如其名，也就是说这次反过来，我们保留的是 word -> id 的字典。
于是情况就豁然开朗了，在 search 时，我们只需要把想要的 query_word 的几个倒序索引单独拎出来，
然后从这几个列表中找共有的元素，那些共有的元素，即 ID，就是我们想要的查询结果。这样，我们就避免了将所有的 index 过一遍的尴尬。

process_corpus 建立倒序索引。
注意，这里的代码都是非常精简的。在工业界领域，需要一个 unique ID 生成器，来对每一篇文章标记上不同的 ID，
倒序索引也应该按照这个 unique_id 来进行排序。

至于 search() 函数，你大概了解它做的事情即可。
它会根据 query_words 拿到所有的倒序索引，
如果拿不到，就表示有的 query word 不存在于任何文章中，直接返回空；
拿到之后，运行一个“合并 K 个有序数组”的算法，从中拿到我们想要的 ID，并返回。
注意，这里用到的算法并不是最优的，最优的写法需要用最小堆来存储 index。
这是一道有名的 leetcode hard 题，有兴趣请参考：https://blog.csdn.net/qqxx6661/article/details/77814794）


遍历的问题解决了，那第二个问题，如果我们想要实现搜索单词按顺序出现，或者希望搜索的单词在文中离得近一些呢？
我们需要在 Inverted Index 上，对于每篇文章也保留单词的位置信息，这样一来，在合并操作的时候处理一下就可以了。

到这一步，终于，你的搜索引擎上线了，有了越来越多的访问量（QPS）。
欣喜骄傲的同时，你却发现服务器有些“不堪重负”了。经过一段时间的调研，你发现大量重复性搜索占据了 90% 以上的流量，
于是，你想到了一个大杀器——给搜索引擎加一个缓存。
"""