# Detection of Topic Structure of the Guardian's Webpages based on Network Analysis

This repository contains code used for MSc Project for Web Science and Big Data Analytics by Patorn Utenpattanun, University College London.

# Main Package Requirements

* jupyter python to open the ipython notebook
* Python 3.5.0
* igraph (Network)
* scipy
* scikit-learn
* gensim (LDA)
* Vowpal Wabbit (LDA)

# Other Requirements
* nltk
* matplotlib
* numpy
* pandas
* seaborn
* request
* palmetto (CV Topic Coherence)

# Files
Follow the ipython notebook to complete the tasks.

### task1.ipynb

Task 1 is to create a document network and find the network communities. We use the result of Louvain modularity to compare with the results from Hierarchical Clustering and K-means.

### task2.ipynb

For Task 2, we find the topic words extracted from the network-based method and also find topics and topic words with LDA.

### /results

This folder contains the results of various tasks including TF-IDF vectors, Network Preprocessing, LDA, and etc. that used in this project. In order to reproduce the same results, use the data in the folder.
