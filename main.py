from src.clustering import partitioning, hierarchical, density

def main():

    partition = partitioning()
    partition.bestK()
    partition.kmeans()
    partition.draw()

    dens = density()
    dens.bestEPS()
    dens.dbscan()
    dens.draw()

    hierarchy = hierarchical()
    hierarchy.agg()
    hierarchy.draw()
    
if __name__ == "__main__":
    main()