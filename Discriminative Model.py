import string
import numpy as np
import nltk
import re
import sys
import glob
import errno

end = '!.?'


def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^:\n]*[:][^\n]*', '', text)
    for char in string.punctuation:
        if char != '.':
            text = text.replace(char, "")
    text = ''.join([i for i in text if not i.isdigit()])
    text = text.strip()
    # text = np.asarray(nltk.word_tokenize(text))
    return text


def unigram(tokens):
    d = {}
    total = len(tokens)
    for token in tokens:
        if token in d:
            d[token] += 1
        else:
            d[token] = 1
    for key in d:
        d[key] /= float(total)

    return d


def bigram(tokens):
    d = {}
    rev_d = {}
    leng = 0
    values = np.asarray([])

    # Assigns each token an ID.
    # Create a list of unique tokens
    for token in tokens:
        if token not in d:
            values = np.append(values, token)
            d[token] = leng
            rev_d[leng] = token
            leng += 1
    print("Number of types = ", len(d))

    # The bigram table which will store the probability and count information is declared anf filled here
    db = np.zeros([leng, leng])
    prev = '.'
    for token in tokens:
        db[d[prev]][d[token]] += 1
        prev = token

    # Handling the case when the last token's probability doesn't add to one
    x = (tokens.shape[0])
    db[d[tokens[x - 1]]][d['.']] += 1

    # Applying laplace smoothening
    for i in range(leng):
        add = np.sum(db[i])
        for j in range(leng):
            db[i][j] = ((db[i][j] + 1)*add )/(add + leng)

    # Converting the count table into a probability table
    for i in range(leng):
        add = np.sum(db[i])
        for j in range(leng):
            db[i][j] /= add

    return db, d


def probability(sentence, data_tokens, uni_p, bi_p, dick ):
    input_tokens = np.asarray(nltk.word_tokenize(sentence))
    base_p = 0.00000000001

    if input_tokens[0] not in uni_p:
        p = base_p
    else:
        p = uni_p[input_tokens[0]]

    prev = input_tokens[0]
    for i in range(1, len(input_tokens) ):
        if input_tokens[i] not in dick:
            p *= base_p
        elif prev not in dick:
            p *= uni_p[input_tokens[i]]
        else:
            p *= bi_p[ dick[prev] ][ dick[input_tokens[i]] ]
    return p


def classify(sentence):
    db1, db2 = None, None
    p1 = probability(sentence, db1)
    p2 = probability(sentence, db2)

    if p1 > p2:
        print("First Group")
    else:
        print("Second Group")


def graphics():
    path = '/home/nishantsinha15/Documents/sem7/Natural Language Processing/Assignment 3/20_newsgroups/comp.graphics/*'
    files = glob.glob(path)
    article = ""
    count = 0
    for name in files:  # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name, 'r') as f:  # No need to specify 'r': this is the default.
                # print("name = ", name)
                x = str(f.read())
                x = preprocess(x)
                article += '\n' + x
                count += len(x)
        except IOError as exc:
            if exc.errno != errno.EISDIR:  # Do not fail if a directory is found, just ignore it.
                raise  # Propagate other kinds of IOError.
    tokens = np.asarray(nltk.word_tokenize(article))
    return tokens


def motorcycles():
    path = '/home/nishantsinha15/Documents/sem7/Natural Language Processing/Assignment 3/20_newsgroups/rec.motorcycles/*'
    files = glob.glob(path)
    article = ""
    count = 0
    for name in files:  # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name, 'r') as f:  # No need to specify 'r': this is the default.
                # print("name = ", name)
                x = str(f.read())
                x = preprocess(x)
                article += '\n' + x
                count += len(x)
        except IOError as exc:
            if exc.errno != errno.EISDIR:  # Do not fail if a directory is found, just ignore it.
                raise  # Propagate other kinds of IOError.
    tokens = np.asarray(nltk.word_tokenize(article))
    return tokens


def main():
    n = int(input())
    sentences = []
    for i in range(n):
        sentence = input()
        for char in string.punctuation:
            sentence = sentence.replace(char, "")
        sentences.append(sentence)

    p1 = 0.0
    p2 = 0.0

    print("Woreking on Bikes")
    motor_tokens = motorcycles()
    print("Model tokenized")
    uni_p = unigram(motor_tokens)
    print("Unigrtam Model created")
    bi_p, dick = bigram(motor_tokens)
    print("Bigram model created")
    for sentence in sentences:
        p1 = probability(sentence, motor_tokens, uni_p, bi_p, dick)

    print("Woreking on Graphics")
    graphic_tokens = graphics()
    print("Model tokenized")
    uni_p = unigram(graphic_tokens)
    print("Unigrtam Model created")
    bi_p, dick = bigram(graphic_tokens)
    print("Bigram model created")
    for sentence in sentences:
        p2 =  probability(sentence, graphic_tokens, uni_p, bi_p, dick)

    print(p1, p2)
    if p1 > p2:
        print('Motorcycle')
    else:
        print('Graphics')

main()
