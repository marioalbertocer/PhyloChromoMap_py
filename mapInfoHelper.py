# This script helps to correct the file 'mapInfo' produced by the script 'intervals'
# The problems in mapInfo is that some intervals have more than one sequence/og associated.
# This scripts takes the intervals that contain exactly two sequences/ogs, splits the 
# sequences/ogs and put the second sequence/og in the next interval. Beware that this is 
# just a method that I propose to solve the problem. If the first codons of two sequences 
# are in the same interval, it is very likelly that they also occupy the next interval. 
# This iscript resolve most of the problematic cases. However, some cases would need manual
# inspection.

# In which cases this script is not useful (rare cases): 
# - When the next interval already contains a sequence/og.
# - When instead of 2 sequences per interval you have more than 2

folder = 'Saccharomyces_cerevisiae/'
path = '/Users/marioceron/Documents/katzlab/duplications/orthomcl-release5/'
out = open(path + folder + 'mapInfo_corrected.txt', 'w')
mapinfo = open(path + folder + 'mapInfo.txt', 'r')
mapinfo = mapinfo.readlines()

map = []

i = 0
to_add = ""

# Reading mapInfo ...
for line in mapinfo:
	line = line.strip("\n")
	i = i + 1
	values = line.split("\t")

	# ---------------------------
	# It is going to print each line in the output exactly as in mapInfo except when there 
	# are 2 sequences mapped in the same interval. When it is in a interval with 2
	# sequences, it prints only the first sequence for the current interval and saves 
	# the second sequence in the global variable "to_add". For the next iteration, if the 
	# interval is empty, it adds the sequence saved in to_add. Before ending the iteration 
	# to_add sould be set to "" again, so that it can be used in a further iterations with
	# interval containing two sequences. 
	# ----------------------------
	
	if len(values) == 24:					# if two sequences in the current interval ...		
		first = "\t".join(values[0:13])		# takes the first seq
		second = "\t".join(values[13:24])	# takes the second seq
		to_add = ""
		nextline = mapinfo[i].split("\t")	# explore ahead the line of mapinfo that would
											# be used in the next iteration.
		if len(nextline) == 2:				# if the next line is epnty ...
			to_add = second					# put the second sequence in global variable "to_add
			line = first					# modify the line of mapInfo and print the interval with 
			print line						# only the first sequence.
			out.write(line + "\n")	
		else:								# But is the next iteration is in a interval that already 
			print line						# has a sequence, then don't split anything and print
			out.write(line + "\n")			# exactly as in mapinfo.
		
			
	# if the next iteration is in a enpty interval, it would add the sequence saved in 
	# the previous iteration by adding the global variable "to_add" to the line of mapinfo


	if len(values) == 2:
		if to_add != "":
			line = line + "\t" + to_add
			to_add = ""	
			print line
			out.write(line + "\n")
		else:
			print line 
			out.write(line + "\n")
			
	# if the next iteration interval containing either one sequence or more than 2, it
	# would print the line of mapinfo without any modification. 
	
	if len(values) == 13 or len(values) > 24:
		to_add = ""	
		print line
		out.write(line + "\n")