import numpy as np

#sent = np.loadtxt('sim/sim_sentence.txt', np.str)
window = np.loadtxt('word2vec/sim/bow5.txt', np.str)
dep = np.loadtxt('word2vec/sim/deps.txt', np.str)

#sent_car =[x[1:] for x in sent if x[0] == 'car']
#sent_car = sent_car[0]
window_car =[x[1:] for x in window if x[0] == 'car']
window_car = window_car[0]
dep_car =[x[1:] for x in dep if x[0] == 'car']
dep_car = dep_car[0]

#sent_piano =[x[1:] for x in sent if x[0] == 'piano']
#sent_piano = sent_piano[0]
window_piano =[x[1:] for x in window if x[0] == 'piano']
window_piano = window_piano[0]
dep_piano =[x[1:] for x in dep if x[0] == 'piano']
dep_piano = dep_piano[0]

car_judgment = np.loadtxt('word2vec/manually_judgment/word2vec_car_dist_judgment.txt', np.str)
piano_judgment = np.loadtxt('word2vec/manually_judgment/word2vec_piano_dist_judgment.txt', np.str)


def arr_to_dic(arr):
    dic_topic = {}
    dic_semantic = {}
    for x in arr:
        word, topic, semantic = x[0], x[1], x[2]
        dic_topic[word] = int(topic)
        dic_semantic[word] = int(semantic)

    return dic_topic, dic_semantic

def ap(idx, pred, gold):
    numerator = 0.0
    for i in xrange(0, idx + 1):
        word = pred[i]
        numerator += prec(i, pred, gold) * gold[word]
    return numerator / 20


def prec(idx, pred, gold):
    avg = 0.0
    for i in xrange(0, idx + 1):
        word = pred[i]
        avg += gold[word]
    return avg / (idx + 1)



if __name__ == '__main__':
    car_dic_topic, car_dic_semantic = arr_to_dic(car_judgment)
    piano_dic_topic, piano_dic_semantic = arr_to_dic(piano_judgment)


    #sent_car_map = sum([ap(i, sent_car, car_dic_topic) for i in xrange(20)]) / 20
    window_car_map = sum([ap(i, window_car, car_dic_semantic) for i in xrange(20)]) / 20
    dep_car_map = sum([ap(i, dep_car, car_dic_semantic) for i in xrange(20)]) / 20

    print window_car_map, dep_car_map

    #sent_piano_map = sum([ap(i, sent_piano, piano_dic_topic) for i in xrange(20)]) / 20
    window_piano_map = sum([ap(i, window_piano, piano_dic_semantic) for i in xrange(20)]) / 20
    dep_piano_map = sum([ap(i, dep_piano, piano_dic_semantic) for i in xrange(20)]) / 20

    print window_piano_map, dep_piano_map
    
