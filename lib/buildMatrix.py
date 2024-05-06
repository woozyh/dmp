#!/usr/bin/python3.11.8
from fileReader  import Reader
from os          import listdir
from nltk.tokenize import RegexpTokenizer
import sqlite3

class BuildMatrix(object):

    def __init__(self) -> None:
        
        try:
            self.database = sqlite3.connect("termDoc.db")
            self.cursor   = self.database.cursor()
            [self.cursor.execute(f"DROP TABLE IF EXISTS {doc[:-4]};") for doc in listdir("/home/woozy/mine/dmp/docs/")]
            [self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {doc[:-4]} (term text PRIMARY KEY, frequency int);") for doc in listdir("/home/woozy/mine/dmp/docs/")]
        except sqlite3.OperationalError as er:
            print(f"database Error: {er}")
        
    def remStopWordsOur(self, lineIn) -> str:
        stopWords= {'i','i\'m', 'I\'m', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'}
        rmdStopWordsLn = ' '.join(w for w in lineIn.split() if w.lower() not in stopWords)
        return rmdStopWordsLn

    def preprocessText(self, lineIn) -> str:
        lineInLower=lineIn.lower()
        lineInRmdSplChars=lineInLower.replace('.',' ').replace(';',' ').replace(',',' ').replace('?',' ').replace('!',' ').replace(':',' ')
        return lineInRmdSplChars

    def buildTermDocMatrix(self):
        for doc in listdir("/home/woozy/mine/dmp/docs/"):
            lines = Reader(f"/home/woozy/mine/dmp/docs/{doc}").read()
            while True:
                try:
                    words = RegexpTokenizer(r'\w+').tokenize(self.remStopWordsOur(self.preprocessText(next(lines))))
                    for word in words:
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
