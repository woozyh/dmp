#!/usr/bin/python3.11.8
from fileReader  import Reader
from os          import listdir
from nltk.corpus import stopwords
from nltk        import word_tokenize
import sqlite3

class BuildMatrix(object):

    def __init__(self) -> None:
        
        self.junks    = stopwords.words("english")
        
        try:
            self.database = sqlite3.connect("termDoc.db")
            self.cursor   = self.database.cursor()
            [self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {doc[:-4]} (term text PRIMARY KEY, frequency int)") for doc in listdir("/home/woozy/mine/dmp/docs/")]
            
        except sqlite3.OperationalError as er:
            print(f"database Error: {er}")
        

    def buildDoc(self):
        for doc in listdir("/home/woozy/mine/dmp/docs/"):
            lines = Reader(doc).read()
            while True:
                try:
                    words = word_tokenize(next(lines))
                    for word in words:
                        if word not in self.junks:
                            self.cursor.execute("INSERT INTO TABLE ")
                            pass
                except StopIteration:
                    break
        print()
        
        pass

ins = BuildMatrix()
# ins.buildDoc()
