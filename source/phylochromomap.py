import os, sys
import TreesCriteria_counts
import Intervals
import MapInfoHelper
import BuildMapMatrix

def get_parameters():
	path2files = ''
	treesFolder = ''
	chromoSizeFile = ''
	mappingFile = ''
	majorClade = ''
	minsOP = ''
	minsAM = ''
	minsEX = ''
	minsPL = ''
	minsEE = ''
	minsSR = ''
	minsBA = ''
	minsZA = ''
	criterion = ''
	m_interval = ''

	parametersFile = open('parametersFile.txt', 'r').readlines()
	minorsXmajor = {}
	colors = {} 
	for parameter in parametersFile:
		if "*" in parameter:
			if "path to files:" in parameter:
				path2files = parameter.split(":")[1].strip()
			elif "trees folder:" in parameter:
				treesFolder = parameter.split(":")[1].strip()
			elif "chromosome size file:" in parameter:
				chromoSizeFile = parameter.split(":")[1].strip()
			elif "mapping file:" in parameter:
				mappingFile = parameter.split(":")[1].strip()
			elif "major clades:" in parameter:
				majors = list(map(lambda x: x.strip(), (parameter.split(":")[1]).split(",")))
			elif "major clade:" in parameter:
				majorClade = parameter.split(":")[1].strip()				
			elif "minor clades" in parameter:
				major = (parameter.split("-")[1].split(":")[0]).strip()
				minors = int((parameter.split(":")[1]).strip())
				minorsXmajor[major] = minors
			elif "criterion:" in parameter:
				criterion = parameter.split(":")[1].strip()
			elif "m_interval:" in parameter:
				m_interval = parameter.split(":")[1].strip()
			elif "color codes" in parameter:
				major = (parameter.split("-")[1].split(":")[0]).strip()
				colors_inf = (parameter.split(":")[1]).split(",")
				colors[major] = []
				for color in colors_inf: colors[major].append(color.strip())
				
	return path2files , treesFolder , chromoSizeFile , mappingFile , majorClade , minorsXmajor, majors, criterion, m_interval, colors

def main():		
	
	rExists = os.system("which r")
	if rExists == 256:
		print("\n\nYou need to install r first\n\n")
		quit()

	rscriptExists = os.system("which Rscript")
	if rscriptExists == 256:
		print("\n\nYou need to install Rscript first\n\n")
		quit()
		
	path2files , treesFolder , chromoSizeFile , mappingFile , majorClade , minorsXmajor, majors, criterion, m_interval, colors = get_parameters()	

	# Creating file with the color codes per major clade
	colors_file = open(path2files + "/" + 'colorCodes.csv', 'w')
	colors_file.write("MC,[0-25],(0.25-0.5],(0.5-0.75],(0.75-1]")
	for major in majors:
		for mc, col in colors.items():
			if major == mc:
				col_codes = ",".join(col)
				colors_file.write("\n" + mc + "," + col_codes)
	colors_file.close()
		
	# Counting minor clades and filtering by criterion
	result_counts = TreesCriteria_counts.count(path2files, treesFolder, majorClade, majors, mappingFile, int(criterion))

	print("total genes = " + result_counts.split(",")[0])
	print("total trees = " + result_counts.split(",")[1])

	# Mapping the information
	result_mapIntervals = Intervals.mapIntervals(path2files, m_interval, chromoSizeFile)
	
	print("number of chromosomes: " + str(result_mapIntervals['number of chromosomes']))
	print("map size: " + str(result_mapIntervals['map size']))
	print("genes mapped: " + str(result_mapIntervals['genes mapped']))
	
	# Redistributing the loci that are not clearly in an interval. 
	
	result_mapInfoHelper = MapInfoHelper.redistributeLoci(path2files, majors)
	print(result_mapInfoHelper)

	result_matrix = BuildMapMatrix.BuildMatrix(path2files, minorsXmajor, majors, m_interval)
	
#	os.system("rm *.pyc")
	
main()