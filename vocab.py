'''

Name :- Siddharth Nahar
Entry No :- 2016csb1043
Date :- 17/11/18
Purpose :-

	1. Class for Information regarding single Word.
	2. It stores spam-freq,ham-freq,condition probablites etc.

'''

#Class Definition for single word

class Vocab:

	#Constructor will be called first time word has been seen
	def __init__(self, word, freq, isSpam):

		self.word = word

		if(isSpam == True):
			self.freqSpam = freq
			self.freqHam = 0
		else:
			self.freqSpam = 0
			self.freqHam = freq

		self.spamProb = 0
		self.hamProb = 0

#------------------------------------------------------------------------------

	#Defining Probablites using m-estimate
	def compute(self, m, p, spamN, hamN):

		self.spamProb = (self.freqSpam + m*p)/(spamN + m)
		self.hamProb = (self.freqHam + m*p)/(hamN + m)

		return self.spamProb ,self.hamProb

#-------------------------------------------------------------------------------

	#Updating Frequencies for spamming and Ham
	def update(self, count, isSpam):

		#Check for is this count for Spam or non spam emails
		if(isSpam == True):
			self.freqSpam = self.freqSpam + count
		else:
			self.freqHam = self.freqHam + count

#-------------------------------------------------------------------------------

	#If called to Print
	def __str__(self):

		String = self.word
		String += "\nProbablity of Spam : "+str(self.spamProb)
		String += "\nProbablity of Ham : "+str(self.hamProb)

		String += "\n--------------------------------------"
		return String	
