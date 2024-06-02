#!/usr/bin/python3.11.8

from numpy                   import sort, unique, zeros, column_stack
from sklearn.cluster         import KMeans, DBSCAN, AgglomerativeClustering
from src.cosineSimilarity    import CosineSimilarity
from matplotlib.pyplot       import plot, scatter, show, xlabel, ylabel, title
from sklearn.decomposition   import PCA
from sklearn.neighbors       import NearestNeighbors
from scipy.cluster.hierarchy import dendrogram

class preProcessingData(object):
    
    MATRIX = CosineSimilarity()
    MATRIX.cosineSimilarityAndDistance()
    
    def __init__(self) -> None:
        self.pca              = PCA(2)
        self.cosineSimilarity = self.MATRIX.cosineSim
        self.transform        = self.pca.fit_transform(self.cosineSimilarity)

class partitioning(preProcessingData):

    def __init__(self) -> None:
        super().__init__()
        
    def bestK(self):
        inertias = []
        for i in range(1, 10):
            kmeans = KMeans(n_clusters=i)
            kmeans.fit(self.cosineSimilarity)
            inertias.append(kmeans.inertia_)
        plot(range(1, 10), inertias)
        title("elbow methon for finding best K")
        xlabel('Number of clusters')
        ylabel('Inertia')
        show()

    def kmeans(self):
        self.kmeans    = KMeans(n_clusters=3)
        self.label     = self.kmeans.fit_predict(self.transform)
        self.u_labels  = unique(self.label)
        self.centroids = self.kmeans.cluster_centers_
        
    def draw(self):
        for i in self.u_labels:
            scatter(self.transform[self.label == i, 0], self.transform[self.label == i, 1], label = i)
        scatter(self.kmeans.cluster_centers_[:, 0], self.kmeans.cluster_centers_[:, 1], color='black', marker='*', label='centroid')
        title("KMeans")
        show()

class hierarchical(preProcessingData):

    def __init__(self) -> None:
        super().__init__()

    def agg(self):
        self.aggmo = AgglomerativeClustering(n_clusters=3, compute_distances=True)
        self.label = self.aggmo.fit_predict(self.transform)
        self.u_labels = unique(self.label)

    def draw(self):
        print(self.aggmo.children_)
        print(self.aggmo.distances_)
        counts = zeros(self.aggmo.children_.shape[0])
        n_samples = len(self.aggmo.labels_)
        for i, merge in enumerate(self.aggmo.children_):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count
        linkage_matrix = column_stack([self.aggmo.children_, self.aggmo.distances_, counts]).astype(float)
        dendrogram(linkage_matrix, truncate_mode="level", p=3)
        title("Agglomerative")
        xlabel("dendrogram")
        show()

class density(preProcessingData):

    def __init__(self) -> None:
        super().__init__()

    def bestEPS(self):
        neighbors          = NearestNeighbors(n_neighbors=3)
        neighbors_fit      = neighbors.fit(self.cosineSimilarity)
        distances, indices = neighbors_fit.kneighbors(self.cosineSimilarity)
        distances          = sort(distances, axis=0)
        distances          = distances[:,1]
        plot(distances)
        title("best eps")
        show()
        
    def dbscan(self):
        self.db     = DBSCAN(eps=0.36, min_samples=1)
        self.label = self.db.fit_predict(self.transform)
        self.u_labels = unique(self.label)

    def draw(self):
        for i in self.u_labels:
            scatter(self.transform[self.label == i, 0], self.transform[self.label == i, 1], label = i)
        title("DBscan")
        show()

def main():

    partition = partitioning()
    partition.bestK()
    partition.kmeans()
    partition.draw()

    hierarchy = hierarchical()
    hierarchy.agg()
    hierarchy.draw()

    dens = density()
    dens.bestEPS()
    dens.dbscan()
    dens.draw()

if __name__ == "__main__":
    main()
