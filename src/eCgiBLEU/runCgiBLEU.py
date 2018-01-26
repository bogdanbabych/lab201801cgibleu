'''
Created on 26 Jan 2018

@author: bogdan
'''

class runCgiBLEU(object):
	'''
	runs BLEU perl script via CGI from the web interface. Is triggered by input from the index.html file
	Template for other corpus labs projects with web interface to run Linux / Unix programmes
	'''


	def __init__(self, params):
		'''
		Constructor
		'''
		