import numpy as np
import sys

WORD_CONTEXT_THRESHOLD = 10

path = sys.argv[1] #'window_co-occurence'

word_context = {}

with open(path) as file:
    for line in file:
        count, word, context = line.split()
        if int(count) >= WORD_CONTEXT_THRESHOLD:
            if word not in word_context:
                word_context[word] = {}
            word_context[word][context] = float(count)
            #word_context.get(word,{})[context] = counter



context_word = {}
for word, contexts in word_context.items():
    for context, count in contexts.items():
        if context not in context_word:
            context_word[context] = {}
        context_word[context][word] = count



total = 0.0
word_proba = {}

for word, contexts in word_context.items():
    word_count = sum(contexts.itervalues())
    for context in contexts:
        contexts[context] /= word_count

    word_proba[word] = word_count
    total += word_count



for word, count in word_proba.items():
    word_proba[word] /= total




