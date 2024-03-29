# This script is for counting presence/absence of minor clades in trees
# It also says if a tree contains more than 10 leaves (criterion)
# It needs the mapping file and the gene trees database

import os

def count(path2files, treesFolder, majorClade, majors, mappingFile, criterion):
	
	listOGs = open(path2files + "/" + mappingFile, 'r').readlines()
	out = open(path2files + "/" + 'criteriaANDcounts_out.csv', 'w')
	counts = []

	for line in listOGs:
		line = line.replace("\n", "")
		tree_code = line.split(",")[4]
		
		if tree_code != "no_tree":
			minCs = []
			minCscounts = {}
			for major in majors: minCscounts[major] = 0
			criterion_meet = 'no'

			# take each gene tree from the gene trees database
			for i in os.listdir(path2files + "/" + treesFolder):
				if tree_code in i:
					tree = open(path2files + "/" + treesFolder + "/" + i, 'r').readline()

					# As the trees are in neweck format, we can make a list of leaves by 
					# splitting the tree by the comas.
					tree = tree.split(',')

					# if there are more than X leaves in the tree, it meets the criterion
					# X is defined by the user in the parameters file
					if len(tree) > int(criterion):
						criterion_meet = 'yes'

					# Here we are going to clean the leaves, so that we can extract
					# the major clade and minor clade (e.g., Sr_di).
					# We collect all cleaned leaves in a list.
					for leaf in tree:
						leaf = leaf.replace("(", "")
						leaf = leaf.replace(")", "")
						leaf = leaf.split("_")
						minCs.append(leaf[0] + "_" + leaf[1])

					# Now that we have all the leaves (as Sr_di) in a list, we need to 
					# remove duplicates:
					minCs = list(set(minCs))

					# Finally, we count the number of minor clades per major clade there are 
					# in the tree. 
					for minC in minCs:
						for k in minCscounts.keys():
							if k == minC.split("_")[0]: 
								minCscounts[k] += 1
									
			# The report is corrected with criterion and counts and printed in the terminal
			new_line = "%s,%s" % (line, criterion_meet)
			for major in majors: new_line += "," + str(minCscounts[major])
			print(new_line)
			out.write(new_line + "\n")
			counts.append(new_line)
		
		else:
			print(line)
			out.write("%s\n" % line)

	return str(len(listOGs)) + "," + str(len(counts))