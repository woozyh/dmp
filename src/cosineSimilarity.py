#!/usr/bin/python3.11.8
from numpy.linalg import norm
from numpy        import dot, array
from itertools    import combinations
import sqlite3

class CosineSimilarity(object):

    def __init__(self) -> None:
        self.databse = sqlite3.connect("termDoc.db")
        self.cursor  = self.databse.cursor()
        self.tables  = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

    def documentCombinations(self) -> list:
        docComb = list(combinations([f[0] for f in self.tables], 2))        
        return docComb
    
    def vectorization(self, doc_x, doc_y) -> tuple:
        frequencies = self.cursor.execute(f"SELECT {doc_x}.frequency, {doc_y}.frequency FROM {doc_x} INNER JOIN {doc_y} ON {doc_x}.term = {doc_y}.term").fetchall()
        doc_x = array([f[0] for f in frequencies])        
        doc_y = array([f[1] for f in frequencies])        
        return (doc_x, doc_y)

    def cosineSimilarity(self):
        for comb in self.documentCombinations():
            vector = self.vectorization(comb[0], comb[1])
            cosineSimilarity = dot(vector[0], vector[1])/((norm(vector[0]))*(norm(vector[1])))
            print(f"cosine similarity for {comb}: {cosineSimilarity}")
        # self.databse.close()
        # self.cursor.close()

def main():
    ins = CosineSimilarity()
    ins.cosineSimilarity()

if __name__ == "__main__":
    main()
    