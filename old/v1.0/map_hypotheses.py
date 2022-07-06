# The input matrix should contain all intervals with the counts
# The output matrix countain 1 or 0 for every hypothesis

# Example of first 2 lines of input matrix

#chr01	1	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00
#chr01	1001	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00

path = '/Users/marioceron/Documents/plasmodium/Saccharomyces_cerevisiae/PCM/'
inputMatrix = open(path + 'freqs4map.csv', 'r').readlines()
outputMatrix = open(path + 'outputMatrix4hypotheses.txt', 'w')


# This is the default order of the counts, you can change it according to your data
majorClades = ["Sr","Pl","Op","EE","Am","Ex","Ba","Za"]


# Here we are taking the counts and specifing to which major clade they belong
def assignCounts(counts):
	countsXmajor = {}
	index = -1
	
	for majorClade in majorClades:
		index = index + 1
		countsXmajor[majorClade] = float(counts[index])

	return countsXmajor

# Hypothesis 1: Gene originated in LUCA


def hypothesis(countsXmajor, line):
	rule = line[0].split(";")
	color = line[1]
	presence = line[2:]
	criteria = []
	clade_presence = {"Sr":presence[0],"Pl":presence[1],"Op":presence[2],"EE":presence[3],"Am":presence[4],"Ex":presence[5],"Ba":presence[6],"Za":presence[0]}

	for rule_part in rule:
		if "[" in rule_part:
			clades = rule_part.replace("[", "")
			clades = (clades.split("]")[0]).split("|")
			countCriterion = rule_part.split("]")[1]
			countCriterion_n = int(countCriterion[-1])
			countCriterion_s = ''
			if len(countCriterion) == 2 : countCriterion_s = countCriterion[0]
			
			count_clades = 0
			for clade in rule_part:
				if countsXmajor[clade] >= clade_presence[clade] : count_clades += 1
			
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

		


	if countsXmajor['Sr'] >= 0.25 : euks += 1
	if countsXmajor['Pl'] >= 0.25 : euks += 1
	if countsXmajor['Op'] >= 0.25 : euks += 1
	if countsXmajor['EE'] >= 0.25 : euks += 1 
	if countsXmajor['Am'] >= 0.25 : euks += 1 
	if countsXmajor['Ex'] >= 0.25 : euks += 1 
	if countsXmajor['Ba'] >= 0.25 : criteria += 1 
	if countsXmajor['Za'] >= 0.25 : criteria += 1 
	if euks >= 5 : criteria += 1 
	if criteria == 3:
		return 1
	else:
		return 0

def hypothesis1(countsXmajor): 
	criteria = 0
	euks = 0
	if countsXmajor['Sr'] >= 0.25 : euks += 1
	if countsXmajor['Pl'] >= 0.25 : euks += 1
	if countsXmajor['Op'] >= 0.25 : euks += 1
	if countsXmajor['EE'] >= 0.25 : euks += 1 
	if countsXmajor['Am'] >= 0.25 : euks += 1 
	if countsXmajor['Ex'] >= 0.25 : euks += 1 
	if countsXmajor['Ba'] >= 0.25 : criteria += 1 
	if countsXmajor['Za'] >= 0.25 : criteria += 1 
	if euks >= 5 : criteria += 1 
	if criteria == 3:
		return 1
	else:
		return 0 	


# Hypothesis 2: Gene originated common ancestor of Archaea and Euks

def hypothesis2(countsXmajor): 
	criteria = 0
	euks = 0
	if countsXmajor['Sr'] >= 0.25 : euks += 1
	if countsXmajor['Pl'] >= 0.25 : euks += 1
	if countsXmajor['Op'] >= 0.25 : euks += 1
	if countsXmajor['EE'] >= 0.25 : euks += 1
	if countsXmajor['Am'] >= 0.25 : euks += 1
	if countsXmajor['Ex'] >= 0.25 : euks += 1
	if countsXmajor['Ba'] < 0.25 : criteria += 1
	if countsXmajor['Za'] >= 0.25 : criteria += 1
	if euks >= 5 : criteria += 1
	if criteria == 3:
		return 1
	else:
		return 0 

# Hypothesis 3: EGT from mitochondria

def hypothesis3(countsXmajor):
	criteria = 0
	euks = 0
	if countsXmajor['Sr'] >= 0.25 : euks += 1
	if countsXmajor['Pl'] >= 0.25 : euks += 1
	if countsXmajor['Op'] >= 0.25 : euks += 1
	if countsXmajor['EE'] >= 0.25 : euks += 1
	if countsXmajor['Am'] >= 0.25 : euks += 1
	if countsXmajor['Ex'] >= 0.25 : euks += 1
	if countsXmajor['Ba'] >= 0.25 : criteria += 1
	if countsXmajor['Za'] < 0.25 : criteria += 1
	if euks >= 5 : criteria += 1
	if criteria == 3:
		return 1
	else:
		return 0 

# Hypothesis 4: EGT from plastid (relaxed)

def hypothesis4(countsXmajor):
	criteria = 0
	photoeuks = 0
	nonPhotoeuks = 0
	if countsXmajor['Sr'] >= 0.25 : photoeuks += 1
	if countsXmajor['Pl'] >= 0.25 : photoeuks += 1
	if countsXmajor['EE'] >= 0.25 : photoeuks += 1
	if countsXmajor['Op'] >= 0.25 : nonPhotoeuks += 1
	if countsXmajor['Am'] >= 0.25 : nonPhotoeuks += 1
	if countsXmajor['Ex'] >= 0.25 : nonPhotoeuks += 1
	if countsXmajor['Ba'] >= 0 : criteria += 1 
	if countsXmajor['Za'] < 0.25 : criteria += 1 
	if photoeuks >= 2 : criteria += 1
	if nonPhotoeuks == 0 : criteria += 1
	if criteria == 4:
		return 1
	else:
		return 0 

# Hypothesis 5: EGT from plastid (strict)

def hypothesis5(countsXmajor):
	criteria = 0
	photoeuks = 0
	nonPhotoeuks = 0
	if countsXmajor['Sr'] >= 0.25 : photoeuks += 1
	if countsXmajor['Pl'] >= 0.25 : photoeuks += 1
	if countsXmajor['EE'] >= 0.25 : photoeuks += 1
	if countsXmajor['Op'] >= 0.25 : nonPhotoeuks += 1
	if countsXmajor['Am'] >= 0.25 : nonPhotoeuks += 1 
	if countsXmajor['Ex'] >= 0.25 : nonPhotoeuks += 1 
	if countsXmajor['Ba'] >= 0 : criteria += 1
	if countsXmajor['Za'] < 0.25 : criteria += 1
	if photoeuks == 3 : criteria += 1 
	if nonPhotoeuks == 0 : criteria += 1
	if criteria == 4:
		return 1
	else:
		return 0 

# Hypothesis 6: Gene from common ancestor of eukaryotes

def hypothesis6(countsXmajor):
	criteria = 0
	euks = 0
	if countsXmajor['Sr'] >= 0.25 : euks += 1
	if countsXmajor['Pl'] >= 0.25 : euks += 1
	if countsXmajor['Op'] >= 0.25 : euks += 1
	if countsXmajor['EE'] >= 0.25 : euks += 1
	if countsXmajor['Am'] >= 0.25 : euks += 1
	if countsXmajor['Ex'] >= 0.25 : euks += 1 
	if countsXmajor['Ba'] < 0.25 : criteria += 1
	if countsXmajor['Za'] < 0.25 : criteria += 1
	if euks >= 5 : criteria += 1
	if criteria == 3:
		return 1
	else:
		return 0 

# Test each hypothesis

for line in inputMatrix:
	hypotesesResults = []
	line = line.replace("\n", "")
	values = line.split(",")
	chr = values[0]
	position = int(values[1])
	counts = values[2:]
	countsXmajor = assignCounts(counts)
	hypotesesResults = []
	
	hypotesesResults.append(str(hypothesis1(countsXmajor)))
	hypotesesResults.append(str(hypothesis2(countsXmajor)))
	hypotesesResults.append(str(hypothesis3(countsXmajor)))
	hypotesesResults.append(str(hypothesis4(countsXmajor)))
	hypotesesResults.append(str(hypothesis5(countsXmajor)))
	hypotesesResults.append(str(hypothesis6(countsXmajor)))
	
	print countsXmajor
	print hypotesesResults
	print "\n"
	
	outputMatrix.write(chr + "," + str(position) + "," + ",".join(hypotesesResults) + "\n")