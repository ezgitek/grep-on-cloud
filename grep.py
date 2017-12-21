import sys
import re
import subprocess
import os
import pwd
from sets import Set
import datetime
from dateutil.parser import parse



list1 = []
tobeexecuted=[]
tobeexecuted.append("")
lines=[]
bools = [0,0,0,0,0] # [ -b ] [-f] [-s ] [-i ] [directory]


def fromfile(filename):
	f = open(filename, 'r')
	lines = f.readlines()
	file = open('statementsfile.txt', 'w+')
	for line in lines:
		file.write(line)


def stdinput():
	lines=sys.stdin.readlines()
	file = open('statementsfile.txt', 'w+')
	for line in lines:
		file.write(line)
	


def read_file():
	f = open('statementsfile.txt', 'r')
	lines = f.readlines()
	for line in lines:
		match = re.search(r'(.+)=>(.+)', line)
		if match:
			evaluate(match.group(1).strip(),match.group(2).strip() )


def traverse_dfs(directory):
 
	temp= [directory] 
	list1.append(directory)
	while temp: 
		fullpathname =  temp.pop()  
		curlist = os.listdir(fullpathname) 
		for fdname in reversed(curlist): 
			newpath = fullpathname + "/" + fdname 
			if os.path.isdir(newpath): 
				temp.append(newpath)
			list1.append(newpath)  
    
def traverse_bfs(directory):
	temp= [directory] 
	list1.append(directory)
	while temp: 
		fullpathname =  temp.pop()  
		curlist = os.listdir(fullpathname) 
		for fdname in curlist: 
			newpath = fullpathname + "/" + fdname 
			if os.path.isdir(newpath): 
				temp.append(newpath)
			list1.append(newpath)  


def evaluate(expl,expr):
	#print list
	match= re.search(r'^start$',expl)
	if match:
		parseright(expr,"")

	match = re.search(r'file', expl)
	if match:
		parseright(expr,parseleft(expl))

	match = re.search(r'directory', expl)
	if match:
		parseright(expr, parseleft(expl))

	match = re.search(r'^finish$', expl)
	if match:
		parseright(expr,"")



def parseleft(exporg):
	matched=[]
	
	for elem in list1:
		exp = exporg
		exp=exp.strip()
		exp =" " + exp + " "
		result = []
		exp=exp.replace("&&","&")
		exp=exp.replace("||","|")


		match = re.search(r'file', exp)
		if match:
			if os.path.isfile(elem):
				exp=exp.replace("file","True")
			else:
				exp=exp.replace("file","False")

		match = re.search(r'directories', exp)
		if match:
			if os.path.isdir(elem):
				exp=exp.replace("directories","True")
			else:
				exp=exp.replace("directories","False")
	

		match = re.search(r"\W/(.+)/\W", exp)  # item matches 
		if match:
			if bools[1]==1:
				match2 = re.search(match.group(1), elem)
				if match2:
					exp=exp.replace(match.group(),"True")
				else:
					exp=exp.replace(match.group(),"False")
			else:
				filename=re.search(r"[^/]+$",elem)
				#print "bisey"
				if filename:
					#print filename.group(0)
					match2 = re.search(match.group(1), filename.group(0))
					if match2:
						#print filename.group(0)
						exp=exp.replace(match.group(),"True")
					else:
						#print "else"
						exp=exp.replace(match.group(),"False")
						#print exp
				else: 
					exp=exp.replace(match.group(),"False")


		match = re.search(r"c/(.+)/", exp)  # contents of the item (file) matches
		if match:
			f = open(elem, 'r')
			content = f.read()
			match2 = re.search(match.group(1), content)
			if match2:
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")


		match = re.search(r"o/(.+)/", exp)  # owner of the item matches
		if match:
			owner = pwd.getpwuid(os.stat(elem).st_uid).pw_name
			match2 = re.search(match.group(1), owner)
			if match2:
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")

		match = re.search(r"p/(.+)/", exp)  # permission of the item matches (octal representation)
		if match:
			permission = oct(stat.S_IMODE(os.lstat(elem).st_mode))
			match2 = re.search(match.group(1), permission)
			if match2:
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")	

		match = re.search(r"d/(.+)/", exp)
		if match:
			statinfo = datetime.datetime.fromtimestamp(os.stat(elem).st_mtime)
			if (statinfo - parse(match.group(1))).days==0:
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")

		match = re.search(r"d/(.+)/b", exp)
		if match:
			statinfo = datetime.datetime.fromtimestamp(os.stat(elem).st_mtime)
			if (statinfo - parse(match.group(1))).days<0:
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")
		match = re.search(r"d/(.+)/a", exp)
		if match:
			statinfo = datetime.datetime.fromtimestamp(os.stat(elem).st_mtime)
			if (statinfo - parse(match.group(1))).days>0:
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")
		match = re.search(r"s/(.+)/", exp)
		if match: 
			size = os.stat(elem).st_size
			if (int(match.group(1))==size):
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")

		match = re.search(r"s/(.+)/l", exp)
		if match: 
			size = os.stat(elem).st_size
			if (int(match.group(1))<size):
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")

			
		match = re.search(r"s/(.+)/m", exp)
		if match: 
			size = os.stat(elem).st_size
			if (int(match.group(1))>size):
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")


		match = re.search(r"readable",exp)
		if match:
			if os.access(elem, os.R_OK):
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")

		match = re.search(r"writeable",exp)
		if match:
			if os.access(elem, os.W_OK):
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")


		match = re.search(r"executable",exp)
		if match:
			if os.access(elem, os.X_OK):
				exp=exp.replace(match.group(),"True")
			else:
				exp=exp.replace(match.group(),"False")

		if eval(exp):
			#print "matched"
			matched.append(elem)

	#print matched
	return matched

def parseright(exp, list):
	###print list
	commands = exp.split(';') #split statements
	for command in commands:
		if command != '':
			command = command.strip()
			match = re.search(r'{(.+)}', command)
			if match:
				if '$MATCHED' in command:
					for elem in list:						
						incurly=match.group(1).strip()
						incurly = incurly.replace('$MATCHED', "'" + elem + "'") #change argument
						tobeexecuted[0]+=incurly #execute python script
						tobeexecuted[0]+="\n"
									
				else:
					for elem in list:
						tobeexecuted[0]+=match.group(1).strip()
						tobeexecuted[0]+="\n"

			else:
				if '$MATCHED' in command:
					for elem in list:
						command = str(command).replace('$MATCHED', str(elem))
						command2 =command.split(" ")
						###print command
						os.system(command) #execute bash command
						command = str(command).replace(str(elem),'$MATCHED')

				else:
					for elem in list:
						command2 =command.split(" ")
						os.system(command) #execute bash command


def execute():
	if tobeexecuted[0]!="":
		tobeexecuted[0]=tobeexecuted[0].decode('string_escape')
		###print tobeexecuted[0]
		exec(tobeexecuted[0])

def main():
	directory=""
	argnum =len(sys.argv)
	if argnum > 1:
		args = sys.argv[1:]
		cmd = "python /home/ec2-user/fdsm.py"
		while  len(args) >0:
		
			if args[0]=='-b':
				bools[0]=1
				cmd += " "+ args[0]
				del args[0]
			
			elif args[0]=='-f':
				bools[1]=1
				cmd += " "+ args[0]
				del args[0]
			
			elif args[0] == '-s':
				bools[2]=1
				cmd += " "+ args[0]
				del args[0]
				filename = args[0]
				cmd += " statementsfile.txt"
				del args[0]
			
			elif args[0] == '-i':
				bools[3]=1
				del args[0]
				instanceid = args[0]
				del args[0]
				
			elif args[0]!=None:
				bools[4]=1
				directory = args[0]
				cmd += " " + args[0]
				del args[0]

	if bools[4]==0:
		cmd += " " + "/home/ec2-user"
		directory = os.getcwd()
		
		


	if bools[2]==1:
		fromfile(filename)
	else:
		stdinput()
	if bools[3]==1:   
		import boto3
		ec2 = boto3.resource('ec2')
		instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
 
		ip = ''
		for instance in instances:
			if instanceid == instance.id:
				ip = instance.public_ip_address
		##print ip

		subprocess.call('scp -i amazon.pem fdsm.py ec2-user@' + ip + ':/home/ec2-user',shell=True)
		subprocess.call('scp -i amazon.pem statementsfile.txt ec2-user@' + ip + ':/home/ec2-user',shell=True)
		subprocess.call('scp -i amazon.pem b.txt ec2-user@' + ip + ':/home/ec2-user',shell=True)
		keyfile = '-i ./amazon.pem '
		sshstring = r'ssh -i amazon.pem '
		machine = 'ec2-user@' + ip + ' ' 
		command = sshstring + machine + cmd
		subprocess.call(command,shell=True)
		remove = sshstring + machine 
		subprocess.call(remove + " rm /home/ec2-user/fdsm.py",shell=True)
		subprocess.call(remove + " rm /home/ec2-user/statementsfile.txt",shell=True)
		sys.exit()


	else:
		if bools[0]==1: 
			traverse_bfs(directory)
		else: 
			traverse_dfs(directory)

		read_file() 
		
		execute()

	


if __name__ == '__main__':
	main()
