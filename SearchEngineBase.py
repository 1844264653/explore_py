"""
SearchEngineBase 可以被继承，继承的类分别代表不同的算法引擎。
每一个引擎都应该实现 process_corpus() 和 search() 两个函数，
对应我们刚刚提到的索引器和检索器。main() 函数提供搜索器和用户接口，
于是一个简单的包装界面就有了。
"""

import os.path

root = os.path.dirname(os.path.abspath(__file__))
search_fs = os.path.join(root, "file2search")


class SearchEngineBase(object):
    def __init__(self):
        pass

    def add_corpus(self, file_path):
        """
        函数负责读取文件内容，将文件路径作为 ID，连同内容一起送到 process_corpus 中。
        :param file_path:
        :return:
        """
        with open(file_path, 'r') as fin:
            text = fin.read()
            self.process_corpus(file_path, text)

    def process_corpus(self, Id, text):
        """
        需要对内容进行处理，然后文件路径为 ID ，将处理后的内容存下来。处理后的内容，就叫做索引（index）。
        :param Id:
        :param text:
        :return:
        """
        raise Exception('process_corpus not implemented.')

    def search(self, query):
        """
        则给定一个询问，处理询问，再通过索引检索，然后返回
        :param query:
        :return:
        """
        raise Exception('search not implemented.')


def main(search_engine):
    files = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']
    full_pths = [os.path.join(search_fs, f_pth) for f_pth in files]
    for file_path in full_pths:
        search_engine.add_corpus(file_path)

    while True:
        query = input()
        results = search_engine.search(query)
        print('found {} result(s):'.format(len(results)))
        for result in results:
            print(result)


class SimpleEngine(SearchEngineBase):
    def __init__(self):
        super(SimpleEngine, self).__init__()
        self.__id_to_texts = {}

    def process_corpus(self, id, text):
        """
        索引
        """
        self.__id_to_texts[id] = text

    def search(self, query):
        results = []
        for id, text in self.__id_to_texts.items():
            if query in text:
                results.append(id)
        return results


search_engine = SimpleEngine()
main(search_engine)

# 但显然是一种很低效的方式：
#       每次索引后需要占用大量空间，因为索引函数并没有做任何事情；
#       每次检索需要占用大量时间，因为所有索引库的文件都要被重新搜索一遍。
#       如果把语料的信息量视为 n，那么这里的时间复杂度和空间复杂度都应该是 O(n) 级别的。

# 这里的 query 只能是一个词，或者是连起来的几个词。如果你想要搜索多个词，它们又分散在文章的不同位置，我们的简单引擎就无能为力了。


#  这时应该怎么优化呢？

"""
最直接的一个想法，就是把语料分词，看成一个个的词汇，这样就只需要对每篇文章存储它所有词汇的 set 即可。
根据齐夫定律（Zipf’s law，https://en.wikipedia.org/wiki/Zipf%27s_law），
在自然语言的语料库里，一个单词出现的频率与它在频率表里的排名成反比，呈现幂律分布。
因此，语料分词的做法可以大大提升我们的存储和搜索效率。
"""
