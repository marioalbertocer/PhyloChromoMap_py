import os
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
			elif "major clade:" in parameter:
				majorClade = parameter.split(":")[1].strip()
			elif "minor clades Op" in parameter:
				minsOP = int(parameter.split(":")[1].strip())
			elif "minor clades Am" in parameter:
				minsAM = int(parameter.split(":")[1].strip())
			elif "minor clades Ex" in parameter:
				minsEX = int(parameter.split(":")[1].strip())
			elif "minor clades Pl" in parameter:
				minsPL = int(parameter.split(":")[1].strip())
			elif "minor clades EE" in parameter:
				minsEE = int(parameter.split(":")[1].strip())
			elif "minor clades Sr" in parameter:
				minsSR = int(parameter.split(":")[1].strip())
			elif "minor clades Ba" in parameter:
				minsBA = int(parameter.split(":")[1].strip())
			elif "minor clades Za" in parameter:
				minsZA = int(parameter.split(":")[1].strip())
			elif "criterion:" in parameter:
				criterion = parameter.split(":")[1].strip()
			elif "m_interval:" in parameter:
				m_interval = parameter.split(":")[1].strip()
	
	if majorClade == 'Op': 
		majors = ["Op","Am","Ex","EE","Pl","Sr","Za","Ba"]
		minorsXmajor = [minsOP, minsAM, minsEX, minsEE, minsPL, minsSR, minsZA, minsBA]													
	elif minor_clade == "Am":
		majors = ["Am","Op","Ex","EE","Pl","Sr","Za","Ba"] 
		minorsXmajor = [minsAM, minsOP, minsEX, minsEE, minsPL, minsSR, minsZA, minsBA]													
	elif minor_clade == "Ex":
		majors = ["Ex","EE","Pl","Sr","Am","Op","Za","Ba"] 
		minorsXmajor = [minsEX, minsEE, minsPL, minsSR, minsAM, minsOP, minsZA, minsBA]													
	elif minor_clade == "EE":
		majors = ["EE","Pl","Sr","Ex","Am","Op","Za","Ba"] 
		minorsXmajor = [minsEE, minsPL, minsSR, minsEX, minsAM, minsOP, minsZA, minsBA]													
	elif minor_clade == "Pl":
		majors = ["Pl","EE","Sr","Ex","Am","Op","Za","Ba"]
		minorsXmajor = [minsPL, minsEE, minsSR, minsEX, minsAM, minsOP, minsZA, minsBA]													
	elif minor_clade == "Sr":
		majors = ["Sr","Pl","EE","Ex","Am","Op","Za","Ba"]
		minorsXmajor = [minsSR, minsPL, minsEE, minsEX, minsAM, minsOP, minsZA, minsBA]													
	
	return path2files , treesFolder , chromoSizeFile , mappingFile , majorClade , minorsXmajor, majors, criterion, m_interval

def main():		
	
	rExists = os.system("which r")
	if rExists == 256:
		print "\n\nYou need to install r first\n\n"
		quit()

	rscriptExists = os.system("which Rscript")
	if rscriptExists == 256:
		print "\n\nYou need to install Rscript first\n\n"
		quit()

		
	path2files , treesFolder , chromoSizeFile , mappingFile , majorClade , minorsXmajor, majors, criterion, m_interval = get_parameters()	

	# Counting minor clades and filtering by criterion
	result_counts = TreesCriteria_counts.count(path2files, treesFolder, majorClade, mappingFile, int(criterion))

	print "total genes = " + result_counts.split(",")[0]
	print "total trees = " + result_counts.split(",")[1]

	# Mapping the information
	result_mapIntervals = Intervals.mapIntervals(path2files, m_interval, chromoSizeFile)
	
	print "number of chromosomes: " + str(result_mapIntervals['number of chromosomes'])
	print "map size: " + str(result_mapIntervals['map size'])
	print "genes mapped: " + str(result_mapIntervals['genes mapped'])
	
	# Redistributing the loci that are not clearly in an interval. 
	
	result_mapInfoHelper = MapInfoHelper.redistributeLoci(path2files)
	print result_mapInfoHelper

	result_matrix = BuildMapMatrix.BuildMatrix(path2files, minorsXmajor, majors, m_interval)
	
	os.system("rm *.pyc")
	
main()