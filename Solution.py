'''

Name :- Siddharth Nahar
Entry No :- 2016csb1043
Date :- 17/11/18
Purpose :-

	1. PreProcessing of Train and Test Data
	2. Create Dictionary and Predict result,computing accuracies etc.

'''

from vocab import Vocab
import heapq
from math import log10
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------------------------

#Assigning Probablites to each Object in Dictionary

def assignProbablities(Vocabulary,countWordSpam,countWordHam,m):

	#m = len(Vocabulary)
	p = 1/m

	FreqSpamWords = list()
	FreqHamWords = list()

	for word, Obj in Vocabulary.items():

		probSpam, probHam = Obj.compute(m, p, countWordSpam, countWordHam)
		FreqSpamWords.append((probSpam,Obj.word))
		FreqHamWords.append((probHam,Obj.word))
	
	SpamTop = heapq.nlargest(5,FreqSpamWords)
	HamTop = heapq.nlargest(5,FreqHamWords)

	TopSpam = ""
	TopHam = ""

	for i in range(0,5):

		TopSpam += SpamTop[i][1] + ", "
		TopHam += HamTop[i][1] +", "

	print("Top 5 Words Contributing to Spam : "+TopSpam[:-2])
	print("Top 5 Words Contributing to Ham : "+TopHam[:-2])

	print("--------------------------------------------------------")

#------------------------------------------------------------------------------------------------


'''
1. m-estimate justifies confidence of user in value
2. Higher value m justifes user has more confidence in probablity value
3. Lower value represent low confidence in new probablity value
'''

#Plot m vs Accuracy graph
def Plot(X,Y):

	plt.plot(X,Y,'b--')
	plt.xlabel("m-values")
	plt.ylabel("Accuracy")
	plt.title("m-Values Vs Accuracy\n Naive Bayes Model")
	plt.gca().set_ylim([55,100])
	plt.savefig("m vs Accuracy")
	plt.show()

#------------------------------------------------------------------------------------------------

#Preprocess the train set and Returns created Dictionary
def preProcess():

	#Created dictionary stores word and it's corresponding Vocab Object
	Vocabulary = dict()

	filePtr = open('Data/nbctrain','r')
	#filePtr = open('train.txt','r')
	countSpam = 0
	countHam = 0

	countWordSpam = 0
	countWordHam = 0
	
	#Read Training file line by line
	for line in filePtr:

		isSpam = False

		#Remove Ending characters
		line = line.strip()

		#Split line by spaces
		line = line.split()

		if(line[1].strip() == 'spam'):
			isSpam = True
			countSpam = countSpam + 1
		else:
			countHam = countHam + 1

		#Iterate in spaces of two to get word and word-count
		for i in range(2, len(line), 2):

			word = line[i].strip()
			wordCount = int(line[i+1].strip())

			#If Vocabulary contains the word update freq count else insert it in vocab 
			if(word in Vocabulary):
				Vocabulary[word].update(wordCount, isSpam)
				#print('Hello')
			else:
				Obj = Vocab(word, wordCount, isSpam)
				Vocabulary[word] = Obj

			#If isSpam is True add Total WordCount in Spamming Words and viceversa
			if(isSpam == True):
				countWordSpam = countWordSpam + wordCount
			else:
				countWordHam = countWordHam + wordCount
	
	
	probSpam = countSpam/(countSpam + countHam)
	probHam = 1 - probSpam

	print("Prior Probablity of Spam P(Spam) = "+str(probSpam))
	print("Prior Probablity of Ham P(Ham) = "+str(probHam))

	print("----------------------------------------------------------------")
	m_array = np.linspace(1,100000000,1000,dtype = np.int32)
	result = list()

	'''
	for m in np.nditer(m_array):
	
		assignProbablities(Vocabulary,countWordSpam,countWordHam, m)
		Accu = TestAccuracy(Vocabulary, probSpam, probHam)
		print("For Value m = "+str(m)+" Accuracy : "+str(Accu))
		result.append(Accu)

	r_array = np.array(result)

	Plot(m_array,r_array)
	'''

	assignProbablities(Vocabulary,countWordSpam,countWordHam, len(Vocabulary))
	TestAccuracy(Vocabulary, probSpam, probHam)

#----------------------------------------------------------------------------------------------------

'''
1. Posteriror Probablity problem if new word is found in test Set then I just ignore that word
2. More Product of probablities tends towards zero so for numerical stablity use additions of log

*To modify emails to beat classifiers :

1. Bayesian Posining to produce spam emails use more amount of legitimate words,inncucus words to pass threshold of spam filter
2. Modify the more used spam word viagra to v!iagra or viaagra
3. Replace text with pictures.our filter can't read text from images
'''

#Tests Accuracy for Given Test Set
def TestAccuracy(Vocabulary, probSpam, probHam):

	filePtr = open('Data/nbctest','r')
	#filePtr = open('test.txt','r')
	Accuracy = 0
	#Acc2 = 0
	TotExamples = 0

	for line in filePtr:

		isSpam = False

		#Remove Ending characters
		line = line.strip()

		#Split line by spaces
		line = line.split()

		if(line[1].strip() == 'spam'):
			isSpam = True

		spamProb = log10(probSpam)
		hamProb = log10(probHam)

		#Iterate in spaces of two to get word and word-count
		for i in range(2, len(line), 2):

			word = line[i].strip()
			wordCount = int(line[i+1].strip())

			if(word in Vocabulary):
					
				spamProb += log10(Vocabulary[word].spamProb)*wordCount
				hamProb += log10(Vocabulary[word].hamProb)*wordCount

		#Check for Accuracy
		if((spamProb > hamProb and isSpam == True) or (hamProb > spamProb and isSpam == False)):
			Accuracy += 1

		
		TotExamples = TotExamples + 1

	Percentage = (Accuracy/10)

	print('Accuracy found : '+str(Percentage))

#----------------------------------------------------------------------------------------------------

if __name__ == '__main__':

	preProcess()
