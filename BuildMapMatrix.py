# Paths and values to be set.
path = '/Users/marioceron/Documents/katzlab/duplications/orthomcl-release5/'
folder = 'test2/'
inFile = File.open(path + folder + 'mapInfo_corrected.csv', 'r')
inFile = inFile.readlines()
criteriaFile = File.open(path + folder + 'criteriaANDcounts_out.csv', 'r')
criteriaFile = criteriaFile.readlines()
seqsDir = Dir.open(path + folder + 'seqs/')
#out1 = File.open(path + folder + 'freqs4map.txt', 'w')
out2 = File.open(path + folder + 'matrix-raw.csv', 'w')
out3 = File.open(path + folder + 'matrix4map.csv', 'w')
minor_clade = "op"  # options = "op","am","pl","ex","sr","ee","ba","za"

if minor_clade == "op"
	majors = ["op","am","ex","ee","pl","sr","za","ba"] 
	totalMinors = [6, 8, 8, 6, 3, 8, 16, 39]	# number of minor clade per major clade												
elsif minor_clade == "am"
	majors = ["am","op","ex","ee","pl","sr","za","ba"] 
	totalMinors = [8, 6, 8, 6, 3, 8, 16, 39]	# number of minor clade per major clade												
elsif minor_clade == "ex"
	majors = ["ex","ee","pl","sr","am","op","za","ba"] 
	totalMinors = [8, 6, 3, 8, 8, 6, 16, 39]	# number of minor clade per major clade												
elsif minor_clade == "ee"
	majors = ["ee","pl","sr","ex","am","op","za","ba"] 
	totalMinors = [6, 3, 8, 8, 8, 6, 16, 39]	# number of minor clade per major clade												
elsif minor_clade == "pl"
	majors = ["pl","ee","sr","ex","am","op","za","ba"]
	totalMinors = [3, 6, 8, 8, 8, 6, 16, 39]	# number of minor clade per major clade
elsif minor_clade == "sr"
	majors = ["sr","pl","ee","ex","am","op","za","ba"]
	totalMinors = [8, 3, 6, 8, 8, 6, 16, 39]	# number of minor clade per major clade
end

# This is the codes for assigning colors to the values:

#	op	am	pl	ex	sr	ee	ba	za
#[0-25]	1	5	9	13	17	21	25	29
#(0.25-0.5]	2	6	10	14	18	22	26	30
#(0.5-0.75]	3	7	11	15	19	23	27	31
#(0.75-1]	4	8	12	16	20	24	28	32

# Notice that [ and ] represent close interval and ( and ) represent open interval

minor_code = Hash.new
minor_code["op"] = [1,2,3,4].join(",")
minor_code["am"] = [5,6,7,8].join(",")
minor_code["pl"] = [9,10,11,12].join(",")
minor_code["ex"] = [13,14,15,16].join(",")
minor_code["sr"] = [17,18,19,20].join(",")
minor_code["ee"] = [21,22,23,24].join(",")
minor_code["ba"] = [25,26,27,28].join(",")
minor_code["za"] = [29,30,31,32].join(",")

young_code = Hash.new
young_code["y"] = 33
young_code["n"] = 34

# Here we are extracting the loci of the young CDSs from the seqs folder. The young loci 
# will be also mapped
young_loci = Array.new
chrs = Array.new

criteriaFile.each do |line|
	if line !~ /\tyes\t/
		chr = line.split(",")[0]		
		chr = chr.split(".")[0]
		seq = line.split(",")[1]		
		chrs << chr
		
		# Onpening CDSs files...
		seqsDir.each do |cdsFile|
			if cdsFile =~ /\.txt/
				if cdsFile.include? chr
					cdsFile = File.open(path + folder + 'seqs/' + cdsFile)
					cdsFile = cdsFile.readlines()
					cdsFile.each do |line2|		
						if line2.include? seq
						
							# Here we take the locus of every young sequence for placing it on the intervals					
							line2 = line2.chomp
							locus = line2.sub(/^.*location=/, "")
							locus = locus.sub(/^.*\(/, "")
							locus = locus.sub(/(,|(\.\.)).*$/, "")
							locus = locus.gsub(/>|</, "")
							young_loci <<  chr + "," + locus.to_s
							puts chr + "\t" + locus.to_s
							
							# microsporidia data
#							line2 = line2.chomp
#							locus = line2.split("location=")[1]
#							locus = locus.sub(/^.*:/, "")
#							locus = locus.sub(/\(.*$/, "")
#							locus = locus.split("-")[0]
#							young_loci <<  chr + "\t" + locus.to_s
#							puts chr + "\t" + locus.to_s

						end
					end
				end
			end
		end
	end
end

intervals = Array.new
freqs = Array.new
inFile.each do |line|
	line = line.chomp
	line = line.sub(/,*$/, "")
	values = line.split(",")
	
	chr = values[0]
	interval = values[1]
	intervals << interval
	
	if values.length > 2

		m0 = ((values[5].sub(/counts:/, "")).to_f / totalMinors[0].to_f).round(2)
		m1 = (values[6].to_f / totalMinors[1].to_f).round(2)
		m2 = (values[7].to_f / totalMinors[2].to_f).round(2)
		m3 = (values[8].to_f / totalMinors[3].to_f).round(2)
		m4 = (values[9].to_f / totalMinors[4].to_f).round(2)
		m5 = (values[10].to_f / totalMinors[5].to_f).round(2)
		m6 = (values[11].to_f / totalMinors[6].to_f).round(2)
		m7 = (values[12].to_f / totalMinors[7].to_f).round(2)
		counts = [m0, m1, m2, m3, m4, m5, m6, m7].join(",")
		young = "n"
	else
		counts = ([0] * 8).join(",")		
		
		young_loci.each do |locus|
			chr_y = locus.split(",")[0]
			locus = locus.split(",")[1]
			
			young = "n"
			if chr == chr_y
				if locus.to_i >= interval.to_i
					if locus.to_i < (interval.to_i + 1000)
						young = "y"
						break
					end
				end
			end
		end		
	end
	puts chr + "\t" + interval.to_s + "\t" + young + "\t" + counts
	freqs << (chr + "," + interval.to_s + "," + young + "," + counts)
#	out1.write(chr + "," + interval.to_s + "," + counts)
end

chrs.uniq!
map = intervals.uniq
map_cod = intervals.uniq

index = 0 
map.each do |interval|
	puts interval
	index = index + 1
	interval_only = interval.split(",")[0]
	to_replace = (["NA"] * 9).join(",")		
	to_replace_cod = (["NA"] * 10).join(",")	

	chrs.each do |chr|
		freqs.each do |seq2map|
			to_replace = (["NA"] * 9).join(",")	
			to_replace_cod = (["NA"] * 10).join(",")
			seq2map = seq2map.split(",")
			chr_int2map = seq2map[0] + "," + seq2map[1]
			if (chr_int2map.include? chr) and (chr_int2map.include? interval_only)
				to_replace = seq2map[2..seq2map.length].join(",")
				counts2cod = seq2map[3..seq2map.length]				
				minor = 0
				coded_counts = Array.new
				coded_young = ""

				counts2cod.each do |minor_count|
					minor = minor + 1 
															
					if (minor_count.to_f >= 0) and (minor_count.to_f <= 0.25)
						minor_count_cod = minor_code[majors[minor - 1]].split(",")[0]
						coded_counts << minor_count_cod
						next
					end 					
					if (minor_count.to_f > 0.25) and (minor_count.to_f <= 0.5)
						minor_count_cod = minor_code[majors[minor - 1]].split(",")[1]
						coded_counts << minor_count_cod
						next
					end 					
					if (minor_count.to_f > 0.5) and (minor_count.to_f <= 0.75)
						minor_count_cod = minor_code[majors[minor - 1]].split(",")[2]
						coded_counts << minor_count_cod
						next
					end 					
					if (minor_count.to_f >= 0.75) and (minor_count.to_f <= 1)
						minor_count_cod = minor_code[majors[minor - 1]].split(",")[3]
						coded_counts << minor_count_cod
						next
					end 									
				end				
				
				if seq2map[2] =~ /y|n/
					coded_young = young_code[seq2map[2]] 
				end
				
				to_replace_cod = young_code["y"].to_s + "," + coded_young.to_s + "," + coded_counts.join(",")
				break 
			end
		end
		
		newline_map = map[index - 1] + "," + to_replace + ","
		newline_map_cod = map_cod[index - 1] + "," + to_replace_cod + ","
		map[index - 1] = newline_map
		map_cod[index - 1] = newline_map_cod
	end
end

index = 0
map.each do |line|
	index = index + 1
	values = line.split(",")
	puts "number of chromosomes: " + ((values.length) / 9).to_s
	out2.write(line + "\n")
	out3.write(map_cod[index -1] + "\n")
end

system "Rscript --vanilla ./buildMap.R " + path + folder + "matrix4map.csv " + path + folder + "chromomap.pdf"