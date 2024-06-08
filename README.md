# dmp
## how to run it?
* starting point is `lib/buildMatrix.py` and then after/while building your termDoc matrix you can run `main.py`.

##  how it works?
* As first thing we must do is to calculate the term doument matrix for our  dataset which done by [`buildMatrix.py and fileReader.py`](lib/) , The file reader module read files in memory friendly way. The second step is calculation of similarity beweent docs (consine similarity) which done by [`cosineSimilarity.py`](src/cosineSimilarity)

## Bulding the matrix with [buildMatrix.py](lib/buildMatrix.py)
* As we said we are storing our data on dbms so we need an architecture to satisfy the problem in this step. <hr>
### db schema
```python
class BuildMatrix(object):

    def __init__(self) -> None:
        self.stopWords = {....}
        try:
            self.database = sqlite3.connect("termDoc.db")
            self.cursor   = self.database.cursor()
            self.docs     = listdir("docs/")
            [self.cursor.execute(f"DROP TABLE IF EXISTS {doc[:-4]};") for doc in self.docs]
            [self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {doc[:-5]} (term text PRIMARY KEY, frequency int);") for doc in self.docs]
        except sqlite3.OperationalError as er:
           print(f"database Error: {er}")
```
* For each doument we create a table which named as document. (how?)
    * as our document is static we look for our docs in [docs/](docs/) which listed by listdir() >> it may be better if we do some walking on directories for our docs, but we keep it simpler.
    * the db's tables features contains one constraint(which is primary key and choosed from terms) and a frequency(int).
    <hr>
### text preprocessing
```python
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
```
* The buildMatrix() starts completing the termDoc matrix via getting each line of file and pass it to preprocessor and get the normal form of term in each line, to merge it into db.
    * the remStopWordOur(lineIn) && preprocessText(lineIn) preprocessors of lines. (is straigh enough to not discuss it)

## Calculation of CosineSimilarity with [cosineSimilrity.py](src/cosineSimilarity.py)
* The first thing to calculate cosine similarity is building a storage space to store it, we choose a 2D [20*20] array of integer (because of its static type the storage that it occupies decrease).
```python
class CosineSimilarity(object):

    def __init__(self) -> None:
        self.databse      = sqlite3.connect("termDoc.db")
        self.cursor       = self.databse.cursor()
        self.tables       = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        self.cosineSim    = array([[1.0 for i in range(20)] for i in range(20)])
        self.cosineDis    = array([[0.0 for i in range(20)] for i in range(20)])
```

* now it's time to read vectors from db and find the cosineSimilarity between vectors, but before jumping to get vectors you need a combination of vectors that you want. (how?)
```python
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
```
* as we see above the cosineSimilarityAndDistance() at first step calls the documentCombinations() to find the docs combinations and after that gets the pure vector of each doc in a way that we pass all sparse values away (more performance) and don't calculate them in our program, but there is one missing part and that is vectorization() the vectorization just execute the core query for finding the sparse less values between two vectors which comes from combination() after all again we get back to documentCombinations() to store the amounts. <hr>
```python
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
```
* In cosineSimilarity as a feature you can get the distance/similarity in csv. [just call it and pass the data you want to csv and then the name of file you want to store csv in it] <hr>

## Clustering from similarity matrix [clustering.py](src/clustering.py)
* In first step we need to call the matrix from cosineSimilarity.py which is the core data in this place, then as you must to know we need decomposition, but why?
    1. The first reason is for normalizing the data in a way that you can draw any graph, you will see at the end you observe the algorithm with a 2D graph so from now you must handle your data.
    2. As you see the [docs/](docs/) there is 20 docs so the matrix has 20*20 values which are mostly repeatedly (just 190 elements are unique) so you need to normalize it.
* As you can see below theses steps for each algorithm must done so we implement a base class and inherit from as we need.

```python
class preProcessingData(object):
    
    MATRIX = CosineSimilarity()
    MATRIX.cosineSimilarityAndDistance()
    
    def __init__(self) -> None:
        self.pca              = PCA(2)
        self.cosineSimilarity = self.MATRIX.cosineSim
        self.transform        = self.pca.fit_transform(self.cosineSimilarity)
```

#### KMeans clustering (base on partitioning)
* In first step to run KMeans is to find the best K value, which in there done by bestk(). (also known as elbow method)
```python
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
```
* In second step we process kmeans on our data with best k values, then passing the transformed (docomposited data with PCA) data to kmeans to get labels. after we go for unique lables because we don't wanna have repeated data in this steps (because it does't make any sense that two element of our data are same and we can't even figure it out while drawing graph because of over-writing), and at the end get the graph of our kmeans result to see what heppened in there. <hr>

#### Agglomerative clustering (base on hierarchical)
* As we discussed for KMeans again we need some preprocessing, The first thing we want pass the argument to process agglomerative on decomposited data.

```python
class hierarchical(preProcessingData):

    def __init__(self) -> None:
        super().__init__()

    def agg(self):
        self.aggmo = AgglomerativeClustering(n_clusters=3, compute_distances=True)
        self.label = self.aggmo.fit_predict(self.transform)
        self.u_labels = unique(self.label)
        
    def draw(self):
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
```
* The difficulty in there is how to draw the dendogram?
    1. The first thing we must to do is finding the children and where the break points are.
    2. In second step we build a new matrix for linkage between nodes.

#### Dbscan clustering (base on density)
* Again we have some preprocessing in there, but the most important one is to calculate best(not always) eps for our algorithm in there which done by NearestNeighbors from sklearn.neighbors.

```python
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
```

## Benefits of our implementation
```
    1. parallel processing without any multithreading/parallelism with libraries (think you are working on dynamic datas and suddenly you get a requst to calculate)
    
    2. incremental working (in each state you can check your docs clusterig result while 
    other docs are merging to db)
    
    3. performance (this method is ram/cpu friendly, but lazy depending on your storing hardware)
    4. accuracy (nothing miss or crash)
 ```
