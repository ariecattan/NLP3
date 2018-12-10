import numpy as np
from collections import defaultdict, Counter
import sys
import time

start = time.time()

THRESHOLD = 100
CONTEXT_THRESHOLD = 50

window = 2
functional_pos = ['dt', 'in', 'to', 'cc', 'rb', 'prp', 'prp$', '.']

path = sys.argv[1]

counts = {}
sentences = []

with open(path) as file:
    sentence = []
    for line in file:
        line = line.strip().lower()
        if line == "":
            sentences.append(sentence)
            sentence = []
        else:
            ID, FORM, LEMMA, CPOSTAG, POSTAG, FEATS, HEAD, DEPREL, PHEAD, PDEPREL = line.split("\t")
            dict = {"ID": ID, "LEMMA": LEMMA, "CPOSTAG": CPOSTAG}
            sentence.append(dict)
            counts[LEMMA] = counts.get(LEMMA, 0) + 1

end = time.time() - start
print "Loaded file", end

start = time.time()

words_to_compute = {word:count for word, count in counts.items() if count > THRESHOLD}

w2i = {word:i for i, word in enumerate(words_to_compute)}
del w2i['.']
del w2i[',']
i2w = {i:word for word, i in w2i.items()}

end = time.time() - start
print 'Create dict : ', end


def dict_to_file(dic, fname):
    dic_file = open(fname,'w')
    for key, label in dic.items():
        dic_file.write(str(label) + ' ' + key + '\n')

def filter_window(window):
    output = []
    for word_dic in window:
        lemma, pos = word_dic['LEMMA'], word_dic['CPOSTAG']
        if counts[lemma] > CONTEXT_THRESHOLD and pos not in functional_pos:
            output.append(lemma)
    return list(set(output))


def sentence_to_features(all_sentences):
    start = time.time()

    lemma_context = {}
    for sentence in all_sentences:
        for word_dic in sentence:
            lemma, pos = word_dic['LEMMA'], word_dic['CPOSTAG']
            if lemma in w2i:
                contexts = [x for x in sentence if x['LEMMA'] != lemma]
                contexts = filter_window(contexts)
                for context in contexts:
                    lemma_context[lemma + ' ' + context] = lemma_context.get(lemma + ' ' + context, 0) + 1

    end = time.time() - start
    print "Co-occurence word in sentence", end

    return lemma_context


def sentence_to_window_feature(all_sentences, k):
    #k is the number of context in each side of the word

    lemma_window = {}
    for sentence in all_sentences:
        for i in xrange(len(sentence)):
            word_dic = sentence[i]
            lemma = word_dic['LEMMA']
            if lemma in w2i:
                contexts = sentence[i-k:i] + sentence[i+1:i+1+k]
                contexts = filter_window(contexts)
                for context in contexts:
                    lemma_window[lemma + ' ' + context] = lemma_window.get(lemma + ' ' + context, 0) + 1
    return lemma_window



if __name__=='__main__':

    by_sentence = sentence_to_features(sentences)
    dict_to_file(by_sentence, 'sentence_co-occurence')


    by_window = []
    by_dependency = []





        #by_window += sentence_to_window_feature(sentence, window)


    print 'Generate word-context : ' + str(time.time() - start)
    start = time.time()



    print 'Save sentences : ' + str(time.time() - start)
