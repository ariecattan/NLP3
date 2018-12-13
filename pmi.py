import numpy as np
import sys
import math
import time
from utils import dict_to_file

start = time.time()

path = sys.argv[1] if len(sys.argv) > 1 else 'dependency_co-occurence'
print path

word_context = {}
word_norme = {}
total = 0.0
word_proba = {}
context_proba = {}
WORD_CONTEXT_THRESHOLD = 10


target_words = ['car', 'bus', 'hospital', 'hotel', 'gun', 'bomb', 'horse', 'fox', 'table', 'bowl' ,'guitar', 'piano']
#word_context is a matrix of pmi
#to compute pmi, i first calculate p(y|x) == p(context|word) and divide by p(y) == p(context)


def pmi(p_y_x, p_y):
    return np.log(p_y_x / p_y)

with open(path) as file:
    for line in file:
        count, word, context = line.split()
        if int(count) >= WORD_CONTEXT_THRESHOLD:
            if word not in word_context:
                word_context[word] = {}
            word_context[word][context] = float(count)
            context_proba[context] = context_proba.get(context, 0.0) + float(count)
            #word_context.get(word,{})[context] = counter


sum_context = sum(context_proba.itervalues())
for context in context_proba:
    context_proba[context] /= sum_context



for word, context_dic in word_context.items():
    norme = 0.0
    sum_values = sum(context_dic.itervalues())
    for context, count in context_dic.items():
        p_y_x = context_dic[context] / sum_values
        p_y = context_proba[context]
        context_dic[context] = pmi(p_y_x, p_y)
        norme += context_dic[context] ** 2
    word_norme[word] = math.sqrt(norme)



context_word = {}
for word, contexts in word_context.items():
    for context, pmi in contexts.items():
        if context not in context_word:
            context_word[context] = {}
        context_word[context][word] = pmi



language_size = len(word_context)
w2i = {word:i for i, word in enumerate(word_context)}
i2w = {i:word for word, i in w2i.items()}

end = time.time() - start

print "Loading file", end

def get_k_most_similar(word, k=20):
    words = np.zeros(language_size)
    for att, pmi1 in word_context[word].items():
        for word2 in context_word[att]:
            words[w2i[word2]] += pmi1 * word_context[word2][att]

    for i in xrange(len(words)):
        words[i] = words[i] / (word_norme[word] * word_norme[i2w[i]])

    #sims = np.argsort(words)[-(k+1):]
    sims = words.argsort()[::-1][:k + 1]
    sims_words = map(lambda x: i2w[x], sims)
    #distance = map(lambda x: words[x], sims)

    return sims_words[1:]


def similarity(word1, word2):
    numerator = 0.0
    for att, count in word_context[word1].items():
        numerator += count * word_context[word2].get(att, 0)
    denominator = word_norme[word1] * word_norme[word2]

    return numerator / denominator


def get_k_most_context(word, k=20):
    pmis = np.zeros(len(word_context[word]))
    c2i = {context: i for i, context in enumerate(word_context[word])}
    i2c = {i: context for context, i in c2i.items()}


    for context, idx in c2i.items():
        pmis[idx] = word_context[word][context]

    sims = pmis.argsort()[::-1][:k + 1]
    sims_words = map(lambda x: i2c[x], sims)
    return sims_words

if __name__ == '__main__':


    cosine = {}
    att = {}
    for word in target_words:
        cosine[word] = get_k_most_similar(word)
        att[word] = get_k_most_context(word)

    fname, _ = path.split('_')
    #dict_to_file(cosine, 'sim/sim_' + fname + '.txt')
    #dict_to_file(att, 'att/att_' + fname + '.txt')
