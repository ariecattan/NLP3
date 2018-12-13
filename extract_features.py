import numpy as np
from collections import defaultdict, Counter
import sys
import time

start = time.time()

THRESHOLD = 100
CONTEXT_THRESHOLD = 20

window = 2
functional_pos = ['dt', 'in', 'to', 'cc', 'rb', 'prp', 'prp$', 'md', 'wdt', 'pos', 'wrb', '.', "''", '``', '(', ')', ',', ':', '$']

path = sys.argv[1] if len(sys.argv) > 1 else 'data/wikipedia.sample.trees.lemmatized'
type = sys.argv[2] if len(sys.argv) > 2 else '-d'

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
            dict = {"ID": ID, "LEMMA": LEMMA, "CPOSTAG": CPOSTAG, "HEAD": HEAD, "DEPREL":DEPREL }

            if LEMMA not in ('.', ','):
                sentence.append(dict)
                counts[LEMMA] = counts.get(LEMMA, 0) + 1

end = time.time() - start
print "Loading file", end

start = time.time()

words_to_compute = {word:count for word, count in counts.items() if count > THRESHOLD}
w2i = {word:i for i, word in enumerate(words_to_compute)}
i2w = {i:word for word, i in w2i.items()}

end = time.time() - start
print 'Create dict : ', end


def dict_to_file(dic, fname):
    start = time.time()
    dic_file = open(fname,'w')
    for key, label in dic.items():
        dic_file.write(str(label) + ' ' + key + '\n')

    end = time.time() - start
    print "Saving file", end

def filter_window(window):
    output = []
    for word_dic in window:
        lemma, pos = word_dic['LEMMA'], word_dic['CPOSTAG']
        if counts[lemma] > CONTEXT_THRESHOLD: #and pos not in functional_pos:
            output.append(lemma)
    return list(set(output))

def filter_functional_words(sentence):
    output = []
    for word_dic in sentence:
        if word_dic['CPOSTAG'] not in functional_pos:
            output.append(word_dic)
    return output

def filter_dependendy_threshold(sentence):
    output = []
    for word_dic in sentence:
        lemma = word_dic['LEMMA']
        if counts[lemma] > CONTEXT_THRESHOLD: #and pos not in functional_pos:
            output.append(word_dic)
    return output

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
    start = time.time()

    lemma_window = {}
    for sentence in all_sentences:
        sentence = filter_functional_words(sentence)
        for i in xrange(len(sentence)):
            word_dic = sentence[i]
            lemma = word_dic['LEMMA']
            if lemma in w2i:
                contexts = sentence[i-k:i] + sentence[i+1:i+1+k]
                contexts = filter_window(contexts)
                for context in contexts:
                    lemma_window[lemma + ' ' + context] = lemma_window.get(lemma + ' ' + context, 0) + 1

    end = time.time() - start
    print "Co-occurence word in window", end

    return lemma_window


def sentence_to_dependency_features(all_sentences):
    start = time.time()

    dependency_features = {}
    for sentence in all_sentences:
        for word_dic in sentence:
            id, lemma, head, deprel = word_dic['ID'], word_dic['LEMMA'], word_dic['HEAD'], word_dic['DEPREL']
            if lemma in w2i:
                contexts = [x for x in sentence if x['LEMMA'] != lemma and (x['HEAD'] == id or x['ID'] == head)]
                contexts = filter_dependendy_threshold(contexts)
                for feature_dic in contexts:
                    lemma_parent = True if id == feature_dic['HEAD'] else False
                    direction = 'left' if lemma_parent else 'right'
                    edge_label = feature_dic['DEPREL'] if lemma_parent else deprel
                    feature = lemma + ' ' + feature_dic['LEMMA'] + '_' + edge_label + '_' + direction
                    dependency_features[feature] = dependency_features.get(feature, 0) + 1


                    if feature_dic['CPOSTAG'] == 'in' and lemma_parent:
                        dependencies = [x for x in sentence if x['HEAD'] == feature_dic['ID'] and x['CPOSTAG'] not in functional_pos]
                        for dep in dependencies:
                            feature = lemma + ' ' + dep['LEMMA'] + '_' + feature_dic['DEPREL'] + '_' + feature_dic['LEMMA'] + '_left'
                            dependency_features[feature] = dependency_features.get(feature, 0) + 1



                    elif feature_dic['CPOSTAG'] == 'in' and lemma_parent is False:
                        dependencies = [x for x in sentence if x['ID'] == feature_dic['HEAD'] and x['CPOSTAG'] not in functional_pos]
                        for dep in dependencies:
                            feature = lemma + ' ' + dep['LEMMA'] + '_' + feature_dic['DEPREL'] + '_' + feature_dic['LEMMA'] + '_right'
                            dependency_features[feature] = dependency_features.get(feature, 0) + 1
                    


    end = time.time() - start
    print "Dependency", end

    return dependency_features


if __name__=='__main__':

    if type == '-s' or type == '-all':
        by_sentence = sentence_to_features(sentences)
        dict_to_file(by_sentence, 'sentence_co-occurence')
        by_sentence = {}

    if type == '-w' or type == '-all':
        by_window = sentence_to_window_feature(sentences, window)
        dict_to_file(by_window, 'window_co-occurence')
        by_window = {}

    if type == '-d' or type == '-all':
        by_dependency = sentence_to_dependency_features(sentences)
        dict_to_file(by_dependency, 'dependency_co-occurence')
        by_dependency = {}

