#!/usr/bin/python3.11.8

from   numpy.linalg             import norm
from   numpy                    import dot, array
from   itertools                import combinations
import sqlite3

class CosineSimilarity(object):

    def __init__(self) -> None:
        self.databse      = sqlite3.connect("termDoc.db")
        self.cursor       = self.databse.cursor()
        self.tables       = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        self.cosineSim    = array([[1.0 for i in range(20)] for i in range(20)])
        self.cosineDis    = array([[1.0 for i in range(20)] for i in range(20)])

    def documentCombinations(self) -> list:
        docComb = list(combinations([f[0] for f in self.tables], 2))        
        return docComb

    def vectorization(self, doc_x, doc_y) -> tuple:
        frequencies = self.cursor.execute(f"SELECT {doc_x}.frequency, {doc_y}.frequency FROM {doc_x} INNER JOIN {doc_y} ON {doc_x}.term = {doc_y}.term").fetchall()
        doc_x = array([f[0] for f in frequencies], dtype='i')        
        doc_y = array([f[1] for f in frequencies], dtype='i')        
        return (doc_x, doc_y)

    def cosineSimilarityAndDistance(self):
        for comb in self.documentCombinations():
            vector = self.vectorization(comb[0], comb[1])
            cosineSimilarity  = dot(vector[0], vector[1])/((norm(vector[0]))*(norm(vector[1])))
            self.cosineSim[int(comb[0][3:])-1][int(comb[1][3:])-1] = cosineSimilarity
            self.cosineSim[int(comb[1][3:])-1][int(comb[0][3:])-1] = cosineSimilarity
            self.cosineDis[int(comb[0][3:])-1][int(comb[1][3:])-1] = 1 - cosineSimilarity
            self.cosineDis[int(comb[1][3:])-1][int(comb[0][3:])-1] = 1 - cosineSimilarity 

    def dataToCsv(self, data, name):
        with open(name+'.csv', 'w') as file:
            for i in range(0, 20):
                file.write(f"{i},")
            file.write("\n")
            for _ in data:
                for __ in _:
                    file.write(f"{__},")
                file.write('\n')
            file.close()

def main():
    ins = CosineSimilarity()
    ins.cosineSimilarityAndDistance()
    ins.dataToCsv(ins.cosineDis, "cosineDis")
    ins.dataToCsv(ins.cosineSim, "cosineSim")

if __name__ == "__main__":
    main()    