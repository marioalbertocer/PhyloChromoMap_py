# This script creates the intervals each X nucleotides (X is defined 
# for the user in the parameters file) for the chromosome maps. 
# Then it places the OGs and loci in their interval. Beware that the output
# can have more than one OG/seq per interval. So, it's necesary to inspect 
# those few cases by with the script 'mapInfoHelper'.

# Input: 
# - criteriaANDcounts_out.txt from 'treesCriteria_counts' -- (path2files)
# - m_interval (number of nucleotides that separates each interval)
# - chromosomes size file

module Intervals2

	def Intervals2.mapIntervals(path2files, m_interval, chromoSizeFile)
	
		out = File.open(path2files + '/mapInfo.csv', 'w')
		toMap = File.open(path2files + "/criteriaANDcounts_out.csv", 'r').readlines()
		chromosize = File.open(chromoSizeFile, "r").readline()
		
		number_chr = 0
		chromosize.each do |chr_line|
			intervals = Array.new
			chr = chr_line.split(",")[0]

			if chr != ''
				number_chr = number_chr + 1
				chrLen = (chr_line.split(",")[1]).gsub(/\n/, "")

				m = m_interval  # length of the intervals
				position = 1
				intervals << position
			
				while (position <= chrLen)
					position = position + m
					intervals << position
				end		
			
				# At this point the intervals are already done and saved in a array. Now we are going 
				# grab the loci and clades counts from criteriaANDcounts_out
				toMap_loci = Array.new()
				toMap.each do |line|
					line = line.sub(/\n$/, "")
					if line.include? chr		# As we are working per chromosome (see first loop above). Then we need to filter the lines 
						if line !~ /no_tree/
							values = line.split(",")
							seq = values[3]
							og = values[4]
							criterion = values[5]
							counts = values[6..13]
							counts = counts * ","
						
							if criterion =~ /yes/	# only consider OGs that meet our criterion
								locus_s = values[1] # locus start
								locus_e = values[2] # locus end
								toMap_loci << "locus:" + locus_s.to_s + "-" + locus_e.to_s + "," + "seqID:" + seq + "," + "OG:" + og + "," + "counts:" + counts					
							end
						end
					end
				end
			
				intervals.each do |interval|
					neighbors = Array.new()
					toMap_loci.each do |toMap_locus|
						locus = toMap_locus.split(",")[0]
						locus = locus.sub(/locus:/, "")
						locus = locus.split("-")[0]
						if locus.to_i >= interval
							if locus.to_i < (interval + 1000)
								neighbors << toMap_locus
							end
						end
					end
				
					if neighbors == []
						puts chr + "\t" + interval.to_s
						out.write(chr + "," + interval.to_s + "\n")			
					else
						neighbors = neighbors * ","
						puts chr + "\t" + interval.to_s + "\t" + neighbors
						out.write(chr + "," + interval.to_s + "," + neighbors + "\n")
					end
				end
			end
		end
		
		return "# of chromosomes: " + number_chr.to_s + "\nMap lines: " + (intervals.length).to_s + "\nGenes mapped: " + (toMap_loci.length).to_s
				
	end
end