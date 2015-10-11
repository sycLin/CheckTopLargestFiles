import os
import sys
import re
import subprocess

####################
# helper functions #
####################
def run_os_cmd(cmd):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = p.communicate()
	return (out, err)

def print_usage():
	print "ERROR: incorrect usage"
	print "Usage: $python <file_name>"
	print "Usage: $python <file_name> <count>"


#
# global settings
#
f1_name = "test.txt"
f2_name = "processed.txt"
HOME_DIR = os.getenv("HOME")
LIST_TOP_COUNT = 10 # default 10


#########################
# start of main program #
#########################

#
# check arguments
#
if len(sys.argv) == 1: # $python <script file name>
	pass
elif len(sys.argv) == 2: # python <script file name> <count>
	try:
		tmp = int(sys.argv[1])
	except:
		print_usage()
		sys.exit(1)
	LIST_TOP_COUNT = tmp
else:
	print_usage()
	sys.exit(1)

#
# remove if existed
#
if os.path.exists(f1_name):
	os.remove(f1_name)

#
# create the text file by "ls" commans
#
cmd = "ls -laSR " + HOME_DIR + " > " + f1_name
out, err = run_os_cmd(cmd)

if len(err) > 0:
    print "ERROR: " + err

#
# remove processed file if existed
#
if os.path.exists(f2_name):
	os.remove(f2_name)

#
# open files
#
f1 = open(f1_name, "r")
f2 = open(f2_name, "w+")

#
# process the raw "ls" data 
#
while True:
	lineBuf = f1.readline()
	if lineBuf == "":
		break
	while lineBuf.endswith("\n"):
		lineBuf = lineBuf[:len(lineBuf)-1]
	tokens = lineBuf.split(" ")
	if len(tokens) >= 9:
		f2.write(lineBuf+"\n")

f1.close()

f2.seek(0)


#
# find the top largest files
#
top_10_path_and_size = []

while True:
	lineBuf = f2.readline()
	if lineBuf == "":
		break
	tokens = re.split("\s+", lineBuf)
	try:
		size = int(tokens[4])
	except:
		continue
	if len(tokens) > 9:
		path = ""
		for i in range(8, len(tokens)):
			path += tokens[i]
	else:
		path = tokens[8]
	if len(top_10_path_and_size) < LIST_TOP_COUNT:
		tmp_list = [path, size]
		top_10_path_and_size.append(tmp_list)
		top_10_path_and_size.sort(key=lambda elem: elem[1], reverse=True)
	elif size > top_10_path_and_size[LIST_TOP_COUNT-1][1]:
		top_10_path_and_size.pop()
		tmp_list = [path, size]
		top_10_path_and_size.append(tmp_list)
		top_10_path_and_size.sort(key=lambda elem: elem[1], reverse=True)

f2.close()
print "length of top_10 = " + str(len(top_10_path_and_size))
print "%10s %s" % ("size", "filename")
for p_and_s in top_10_path_and_size:
	print "%10s %s" % (str(p_and_s[1]), p_and_s[0])

os.remove(f1_name)
os.remove(f2_name)

