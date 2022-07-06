"""
This script will help to redistribute the genes that fall in the same interval on the map

* case 1: A GENE FALL BETWEEN TWO INTERVALS
intervals.rb organizes the genes with range 2300-2700 and 2800-3300 in the same range 
because their first codon is in the range 2000-3000. Then, mpInfoHelper.rb puts the second 
gene in the interval 3000-4000. 

* case2: TWO GENES FALL IN SAME INTERVAL
intervals.rb organizes the genes with range 2300-2700 and 2700-2900 in the same range 
because their first codon is in the range 2000-3000. In this case mpInfoHelper.rb cannot put
the second gene in the interval 3000-4000 because the last codon does not fall in the same
in this range. As a result the second gene is not mapped but the record of location and 
clade counting will be saved in the document notMappedGenes.txt

* case3: MORE THAN TWO GENES FALL IN SAME INTERVAL, OVERLAPPING GENES
intervals.rb organizes the genes with range 2300-2700, 2800-3300 and 2900-4010 in the same range 
because their first codon is in the range 2000-3000. Then, mpInfoHelper.rb puts the second 
gene in the interval 3000-4000 and the third gene in the interval 3000-4000. This is because
it follows the logic of case 1. 

* case4: TWO GENES FALL IN SAME INTERVAL AND NEXT INTERVAL IS ALREADY OCCUPIED 
intervals.rb organizes the genes with range 2300-2700 and 2800-3300 in the same range 
because their first codon is in the range 2000-3000. Then, mpInfoHelper.rb needs to put the 
second gene in the interval 3000-4000. But, if intervals.rb already put another gene in the
interval 3000-4000, then the second gene would not be mapped. Still, the record of location and 
clade counting will be saved in the document notMappedGenes.txt
"""

import os

def redistributeLoci(path2files):

	out = open(path2files + "/" + 'mapInfo_corrected.csv', 'w')
	out2 = open(path2files + "/" + 'notMappedGenes.csv', 'w')
	mapinfo = open(path2files + "/" + 'mapInfo.csv', 'r').readlines()

	map = mapinfo

	exe = 'y'
	run = 0

	while exe == 'y':
	
		# This is an iterative process. The explanation of the use of while loop here will be at 
		# the end ...
	
		run = run + 1
		to_add = ""
		count_changes = 0
		map_corrected = []
	
		print("\nRUN # " + str(run) + ":\n")
	
	#	Reading mapInfo ...
	#	mapinfo.each do |line|
		for line in map:
			line = line.replace("\n", "")
			values = line.split(",")
	
			# ---------------------------
			# It is going to print each line in the output exactly as in mapInfo except when there 
			# is more than one sequence mapped in the same interval. When there is in a interval with
			# more than one sequences, it prints only the first sequence for the current interval and saves 
			# the remaining sequences in the global variable "to_add". Then it checks if the knext interval 
			# if empty and redistribute the genes saved in to_add following the logic described in the 
			# cases above
			# ---------------------------

			if len(values) >= 24:	# if two or more sequences in the current interval ...		
				first = ",".join(values[0:13]) # takes the first seq
				rest = ",".join(values[13:]) # takes the remaining seqs
				if to_add != "" : 
					out2.write(to_add + "\n")
				to_add = "" 
				to_add = rest		# put the remaining sequences in global variable "to_add"
				line = first		# modify the line of mapInfo and print the interval with 
										# only the first sequence.
				print(line)
				map_corrected.append(line)
	
			# if the next iteration is in a enpty interval, it would add the sequence saved in 
			# the previous iteration by adding the global variable "to_add" to the line of mapinfo
	
			if len(values) == 2:
		
				# ----------------------------
				# If the next interval is empty it checks if there are genes saved in to_add. If so, and 
				# part of the first gene (in to_add) falls in this interval, it adds to_add to the interval(*).
				# In contrast, if the gene falls totally in the last interval, it removes the gene from to_add, 
				# takes the next gene from to_add and repeats the procedure. The records of clade counting and
				# locus for every gene that does not fall in the interval (and therefore removed from to_add) is
				# saved in notMappedGenes.txt
				# ----------------------------
			
				while to_add != "":
					remainingGenes = to_add.split(",")

					if int(values[1]) < int(remainingGenes[0].split("-")[1]): # if first gene is still inside the range
						count_changes += 1
						line = line + "," + to_add
						to_add = ""	# After this iteration to_add should be set to ""
					else:
						count_changes += 1
						not_mapped = ",".join(remainingGenes[:11])
						out2.write(not_mapped + "\n")
					
#						if remainingGenes[10]:
					if len(remainingGenes) > 11:
						remainingGenes = remainingGenes[11:]
						to_add = ",".join(remainingGenes)
					else:
						to_add = "" # After this iteration to_add should be set to ""
			
				print(line)

				map_corrected.append(line)
	
			# if the next iteration interval containing either one sequence or more than 2, it
			# would print the line of mapinfo without any modification. 
	
			if len(values) == 13:
				if to_add != "" : 
					out2.write(to_add + "\n")
				to_add = ""
				print(line)
				map_corrected.append(line)
	
		map = map_corrected
	
		print("number of changes: " + str(count_changes))
		if count_changes == 0:
			exe = 'n' 
	
		# This is an iterative process. It will redistribute the second gene in each interval that 
		# has more than one gene. Then the whole process is repeted for redistributing the third genes
		# and so on. The variable count_changes tacks the number of changes per iteration, if there
		# are not more changes in an iteration then the loop stops. 

	# ----------------------------
	# Writing mapInfo_corrected   |
	# ----------------------------

	print("\n\n===== mapInfo_corrected =====\n\n")
	for line in map:
		print(line)
		out.write(line + "\n")
	
	return "Information to be mapped is already corrected"