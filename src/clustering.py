#!/usr/bin/python3.11.8

from   matplotlib.pyplot     import scatter, show, xlabel, ylabel
from   cosineSimilarity      import CosineSimilarity
from   sklearn.cluster       import KMeans, DBSCAN, AgglomerativeClustering

MATRIX = CosineSimilarity()
MATRIX.cosineSimilarityAndDistance()

class partitioning(object):

    def __init__(self) -> None:
        self.cosineSimilarity = MATRIX.cosineSim

    def bestK(self):
        inertias = []
        for i in range(1,21):
            kmeans = KMeans(n_clusters=i)
            kmeans.fit(self.cosineSimilarity)
            inertias.append(kmeans.inertia_)

        scatter(range(1, 21), inertias, marker='o')
        xlabel('Number of clusters')
        ylabel('Inertia')
        show()

    def kmeans(self):
        self.kmeans    = KMeans(n_clusters=11).fit(self.cosineSimilarity)
        self.centroids = self.kmeans.cluster_centers_
        
    def draw(self):
        for i in range(12):
            scatter(self.centroids[:, i], self.centroids[:, i+1])
        show()


class hierarichal(object):

    def __init__(self) -> None:
        self.cosineSimilarity = MATRIX.cosineDis
        pass

    def dbscan(self):
        self.db = DBSCAN(eps=0.9, min_samples=2).fit(self.cosineSimilarity)
        print(self.db.labels_)
        pass

    def agg(self):
        self.ag = AgglomerativeClustering(3).fit_predict(self.cosineSimilarity)
        print(self.ag)   
        pass

def main():
    ins = partitioning()
    ins.bestK()
    ins.kmeans()
    ins.draw()

if __name__ == "__main__":
    main()
