import os

def BuildMatrix(path2files, totalMinors, majors, m_interval):

	# Paths and values to be set.
	inFile = open(path2files + "/" + 'mapInfo_corrected.csv', 'r').readlines()
	criteriaFile = open(path2files + "/" + 'criteriaANDcounts_out.csv', 'r').readlines()
	chrs_info = open(path2files + "/" + 'chromosize.csv', 'r').readlines()

	out1 = open(path2files + "/" + 'freqs4map.csv', 'w')
	out2 = open(path2files + "/" + 'matrix-raw.csv', 'w')
	out3 = open(path2files + "/" + 'matrix4map.csv', 'w')

	# This is the codes for assigning colors to the values:

	#	Op	Am	Pl	Ex	Sr	EE	Ba	Za
	#[0-25]	1	5	9	13	17	21	25	29
	#(0.25-0.5]	2	6	10	14	18	22	26	30
	#(0.5-0.75]	3	7	11	15	19	23	27	31
	#(0.75-1]	4	8	12	16	20	24	28	32

	# Notice that [ and ] represent close interval and ( and ) represent open interval

	minor_code = {}
	
	minor_code["Op"] = "1,2,3,4"
	minor_code["Am"] = "5,6,7,8"
	minor_code["Pl"] = "9,10,11,12"
	minor_code["Ex"] = "13,14,15,16"
	minor_code["Sr"] = "17,18,19,20"
	minor_code["EE"] = "21,22,23,24"
	minor_code["Ba"] = "25,26,27,28"
	minor_code["Za"] = "29,30,31,32"

	young_code = {}
	young_code["y"] = 33
	young_code["n"] = 34

	# Here we are extracting the loci of the young CDSs from the seqs folder. The young loci 
	# will be also mapped
	young_loci = []

	for line in criteriaFile:
		if "yes" not in line:
			chr = line.split(",")[0]
			locus = str(line.split(",")[1])
			young_loci.append(chr + "," + locus)
			print chr + "\t" + locus

	intervals = []
	freqs = []
	for line in inFile:
		line = line.strip()
		values = line.split(",")
	
		chr = values[0]
		interval = values[1]
		if interval not in intervals:
			intervals.append(interval)
	
		if len(values) > 2:
			
			m0 = round((float(values[5].replace("counts:", "")) / float(totalMinors[0])), 2)			
			m1 = round((float(values[6]) / float(totalMinors[1])), 2)
			m2 = round((float(values[7]) / float(totalMinors[2])), 2)
			m3 = round((float(values[8]) / float(totalMinors[3])), 2)
			m4 = round((float(values[9]) / float(totalMinors[4])), 2)
			m5 = round((float(values[10]) / float(totalMinors[5])), 2)
			m6 = round((float(values[11]) / float(totalMinors[6])), 2)			
			m7 = round((float(values[12]) / float(totalMinors[7])), 2)

			counts = ",".join(map(str, [m0, m1, m2, m3, m4, m5, m6, m7]))
			young = "n"
		else:
			counts = ",".join("0" * 8)
		
			for locus in young_loci:
				chr_y = locus.split(",")[0]
				locus = locus.split(",")[1]
			
				young = "n"
				if chr == chr_y:
					if int(locus) >= int(interval):
						if int(locus) < (int(interval) + int(m_interval)):
							young = "y"
							break

		print chr + "\t" + str(interval) + "\t" + young + "\t" + counts
		freqs.append(chr + "," + str(interval) + "," + young + "," + counts)
		out1.write(chr + "," + str(interval) + "," + counts + "\n")

	chrs = []
	for chr in chrs_info:
		chr = chr.split(",")[0]
		chrs.append(chr)	
	

	
	print "\n-------- Building map matrix: -----------"

	chrmap = []
	chrmap_cod = []
	for i in intervals : 
		chrmap.append(i)
		chrmap_cod.append(i)

	for chr in chrs:

		if chr == freqs[0].split(",")[0]:

			index = 0 
			for interval in intervals:
				index = index + 1
				interval_only = str(interval)
				to_replace_cod = ",".join([""] * 10)
				to_replace = ",".join([""] * 9)

				if freqs:
					if str(interval) == freqs[0].split(',')[1]:
						seq2map = freqs[0]
						seq2map = seq2map.split(",")
						del freqs[0]
						to_replace = ",".join(seq2map[2 : len(seq2map)])
						counts2cod = seq2map[3 : len(seq2map)]
						minor = 0
						coded_counts = []
						coded_young = ""
						
						for minor_count in counts2cod:
							minor = minor + 1 
																
							if (float(minor_count) >= 0) and (float(minor_count) <= 0.25):
								minor_count_cod = minor_code[majors[minor - 1]].split(",")[0]
								coded_counts.append(minor_count_cod)
								continue

							if (float(minor_count) > 0.25) and (float(minor_count) <= 0.5):
								minor_count_cod = minor_code[majors[minor - 1]].split(",")[1]
								coded_counts.append(minor_count_cod)
								continue

							if (float(minor_count) > 0.5) and (float(minor_count) <= 0.75):
								minor_count_cod = minor_code[majors[minor - 1]].split(",")[2]
								coded_counts.append(minor_count_cod)
								continue
			
							if (float(minor_count) >= 0.75) and (float(minor_count) <= 1):
								minor_count_cod = minor_code[majors[minor - 1]].split(",")[3]
								coded_counts.append(minor_count_cod)
								continue
				
						if "y" in seq2map[2] or "n" in seq2map[2]:
							coded_young = young_code[seq2map[2]]
				
						to_replace_cod = str(young_code["y"]) + "," + str(coded_young) + "," + ",".join(coded_counts)

				if to_replace != "," * 8 : print chr + "\t" + str(interval) + "\t" + to_replace
				newline_map = str(chrmap[index - 1]) + "," + to_replace + ","
				newline_map_cod = str(chrmap_cod[index - 1]) + "," + to_replace_cod + ","
				chrmap[index - 1] = newline_map
				chrmap_cod[index - 1] = newline_map_cod						
				
				
	print "\n------------------------------------------\n"	
	
	index = 0
	for line in chrmap:

		index = index + 1
		values = line.split(",")
#		print "number of chromosomes: " + str(len(values) / 9)
		out2.write(line + "\n")
		out3.write(chrmap_cod[index -1] + "\n")
#		out3.write(map_cod[index -1] + "\n")

	os.system("Rscript --vanilla ./buildMap.R pcm " + path2files)