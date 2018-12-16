# NLP3


* To extract the features, run the command

`python extract_features.py train_file [-option]`

option can be '-s' for sentence co-occurrence, '-w' for window, '-d' for dependency
or -all for all of them

The program will create a file which contains a list of word context pairs according to the co-occurrence type



* To compute PMI values and 1st-order and 2nd-order similarities, run the command

`python pmi.py feature_file`

feature_file is the file created by the above command


* To load word2vec vectors and compute 1st-order and 2nd-order similarities, run the command:

`python word2vec.py vocabFile contextFile`

