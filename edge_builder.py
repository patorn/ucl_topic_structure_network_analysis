from os import makedirs
from os.path import join, exists
import json
import nltk
import string
import os
import pdb
import csv

import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

def tokenize(text):
  tokens = nltk.word_tokenize(text)
  stems = []
  for item in tokens:
    stems.append(PorterStemmer().stem(item))
  return stems

def main():
  INPUT_DIR = join('tmp', 'parsed')
  OUTPUT_DIR = join('tmp')
  makedirs(OUTPUT_DIR, exist_ok=True)

  print("Building vocabulary...")

  token_dict = {}

  for fname in os.listdir(INPUT_DIR):
    print("Loading fname=", fname)
    if fname != '.DS_Store':
      with open(join(INPUT_DIR, fname), 'r') as f:
        data = json.load(f)
        text = data['body']
        table = str.maketrans({key: None for key in string.punctuation})
        token_dict[data['id']] = text.lower().translate(table)

  print("Processing TF-IDF")

  tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
  tfidf_matrix = tfidf.fit_transform(token_dict.values())

  G = nx.Graph()
  for i, key in enumerate(sorted(token_dict.keys())):
    print("Processing key=", key)
    similarities = cosine_similarity(tfidf_matrix[i], tfidf_matrix)[0]

    for i_2, key_2 in enumerate(token_dict.keys()):
      if i != i_2:
        G.add_edge(key, key_2, weight=similarities[i_2])

  result_fname = join(OUTPUT_DIR, 'edges.csv')
  f = open(result_fname, 'wt')
  try:
    writer = csv.writer(f)
    writer.writerow( ('From', 'To', 'Weight') )
    for edge in G.edges():
      writer.writerow( (edge[0], edge[1], G[edge[0]][edge[1]]['weight']) )
  finally:
    f.close()

if __name__ == "__main__":
  main()
