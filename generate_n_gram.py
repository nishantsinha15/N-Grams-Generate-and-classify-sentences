import string
import numpy as np
import nltk
import re


def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^:\n]*[:][^\n]*','', text)
    text = text.strip()
    # print(text)
    a = string.punctuation
    b = '!,.;?@'
    for char in a:
        if char not in b:
            text = text.replace(char, " ")

    text = ''.join([i for i in text if not i.isdigit()])
    text = np.asarray(nltk.word_tokenize(text))
    return text


def bigram(tokens):
    d = {}
    rev_d = {}
    leng = 0
    values = np.asarray([])
    for token in tokens:
        if token not in d:
            values = np.append(values, token)
            d[token] = leng
            rev_d[leng] = token
            # print(len, " - ", token)
            leng += 1
    print("Types = ", len(d))
    db = np.zeros([leng, leng])
    prev = '.'
    for token in tokens:
        db[d[prev]][d[token]]+=1
        prev = token
    x = (tokens.shape[0])
    # print("Dimension is", x)

    db[ d[tokens[x-1]] ][ d['.'] ]  += 1
    # print(db)

    for i in range(leng):
        add = np.sum(db[i])
        # print(add)
        if add == 0:
            print( rev_d[i] )
        for j in range(leng):
            db[i][j]/=add

    # print(db)

    prev = '.'
    end = '!.?'
    flag = True
    while prev not in end or flag:
        flag = False
        i = np.random.choice(values , p=db[d[prev]])
        print( i, end = " " )
        prev = i
    flag = True
    prev = '?'
    while prev not in end or flag:
        flag = False
        i = np.random.choice(values , p=db[d[prev]])
        print( i, end = " " )
        prev = i


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

    c = 'a'
    end = '!.?'
    while c not in end:
        c = np.random.choice(values, p=p)
        print(c, end=" ")
    c = 'a'
    while c not in end:
        c = np.random.choice(values, p=p)
        print(c, end=" ")
    print()


# file_name = "37913"
# f = open(file_name, "r")
# article = str(f.read())

import sys
import glob
import errno

path = '/home/nishantsinha15/Documents/sem7/Natural Language Processing/Assignment 3/20_newsgroups/comp.graphics/*'
files = glob.glob(path)
article = ""
count = 0
for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
    try:
        with open(name, 'r') as f: # No need to specify 'r': this is the default.
            print("name - ", name)
            x = str(f.read())
            x = x.lower()
            x = re.sub(r'[^:\n]*[:][^\n]*', '', x)
            x = x.strip()
            article += '\n' + (x)
            count += len(x)
    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            raise # Propagate other kinds of IOError.

print(count)

# 2238187
tokens = preprocess(article)
print("Preprocessing complete. Tokens found = ",tokens.shape )
# unigram(tokens)
# bigram(tokens)
