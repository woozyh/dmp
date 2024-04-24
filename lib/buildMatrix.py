#!/usr/bin/python3.11.8
from os          import listdir
from fileReader  import Reader
from nltk        import word_tokenize
from nltk.corpus import stopwords

class BuildMatrix(object):

    def __init__(self) -> None:
        self.docPaths = [f"/home/woozy/mine/dmp/docs/{doc}" for doc in listdir("/home/woozy/mine/dmp/docs/")]
        self.termDoc  = {}
        self.junks    = stopwords.words("english")

    def buildDoc(self):
        for doc in self.docPaths:
            self.termDoc[doc] = dict()
            content           = Reader(doc).read()
            while True:
                try:
                    line = word_tokenize(next(content))
                    for word in line:
                        if word not in self.junks:
                            if word not in self.termDoc[doc]:
                                self.termDoc[doc][word] = 1
                            else:
                                self.termDoc[doc][word] += 1
                    else:
                        pass
                except StopIteration:
                    break

        print('')

ins = BuildMatrix()
ins.buildDoc()
