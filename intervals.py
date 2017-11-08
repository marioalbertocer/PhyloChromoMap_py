# This script creates the intervals each X nucleotides (X is defined 
# for the user in the parameters file) for the chromosome maps. 
# Then it places the OGs and loci in their interval. Beware that the output
# can have more than one OG/seq per interval. So, it's necesary to inspect 
# those few cases by with the script 'mapInfoHelper'.

# Input: 
# - criteriaANDcounts_out.txt from 'treesCriteria_counts' -- (path2files)
# - m_interval (number of nucleotides that separates each interval)
# - chromosomes size file

import os

def mapIntervals(path2files, m_interval, chromoSizeFile):

	out = open(path2files + '/mapInfo.csv', 'w')
	toMap = open(path2files + "/criteriaANDcounts_out.csv", 'r').readlines()
	chromosize = open(path2files + "/" + chromoSizeFile, "r").readlines()
	
	result = {"number of chromosomes" : 0, "map size" : 0, "genes mapped" : 0}


	for chr_line in chromosize:
		intervals = []
		chr = chr_line.split(",")[0]

		if chr != '':
			result["number of chromosomes"] = result["number of chromosomes"] + 1
			chrLen = int((chr_line.split(",")[1]).replace("\n", ""))

			m = int(m_interval)  # length of the intervals
			position = 1
						
			while (position <= chrLen):

				print chr + "\t" + str(position)
				out.write(chr + "," + str(position))
				result["map size"] = result["map size"] + 1

				for line in toMap:
					line = line.replace("\n", "")
					values = line.split(",")
					og = values[4]
				
					if values[0] == chr:		# As we are working per chromosome (see first loop above). Then we need to filter the lines 
						if og != 'no_tree':
							locus_s = values[1] # locus start
							locus_e = values[2] # locus end
						
							if int(locus_s) >= position:
								if int(locus_s) < (position + int(m_interval)):
								
									seq = values[3]
									criterion = values[5]
									counts = values[6:13]
									counts = ",".join(counts)
				
									if 'yes' in criterion:	# only consider OGs that meet our criterion
										print "locus:" + str(locus_s) + "-" + str(locus_e) + "," + "seqID:" + seq + "," + "OG:" + og + "," + "counts:" + counts
										out.write("," + "locus:" + str(locus_s) + "-" + str(locus_e) + "," + "seqID:" + seq + "," + "OG:" + og + "," + "counts:" + counts)
										result["genes mapped"] = result["genes mapped"] + 1
				
				out.write("\n")
				position = position + m

	return result


# 
# 
# # This script creates the intervals each X nucleotides (X is defined 
# # for the user in the parameters file) for the chromosome maps. 
# # Then it places the OGs and loci in their interval. Beware that the output
# # can have more than one OG/seq per interval. So, it's necesary to inspect 
# # those few cases by with the script 'mapInfoHelper'.
# 
# # Input: 
# # - criteriaANDcounts_out.txt from 'treesCriteria_counts' -- (path2files)
# # - m_interval (number of nucleotides that separates each interval)
# # - chromosomes size file
# import os
# 
# def mapIntervals(path2files, m_interval, chromoSizeFile):
# 
# 	out = open(path2files + '/mapInfo.csv', 'w')
# 	toMap = open(path2files + "/criteriaANDcounts_out.csv", 'r').readlines()
# 	chromosize = open(path2files + "/" + chromoSizeFile, "r").readlines()
# 
# 	number_chr = 0
# 	genes_mapped = 0
# 	intervals = []
# 	
# 	for chr_line in chromosize:
# 		chr = chr_line.split(",")[0]
# 
# 		if chr != '':
# 			number_chr = number_chr + 1
# 			chrLen = (chr_line.split(",")[1]).replace("\n", "")
# 
# 			m = m_interval  # length of the intervals
# 			position = 1
# 			intervals.append(position)
# 	
# 			while (position <= int(chrLen)):
# 				position = position + int(m)
# 				intervals.append(position)
# 	
# 			# At this point the intervals are already done and saved in a array. Now we are going 
# 			# grab the loci and clades counts from criteriaANDcounts_out
# 			toMap_loci = []
# 			for line in toMap:
# 				line = line.replace("\n", "")
# 				if chr in line:	# As we are working per chromosome (see first loop above). Then we need to filter the lines 
# 					if not "no_tree" in line:
# 						values = line.split(",")
# 						seq = values[3]
# 						og = values[4]
# 						criterion = values[5]
# 						counts = values[6:13]
# 						counts = ",".join(counts)
# 				
# 						if "yes" in criterion: # only consider OGs that meet our criterion
# 							locus_s = values[1] # locus start
# 							locus_e = values[2] # locus end
# 							toMap_loci.append("locus:" + str(locus_s) + "-" + str(locus_e) + "," + "seqID:" + seq + "," + "OG:" + og + "," + "counts:" + counts)
# 	
# 			for interval in intervals:
# 				neighbors = []
# 				for toMap_locus in toMap_loci:
# 					locus = toMap_locus.split(",")[0]
# 					locus = locus.replace("locus:", "")
# 					locus = locus.split("-")[0]
# 					if int(locus) >= interval:
# 						if int(locus) < (interval + 1000):
# 							genes_mapped = genes_mapped + 1
# 							neighbors.append(toMap_locus)
# 		
# 				if neighbors == []:
# 					print chr + "\t" + str(interval)
# 					out.write(chr + "," + str(interval) + "\n")			
# 				else:
# 					neighbors = ",".join(neighbors)
# 					print chr + "\t" + str(interval) + "\t" + neighbors
# 					out.write(chr + "," + str(interval) + "," + neighbors + "\n")
# 
# 	return "# of chromosomes: " + str(number_chr) + "\nMap lines: " + str(len(intervals)) + "\nGenes mapped: " + str(genes_mapped)