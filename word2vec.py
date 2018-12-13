import numpy as np
import sys
from utils import dict_to_file
import time

start = time.time()

vocabFile = sys.argv[1] if len(sys.argv) >1 else 'data/deps.words'
contextFile = sys.argv[1] if len(sys.argv) >1 else 'data/deps.contexts'

w2i = {}
vocab = []

wordVectors = []

for i, line in enumerate(file(vocabFile)):
    line = line.split()
    word, vec = line[0], np.array(line[1:], dtype=float)
    w2i[word] = i
    vocab.append(word)
    wordVectors.append(vec)

wordVectors = np.array(wordVectors)
vocab = np.array(vocab)

c2i = {}
contexts = []
contextVectors = []

for i, line in enumerate(file(contextFile)):
    line = line.split()
    con, vec = line[0], np.array(line[1:], dtype=float)
    c2i[con] = i
    contexts.append(con)
    contextVectors.append(vec)

contextVectors = np.array(contextVectors)
contexts = np.array(contexts)


end = time.time() - start

print "Loading file", end

def get_k_most_similar(word, k=20):
    word_vec = wordVectors[w2i[word]]
    w = wordVectors.dot(word_vec)
    sims = w.argsort()[::-1][:k + 1]
    return vocab[sims[1:]]


def get_k_most_context(word, k=10):
    word_vec = wordVectors[w2i[word]]
    w = contextVectors.dot(word_vec)
    sims = w.argsort()[::-1][:k]
    return contexts[sims]


if __name__ == '__main__':

    target_words = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl', 'guitar',
                    'piano']


    word2vec_file = {}
    most_feature = {}

    for word in target_words:
        word2vec_file[word] = get_k_most_similar(word)
        most_feature[word] = get_k_most_context(word)

    dict_to_file(word2vec_file, 'word2vec/sim/deps.txt')
    dict_to_file(most_feature, 'word2vec/att/deps.txt')

