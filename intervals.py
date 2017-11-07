# This script creates the intervals each X nucleotides (X is defined 
# for the user in the parameters file) for the chromosome maps. 
# Then it places the OGs and loci in their interval. Beware that the output
# can have more than one OG/seq per interval. So, it's necesary to inspect 
# those few cases by with the script 'mapInfoHelper'.

# Input: 
# - criteriaANDcounts_out.txt from 'treesCriteria_counts' -- (path2files)
# - m_interval (number of nucleotides that separates each interval)
# - chromosomes size file

def mapIntervals(path2files, m_interval, chromoSizeFile):

	out = open(path2files + '/mapInfo.csv', 'w')
	toMap = open(path2files + "/criteriaANDcounts_out.csv", 'r').readlines()
	chromosize = open(chromoSizeFile, "r").readline()

	number_chr = 0
	for chr_line in chromosize:
		intervals = []
		chr = chr_line.split(",")[0]

		if chr != ''
			number_chr = number_chr + 1
			chrLen = (chr_line.split(",")[1]).replace("\n", "")

			m = m_interval  # length of the intervals
			position = 1
			intervals.append(position)
	
			while (position <= chrLen):
				position = position + m
				intervals.append(position)
	
			# At this point the intervals are already done and saved in a array. Now we are going 
			# grab the loci and clades counts from criteriaANDcounts_out
			toMap_loci = []
			for line in toMap:
				line = line.sub("\n", "")
				if chr in line.include:	# As we are working per chromosome (see first loop above). Then we need to filter the lines 
					if "no_tree" in line:
						values = line.split(",")
						seq = values[3]
						og = values[4]
						criterion = values[5]
						counts = values[6:13]
						counts = ",".join(counts)
				
						if "yes" in criterion: # only consider OGs that meet our criterion
							locus_s = values[1] # locus start
							locus_e = values[2] # locus end
							toMap_loci.append("locus:" + str(locus_s) + "-" + str(locus_e) + "," + "seqID:" + seq + "," + "OG:" + og + "," + "counts:" + counts)
	
			for interval in intervals:
				neighbors = []
				for toMap_locus in toMap_loci:
					locus = toMap_locus.split(",")[0]
					locus = locus.replace("locus:", "")
					locus = locus.split("-")[0]
					if int(locus) >= interval:
						if int(locus) < (interval + 1000):
							neighbors.append(toMap_locus)
		
				if neighbors == []:
					print chr + "\t" + str(interval)
					out.write(chr + "," + str(interval) + "\n")			
				else:
					neighbors = ",".join(neighbors)
					print chr + "\t" + str(interval) + "\t" + neighbors
					out.write(chr + "," + str(interval) + "," + neighbors + "\n")

	return "# of chromosomes: " + str(number_chr) + "\nMap lines: " + str(len(intervals)) + "\nGenes mapped: " + str(len(toMap_loci))