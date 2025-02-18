import numpy as np 
import pickle
import lda

vocab = open("vocab.enron.txt").read().splitlines()
doc_raw = open("docword.enron.txt").read().splitlines()[3:]

kos = []
curr_doc = 1
curr_array = np.zeros(len(vocab), dtype=int)
count = 0

for line in doc_raw:
	fields = line.split(" ")
	doc_num = int(fields[0])
	vocab_num = int(fields[1]) - 1
	freq = int(fields[2])
	if doc_num != curr_doc:
		kos += [curr_array]
		curr_array = np.zeros(len(vocab), dtype=int)
		curr_doc = doc_num
		curr_array[vocab_num] = freq
	else:
		curr_array[vocab_num] = freq
	print count
	count += 1

kos = np.array(kos)

print "\n\ntraining\n\n"

curr_MLE = -99999999999
curr_model = None

for i in range(3, 12):
	model = lda.LDA(n_topics=i, n_iter=300, random_state=1)
	model.fit(kos)
	print "RES::::::"
	print "current topic: " + str(i)
	print model.loglikelihoods_[-1]
	topic_word = model.topic_word_
	n_top_words = 8

	for i, topic_dist in enumerate(topic_word):
		topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
		print('Topic {}: {}'.format(i, ' '.join(topic_words)))

	if model.loglikelihoods_[-1] > curr_MLE:
		print "WE BEAT THE PREV MODEL"
		curr_model = model
		curr_MLE = model.loglikelihoods_[-1]

print "displaying result"

print "DONNNEEEEEE\n\n\n\n\n\n"
topic_word = curr_model.topic_word_
n_top_words = 8

for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))

