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

				print(chr + "\t" + str(position))
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
									counts = values[6:]
									counts = ",".join(counts)
				
									if 'yes' in criterion:	# only consider OGs that meet our criterion
										print("locus:" + str(locus_s) + "-" + str(locus_e) + "," + "seqID:" + seq + "," + "OG:" + og + "," + "counts:" + counts)
										out.write("," + "locus:" + str(locus_s) + "-" + str(locus_e) + "," + "seqID:" + seq + "," + "OG:" + og + "," + "counts:" + counts)
										result["genes mapped"] = result["genes mapped"] + 1
				
				out.write("\n")
				position = position + m

	return result

