#!/usr/bin/python
import cgi, sys, os, re, socket
import smtplib
import time
import subprocess

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
		running BLEU
		'''
		self.writeHTMLheading()
		self.procForm()
		
	def writeHTMLheading(self):
		print('Content-type: text/html\n\n')
		print('<title>MT evaluation output</title>\n')
		print('<h2>MT evaluation results! bleu...</h2>\n')

	
	def procForm(self):
		self.readFields()
		self.compBLEUpl()
		
		
	def readFields(self):
		"""
		the function reads form fields which will be used in class
		"""
		NameIPSuffix = 'IP-time-'
		# get remote IP address
		try:
			ClientIP = cgi.escape(os.environ["REMOTE_ADDR"])
		except:
			ClientIP = 'ERROR-default'
			print('clientIP unknown<br>\n')
		# get time
		try:
			ts = time.time()
		except:
			ts = '1000.01'
			print('time not found<br>\b')
		# get dictionary of fields	
		try:
			form = cgi.FieldStorage()
		except:
			print('field storage error<br>\n')
			form = { 'f1010tst' : 'edt' , 'f1020ref' : 'edt das ist ein klein haus' }
			
		try:
			SDataKey1010tstVal = form['f1010tst'].value
			SDataKey1020refVal = form['f1020ref'].value
		except:
			SDataKey1010tstVal = 'edt'
			SDataKey1020refVal = 'edt das ist ein klein haus'
			print('KeyValue fields error : DData = cgi.FieldStorage()<br>\n')
		
		# insert tags:
		# tags ref
		STagRefOpen = """<refset trglang="zn" setid="exper2016" srclang="any">
<doc sysid="ref" docid="1" genre="news" origlang="en">
<seg id="1">
"""

		STagRefClose = """
</seg>
</doc>
</refset>
"""
		# tags src
		STagSrcOpen = """<srcset setid="exper2016" srclang="any">
<doc docid="1" genre="news" origlang="en">
<seg id="1">
"""
		STagSrcClose = """
</seg>
</doc>
</srcset>
"""
		# tags tst
		STagTstOpen = """<tstset trglang="zn" setid="exper2016" srclang="any">
<doc sysid="google" docid="1" genre="news" origlang="en">
<seg id="1">
"""
		STagTstClose = """
</seg>
</doc>
</tstset>		
"""
		
		# saving fields as files for processing
		# path will depend on the system (introduce check?)
		# PathToFile = '/data/bogdan/_oc/_exper/p201701mtbleu/src/users/'
		PathToFile = '/data/html/corpuslabs/lab201801cgibleu/users/'
		
		
		NameTst = NameIPSuffix + ClientIP + '-' + str(ts) + '.tst'
		NameRef = NameIPSuffix + ClientIP + '-' + str(ts) + '.ref'
		NameSrc = NameIPSuffix + ClientIP + '-' + str(ts) + '.src'
		SFDebug = NameIPSuffix + ClientIP + '-' + str(ts) + '.debug'
		
		self.PathNameTst = PathToFile + NameTst
		self.PathNameRef = PathToFile + NameRef
		self.PathNameSrc = PathToFile + NameSrc
		self.PathNameDeb = PathToFile + SFDebug
		
		
		try:
			FTst = open(self.PathNameTst, 'w')
			FTst.write(STagTstOpen + SDataKey1010tstVal + STagTstClose)
			FTst.close()

			FSrc = open(self.PathNameSrc, 'w')
			FSrc.write(STagSrcOpen + SDataKey1020refVal + STagSrcClose)
			FSrc.close()

			FRef = open(self.PathNameRef, 'w')
			FRef.write(STagRefOpen + SDataKey1020refVal + STagRefClose)
			FRef.close()
			
			self.FDebug = open(self.PathNameDeb, 'w')
		except:
			print('cannot record files<br>\n')
		return
		
		
		
	
	def compBLEUpl(self):
		
		# PathToEvalScript = '/data/bogdan/_oc/_exper/p201701mtbleu/src/p010bleuPl/'
		PathToEvalScript = '/data/html/corpuslabs/lab201801cgibleu/src/eCgiBLEU'
		
		SToRun = 'perl ' + PathToEvalScript + 'mteval-v13a.pl -r %s -s %s -t %s\n' % (self.PathNameRef, self.PathNameSrc, self.PathNameTst)
		# SScores = os.popen('echo \'' + STransTextST + '\' | /data/bogdan/_oc/_exper/p2015corp/src/moses/bin/moses -f ' + SMosesIniFile).read()
		self.FDebug.write(SToRun + '\n')
		try:
			SScores = os.popen(SToRun).read()
			# proc = subprocess.Popen(['python','fake_utility.py'],stdout=subprocess.PIPE)
			# proc = subprocess.Popen(['perl', SToRun],stdout=subprocess.PIPE)
		except:
			# proc = 'error: pipe cannot be read<br>\n'
			SScores = 'error: pipe cannot be read<br>\n'
		
		print('<pre>' + SScores + '</pre>\n<br>\n')
		# print(proc + '<br>\n')
		
		

		
		
if __name__ == '__main__':
	ORunBLEUpl = runCgiBLEU()
		