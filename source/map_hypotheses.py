# Based on the frequency of minor clades per major clade, this sprit test 
# a set of hypotheses of gene conservation. For instance, if genes are conserved 
# between particular major clades. The user set the hypotheses to test.

import os

parametersFile = open('parametersFile.txt', 'r').readlines()

for parameter in parametersFile:
	if "path to files:" in parameter:
		path2files = parameter.split(":")[1].strip()
	elif "major clade:" in parameter:
		majorClade = parameter.split(":")[1].strip()
	elif "chromosome size file:" in parameter:
		chromoSizeFile = parameter.split(":")[1].strip()

inputMatrix = open(path2files + '/freqs4map.csv', 'r').readlines()
outputMatrix = open(path2files + '/outputMatrix4hypotheses.csv', 'w')
hypotheses = open(path2files + '/hypotheses.csv', 'r').readlines()
chromosomesFile = open(path2files + "/" + chromoSizeFile, 'r').readlines()

# Number of hypotheses:

hypo_num = 0
print("\n------- Hypotheses: --------")
for hypothesis in hypotheses:
	hypothesis = hypothesis.split(",")[0]
	print(hypothesis)
	if hypothesis : hypo_num += 1
print("----------------------------\n")

# intervals

intervals = []
for line in inputMatrix:
	interval = int(line.split(",")[1])
	if interval not in intervals : intervals.append(interval)

# chromosomes

chromosomes = []
for line in chromosomesFile:
	chromosome = line.split(',')[0]
	chromosomes.append(chromosome) 

# This is the default order of the counts, you can change it according to your data

if majorClade == 'Op' : majorClades = ["Op","Am","Ex","EE","Pl","Sr","Za","Ba"]
elif majorClade == "Am" : majorClades = ["Am","Op","Ex","EE","Pl","Sr","Za","Ba"] 
elif majorClade == "Ex" : majorClades = ["Ex","EE","Pl","Sr","Am","Op","Za","Ba"] 
elif majorClade == "EE": majorClades = ["EE","Pl","Sr","Ex","Am","Op","Za","Ba"] 
elif majorClade == "Pl": majorClades = ["Pl","EE","Sr","Ex","Am","Op","Za","Ba"]
elif majorClade == "Sr": majorClades = ["Sr","Pl","EE","Ex","Am","Op","Za","Ba"]

# Here we are taking the counts and specifing to which major clade they belong

def assignCounts(counts):
	countsXmajor = {}
	index = -1
	
	for majorClade in majorClades:
		index = index + 1
		countsXmajor[majorClade] = float(counts[index])

	return countsXmajor


def hypothesis(countsXmajor, hypo_line, color):
	rule = hypo_line[0].split(";")
#	color = hypo_line[1]
	presence = hypo_line[2:]
	criteria = []
	clade_presence = {
		majorClades[0]:presence[0],
		majorClades[1]:presence[1],
		majorClades[2]:presence[2],
		majorClades[3]:presence[3],
		majorClades[4]:presence[4],
		majorClades[5]:presence[5],
		majorClades[6]:presence[6],						
		majorClades[7]:presence[7]
	}

	for rule_part in rule:
	
		if "[" in rule_part:
			clades = rule_part.replace("[", "")
			clades = (clades.split("]")[0]).split("|")
			countCriterion = rule_part.split("]")[1]
			countCriterion_n = int(countCriterion[-1])
			countCriterion_s = ''
			if len(countCriterion) == 2: countCriterion_s = countCriterion[0]
			
			count_clades = 0
			for clade in clades:
				if countsXmajor[clade] >= float(clade_presence[clade]) : count_clades += 1
			
			if countCriterion_s:

				if countCriterion_s == '+':
					if count_clades >= countCriterion_n:
						criteria.append('yes')
					else:
						criteria.append('no')

				if countCriterion_s == '-':
					if count_clades <= countCriterion_n:
						criteria.append('yes')
					else:
						criteria.append('no')
		
			else:
				if count_clades == countCriterion_n:
					criteria.append('yes')
				else:
					criteria.append('no')
					
		elif '*' in rule_part:
			clade = rule_part.replace('*', '')
			if countsXmajor[clade] >= float(clade_presence[clade]):
				criteria.append('no')
			else: 
				criteria.append('yes')
				
		elif '?' in rule_part:
			clade = rule_part.replace('?', '')
			criteria.append('yes')
		
		else:
			clade = rule_part
			if countsXmajor[clade] >= float(clade_presence[clade]):
				criteria.append('yes')
			else: 
				criteria.append('no')
	
	if 'no' in criteria:
		return ["0", "1"]
	else:
		return ["1", str(color)]

#Test each hypothesis

print("\n--------Test hypothese by interval:-----------")
map = []
for i in intervals : map.append(i)

for chromosome in chromosomes:

	if chromosome == inputMatrix[0].split(",")[0]:

		index = 0 
		for interval in intervals:
			
			index = index + 1
			interval_only = str(interval)
			to_replace = ",".join([""] * (hypo_num + 1))
			real_counts = ",".join([""] * hypo_num)

			if inputMatrix:
				if str(interval) == inputMatrix[0].split(',')[1]:			
					values = inputMatrix[0].replace("\n", "")
					values = values.split(",")
					del inputMatrix[0]
					hypotesesResults = []
					hypotesesResults_real = []
					counts = values[2:]
					countsXmajor = assignCounts(counts)

					color = 2
					for hypo_line in hypotheses:
						color += 1
						hypo_line = hypo_line.replace("\n", "")
						hypo_line = hypo_line.split(',')
						hypotesesResults.append(str((hypothesis(countsXmajor, hypo_line, color))[1]))
						hypotesesResults_real.append(str((hypothesis(countsXmajor, hypo_line, color))[0]))
					to_replace = "2," + ",".join(hypotesesResults)
					real_counts = ",".join(hypotesesResults_real)
			
			if real_counts != "," * (hypo_num - 1) : print(chromosome + "\t" + str(interval) + "\t" + real_counts)
			newline_map = str(map[index - 1]) + "," + to_replace + ","
			map[index - 1] = newline_map
print("\n------------------------------------------\n")
		
# build matrix
		
index = 0
for line in map:
	index = index + 1
	values = line.split(",")
	outputMatrix.write(line + "\n")	

# Draw map

os.system("Rscript --vanilla buildMap.R hm " + path2files)