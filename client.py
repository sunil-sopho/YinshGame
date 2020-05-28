from subprocess import Popen, PIPE
# from nbstreamreader import NonBlockingStreamReader as NBSR
from sys import platform
import os


class client(object):

	def __init__(self,executionCommand,executionFile,playerId,boardSize,time,seq):
		self.child = None
		self.timeout = 100
		self.createChildProcess(executionCommand,executionFile)
		flag = self.sendData(str(playerId)+" "+str(boardSize)+" "+str(time)+" "+str(seq))
		print("send data player : ",playerId,flag)

	def createChildProcess(self,executionCommand,executionFile):
		if platform == "darwin" or platform == "linux" or platform == "linux2":
			self.child = Popen ([executionCommand, executionFile], stdin = PIPE, stdout = PIPE, bufsize=0,preexec_fn=os.setsid)	
		else:
			self.child = Popen ([executionCommand, executionFile], stdin = PIPE, stdout = PIPE, bufsize=0)
		self.ModifiedOutStream = self.child.stdout#NBSR(self.ChildProcess.stdout)		
		
	def sendData(self,data):
		success_flag = False
		try:
			if data[-1] != '\n':
				data += '\n'

			data = str.encode(data)
			self.child.stdin.write(data)
			success_flag = True
		except Exception as e:
			print(e)
			
		return success_flag
	def recieveData(self):
		data = None
		try:
			data = self.ModifiedOutStream.readline(self.timeout)
		except Exception as e:
			print(e)			
		return data

	def closeChild(self):
		if platform == "darwin" or platform == "linux" or platform == "linux2":
			try:
			 	os.killpg(os.getpgid(self.child.pid), 15)
			except Exception as e:
				print(e)
		else:	
			self.child.kill()
		self.child = None