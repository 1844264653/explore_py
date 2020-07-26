"""
先来实现一个名叫 Bag of Words 的搜索模型。
"""

import re
from SearchEngineBase import *


class BOWEngine(SearchEngineBase):
    def __init__(self):
        super(BOWEngine, self).__init__()
        self.__id_to_words = {}

    def process_corpus(self, Id, text):
        self.__id_to_words[id] = self.parse_text_to_words(text)

    def search(self, query):
        query_words = self.parse_text_to_words(query)
        results = []
        for id, words in self.__id_to_words.items():
            if self.query_match(query_words, words):
                results.append(id)
        return results

    @staticmethod
    def query_match(query_words, words):
        for query_word in query_words:
            if query_word not in words:
                return False
        return True

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


search_engine = BOWEngine()
main(search_engine)


"""
这里我们先来理解一个概念，BOW Model，即 Bag of Words Model，中文叫做词袋模型。这是 NLP 领域最常见最简单的模型之一
假设一个文本，不考虑语法、句法、段落，也不考虑词汇出现的顺序，

只将这个文本看成这些词汇的集合。于是相应的，我们把 id_to_texts 替换成 id_to_words，这样就只需要存这些单词，而不是全部文章，也不需要考虑顺序。
process_corpus() 函数调用类静态函数 parse_text_to_words，将文章打碎形成词袋，放入 set 之后再放到字典中。

search() 函数则稍微复杂一些。这里我们假设，想得到的结果，是所有的搜索关键词都要出现在同一篇文章中。那么，我们需要同样打碎 query 得到一个 set，
然后把 set 中的每一个词，和我们的索引中每一篇文章进行核对，看一下要找的词是否在其中。而这个过程由静态函数 query_match 负责。

可是，即使这样做，每次查询时依然需要遍历所有 ID，
虽然比起 Simple 模型已经节约了大量时间，但是互联网上有上亿个页面，每次都全部遍历的代价还是太大了。到这时，又该如何优化呢？

我们每次查询的 query 的单词量不会很多，一般也就几个、最多十几个的样子。那可不可以从这里下手呢？

我们每次查询的 query 的单词量不会很多，一般也就几个、最多十几个的样子。那可不可以从这里下手呢？
"""