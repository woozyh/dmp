#!/usr/bin/python3.11.8

import sqlite3
from   fileReader    import Reader
from   os            import listdir
from   nltk.tokenize import RegexpTokenizer

class BuildMatrix(object):

    def __init__(self) -> None:

        self.stopWords = {'i','i\'m', 'I\'m', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'}
        try:
            self.database = sqlite3.connect("termDoc.db")
            self.cursor   = self.database.cursor()
            self.docs     = listdir("docs/")
            [self.cursor.execute(f"DROP TABLE IF EXISTS {doc[:-4]};") for doc in self.docs]
            [self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {doc[:-5]} (term text PRIMARY KEY, frequency int);") for doc in self.docs]
        except sqlite3.OperationalError as er:
           print(f"database Error: {er}")

    def remStopWordsOur(self, lineIn) -> str:
        # this function never called in thish program at all we are doing some profiling on it for more performance
        rmdStopWordsLn = ' '.join(w for w in lineIn.split() if w.lower() not in self.stopWords)
        return rmdStopWordsLn

    def preprocessText(self, lineIn) -> str:
        lineInLower = lineIn.lower()
        lineInRmdSplChars = lineInLower.replace('.',' ').replace(';',' ').replace(',',' ').replace('?',' ').replace('!',' ').replace(':',' ')
        return lineInRmdSplChars

    def buildTermDocMatrix(self):
        for doc in self.docs:
            lines = Reader(f"docs/{doc}").read()
            while True:
                try:
                    words = RegexpTokenizer(r'\w+').tokenize(self.preprocessText(next(lines)))
                    for word in words:
                        if word not in self.stopWords:
                            self.frequency = self.cursor.execute(f"SELECT frequency FROM {doc[:-4]} WHERE term='{word}'").fetchone()
                            try:
                                self.cursor.execute(f"""
                                    INSERT OR IGNORE INTO {doc[:-4]} VALUES (?, ?) ON CONFLICT (term) DO UPDATE SET frequency=excluded.frequency+1""",
                                    (word, self.frequency[0]))
                            except TypeError:
                                self.cursor.execute(f"INSERT INTO {doc[:-4]} VALUES (?, ?)", (word, 1, ))
                            self.database.commit()
                except StopIteration:
                    break
        self.cursor.close()
        self.database.close()

def main():
    ins = BuildMatrix()
    ins.buildTermDocMatrix()

if __name__ == "__main__":
    main()
