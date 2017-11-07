# This script creates the intervals of 1000 kb for the chromosome maps. 
# Then it places the OGs and loci in their interval. Beware that the output
# can have more than one OG/seq per interval. So, it's necesary to inspect 
# those few cases by hand. The script 'mapInfoHelper' would be very useful
# for performimg that task. 

# Input: 
# - criteriaANDcounts_out.txt from 'treesCriteria_counts'
# - folder with genomic sequences
# - folder with CDSs

import os

folder = 'Saccharomyces_cerevisiae/'
path = '/Users/marioceron/Documents/katzlab/duplications/orthomcl-release5/'
out = open(path + folder + 'mapInfo.txt', 'w')
toMap = open(path + folder + 'criteriaANDcounts_out.txt', 'r')
toMap = toMap.readlines()

# for each chromosome... 
for chrFile in os.listdir(path + folder + 'genome/'):
 
 	# Here we create the intervals from the genome sequences
 	# it takes the sequences, calculate lenght and do intervals each
 	# 1000 kb up to the length of the chromosome.
 	
 	if ".fasta" in chrFile:
 		intervals = []
 		chr = chrFile.split(".")[0]
 		chrSeq = open(path + folder + 'genome/' + chr + ".fasta", 'r')
 		chrSeq = chrSeq.readlines()
 		chrSeq = [x for x in chrSeq if '>' not in x] # avoiding tags '>' in fasta
 		chrSeq = "".join(chrSeq)
 		chrSeq = chrSeq.replace("\n", "")
 		chr = chr.split(".")[0]
 		chrLen = len(chrSeq)
		
 		m = 1000 # length of the intervals
 		position = 1
 		intervals.append(position) 
 		
 		while (position <= chrLen):
 			position = position + m
 			intervals.append(position)	
 		
 		# At this point the intervals are already done and saved in a array. Now we are going 
 		# to read the coding sequences. In future lines we will use them for grabbing the loci from the tags. 
 		cdsFile = open(path + folder + 'seqs/' + chr + '.txt', 'r')
 		cdsFile = cdsFile.readlines()
 		
 		# Now we need the data that we are going to map in the intervals. So, we take the info from 'criteriaANDcounts_out'
 		toMap_loci = []
 		for line in (toMap):
 			line = line.strip("\n")
 			if chr in line:						# As we are working per chromosome (see first loop above). Then we need to filter the lines 
 												# containg that chromosome
 				if 'no_group' not in line:		# We just need OGs, no 'no_groups'
 					values = line.split("\t")
 					seq = values[1]
 					og = values[2]
 					criterion = values[5]
 					counts = values[6:14]
 					counts = "\t".join(counts)
 				
 					if 'yes' in criterion:	# only consider OGs that meet our criterion
 						for line2 in cdsFile:
 							if seq in line2:
 							
 								# Here we take the locus of every sequence for placing it on the intervals					
 								loci = line2.split(" ")[-1]
 								loci = loci.split("=")[1]
								loci = loci.replace('join', '')
								loci = loci.replace('complement', '')
 								loci = loci.replace(")", '')
 								loci = loci.replace("(", '')
 								loci = loci.replace("[", '')
 								loci = loci.replace("]", '')
 								loci = loci.replace("..", ",")
 								loci = loci.split(",")
 
 								# Now we have all loci of the seqs
 								loci_sorted = []
 								for locus in loci:
 									locus_sorted = int(locus)
 									loci_sorted.append(locus_sorted)
 								loci_sorted.sort()
  	 							 	 							
 								toMap_loci.append("locus:" + str(loci_sorted[0]) + "-" + str(loci_sorted[-1]) + "\t" + "seqID:" + seq + "\t" + "OG:" + og + "\t" + "counts:" + counts)

 		for interval in intervals:
 			neighbors = []
 			for toMap_locus in toMap_loci:
 				locus = toMap_locus.split("\t")[0]
 				locus = locus.replace("locus:", "")
 				locus = locus.split("-")[0]
 				if int(locus) >= interval:
 					if int(locus) < (interval + 1000):
 						neighbors.append(toMap_locus)
 		
 			if neighbors == []:
 				print chr + "\t" + str(interval)
 				out.write(chr + "\t" + str(interval) + "\n")
 			else:
 				neighbors = "\t".join(neighbors)
 				print chr + "\t" + str(interval) + "\t" + neighbors
 				out.write(chr + "\t" + str(interval) + "\t" + neighbors + "\n")