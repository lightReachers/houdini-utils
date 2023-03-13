import hou
import os
userdir = os.getenv('HOME')
setshotpath = userdir+"/houdini17.5/setshot.txt"

if os.path.isfile(setshotpath):
	with open(setshotpath) as f:
		lines = [line.rstrip('\n') for line in open(setshotpath)]

if lines[0] == '0':
	hou.hscript("setenv ENV_ID=" + lines[0])		
	hou.hscript("setenv HSHOW=" + lines[1])		
	hou.hscript("setenv HSEQ=" + lines[2])	
	hou.hscript("setenv HSHOT=" + lines[3])	
	hou.hscript("setenv HUSER=" + lines[4])	
	hou.hscript("setenv HELEM=" + lines[5])	
	hou.hscript("setenv JOB=" + lines[6])
	
if lines[0] == '1':
	hou.hscript("setenv ENV_ID=" + lines[0])		
	hou.hscript("setenv HSHOW=" + lines[1])		
	hou.hscript("setenv HUSER=" + lines[2])	
	hou.hscript("setenv HELEM=" + lines[3])	
	hou.hscript("setenv JOB=" + lines[4])

if lines[0] == '2':
	hou.hscript("setenv ENV_ID=" + lines[0])		
	hou.hscript("setenv HSHOW=" + lines[1])		
	hou.hscript("setenv HSEQ=" + lines[2])	
	hou.hscript("setenv HSHOT=" + lines[3])	
	hou.hscript("setenv HUSER=" + lines[4])	
	hou.hscript("setenv HELEM=" + lines[5])	
	hou.hscript("setenv JOB=" + lines[6])	

print "...getting previous shot information"
print lines

	
