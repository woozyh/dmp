# dmp
## how it works?
As first thing we must do is to calculate the term doument matrix for our  dataset which done by <a href='https://github.com/woozyh/dmp/tree/main/lib'> buildMatrix.py and fileReader.py </a>, The file reader module read files in memory friendly way. The second step is calculation of similarity beweent docs (consine similarity) which done by <a href='https://github.com/woozyh/dmp/tree/main/src'> cosineSimilarity.py</a> 
## Benefits
We must know what we want, the first thing we want was to calculate the term document matrix from our documents in order to pass other phases, to calculate termDoc matrix we decide to store our matrix in a Relational DBMS, but why? <br> 1. parallel processing (think you are working on dynamic datas and suddenly you get a requst to calculate) <br> 2. incremental working (in each state you can check your docs while other docs are merging to db) <br> 3. performance (this method is ram/cpu friendly, but lazy depending on your storing hardware) <br> 4. accuracy


## 