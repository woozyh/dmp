#!/usr/bin/python3.11.8

from   cosineSimilarity      import CosineSimilarity
from   sklearn.cluster       import KMeans, DBSCAN
from   sklearn.decomposition import PCA
import pandas as pd

MATRIX = CosineSimilarity()
MATRIX.cosineSimilarityAndDistance()

class partitioning(object):

    def __init__(self) -> None:
        self.cosineDis = MATRIX.cosineDis
        self.pca       = PCA(len(self.cosineDis[0]))
        self.data      = self.pca.transform(self.cosineDis)
        pass

    def kmeans(self):
        pass

class hierarichal(object):

    def __init__(self) -> None:
        self.cosineDis = MATRIX.cosineDis
        pass

    def dbscan(self):
        pass

ins = partitioning()
ins.kmeans()
