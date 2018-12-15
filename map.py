import numpy as np

sent = np.loadtxt('sim/sim_sentence.txt', np.str)
window = np.loadtxt('sim/sim_window.txt', np.str)
dep = np.loadtxt('sim/sim_dependency.txt', np.str)

sent_car =[x[1:] for x in sent if x[0] == 'car']
window_car =[x[1:] for x in window if x[0] == 'car']
dep_car =[x[1:] for x in dep if x[0] == 'car']

sent_piano =[x[1:] for x in sent if x[0] == 'piano']
window_piano =[x[1:] for x in window if x[0] == 'piano']
dep_piano =[x[1:] for x in dep if x[0] == 'piano']

car_judgment = np.loadtxt('car_manually_judgment/dist_judgment.txt', np.str)
piano_judgment = np.loadtxt('piano_manually_judgment/dist_judgment.txt', np.str)




