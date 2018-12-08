# generate-and-classify-sentences
Your task in this assignment is to write a python program that will be able to generate and classify sentences based on some corpus.

## Data set link:
https://archive.ics.uci.edu/ml/datasets/Twenty+Newsgroups

## Generative Model
1. Unigram
2. Bigram
3. Trigram (Used Laplace smoothing)

## Discriminative Model
Trained my model on the given dataset(Trigrams using Laplace Smoothing). For testing, given a sentence it will predict which class does it fall into using the trigram probability. Unknown words are also handled using UNK tag. 
