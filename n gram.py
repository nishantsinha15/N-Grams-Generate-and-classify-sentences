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
    a = string.punctuation
    b = '!,.;?@'
    for char in a:
        if char not in b:
            text = text.replace(char, " ")
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

    values = np.asarray([])
    p = np.asarray([])
    for key in d:
        values = np.append(values, key)
        p = np.append(p, d[key] / float(total))

    #generating sentences
    c = 'a'
    print("Unigram 1: ", end = " ")
    while c not in end:
        c = np.random.choice(values, p=p)
        print(c, end=" ")
    print("\nUnigram 2: ", end = " ")
    c = 'a'
    while c not in end:
        c = np.random.choice(values, p=p)
        print(c, end=" ")
    print()


def bigram(token_list):
    probability = {}
    val = {}
    p = {}
    for word in token_list:
        probability[word] = {}
        val[word] = []
        p[word] = []

    prev = '.'
    for token in token_list:
        if token in probability[prev]:
            probability[prev][token] += 1
        else:
            probability[prev][token] = 1
        prev = token

    if '.' in probability[prev]:
        probability[prev]['.'] += 1
    else:
        probability[prev]['.'] = 1


    for key in probability:
        div = 0
        for subkey in probability[key]:
            div += probability[key][subkey]

        for subkey in probability[key]:
            probability[key][subkey] /= div
            val[key].append(subkey)
            p[key].append(probability[key][subkey])

    prev = '.'
    flag = True
    while prev not in end or flag:
        prev = np.random.choice(val[prev], p = p[prev])
        print(prev, end = " ")
        flag = False
    print()

    prev = '.'
    flag = True
    while prev not in end or flag:
        prev = np.random.choice(val[prev], p=p[prev])
        print(prev, end=" ")
        flag = False
    print()

def graphics():
    path = '/home/nishantsinha15/Documents/sem7/Natural Language Processing/Assignment 3/20_newsgroups/comp.graphics/*'
    files = glob.glob(path)
    article = ""
    count = 0
    for name in files:  # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name, 'r') as f:  # No need to specify 'r': this is the default.
                print("name = ", name)
                x = str(f.read())
                x = preprocess(x)
                article += '\n' + x
                count += len(x)
        except IOError as exc:
            if exc.errno != errno.EISDIR:  # Do not fail if a directory is found, just ignore it.
                raise  # Propagate other kinds of IOError.
    tokens = np.asarray(nltk.word_tokenize(article))
    unigram(tokens)
    bigram(tokens)


graphics()
