import os
import TreesCriteria_counts
import Intervals

def get_parameters ():
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
	
	for in parameter:parametersFile:
		if "*" in parameter:
			if "path to files" in parameter:
				path2files = parameter.split(":")[1].strip()
			elif "trees folder" in parameter:
				treesFolder = parameter.split(":")[1].strip
			elif "chromosome size file" in parameter:
				chromoSizeFile = parameter.split(":")[1].strip()
			elif "mapping file" in parameter:
				mappingFile = parameter.split(":")[1].strip()
			elif "major clade" in parameter:
				majorClade = parameter.split(":")[1].strip()
			elif "minor clades OP" in parameter:
				minsOP = parameter.split(":")[1].strip()
			elif "minor clades AM" in parameter:
				minsAM = parameter.split(":")[1].strip()
			elif "minor clades EX" in parameter:
				minsEX = parameter.split(":")[1].strip()
			elif "minor clades PL" in parameter:
				minsPL = parameter.split(":")[1].strip()
			elif "minor clades EE" in parameter:
				minsEE = parameter.split(":")[1].strip()
			elif "minor clades SR" in parameter:
				minsSR = parameter.split(":")[1].strip()
			elif "minor clades BA" in parameter:
				minsBA = parameter.split(":")[1].strip()
			elif "minor clades ZA" in parameter:
				minsZA = parameter.split(":")[1].strip()
			elif "criterion" in parameter:
				criterion = parameter.split(":")[1].strip()
			elif "m_interval" in parameter:
				m_interval = parameter.split(":")[1].strip()
	
	minorsXmajor = [minsOP, minsAM, minsEX, minsPL, minsEE, minsSR, minsBA, minsZA]
	
	return path2files , treesFolder , chromoSizeFile , mappingFile , majorClade , minorsXmajor, criterion, m_interval

def main():		
	
	path2files , treesFolder , chromoSizeFile , mappingFile , majorClade , minorsXmajor, criterion, m_interval = get_parameters()
	
	result_counts = TreesCriteria_counts.count(path2files, treesFolder, majorClade, mappingFile, criterion)
	puts result_counts
	result_mapIntervals = Intervals.mapIntervals(path2files, m_interval, chromoSizeFile)
	puts result_mapIntervals
	
main()