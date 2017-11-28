# This script is for counting presence/absence of minor clades in trees
# It also says if a tree contains more than 10 leaves (criterion)
# It needs the mapping file and the gene trees database

import os

def count(path2files, treesFolder, majorClade, mappingFile, criterion):
	
	listOGs = open(path2files + "/" + mappingFile, 'r').readlines()
	out = open(path2files + "/" + 'criteriaANDcounts_out.csv', 'w')
	counts = []

	for line in listOGs:
		line = line.replace("\n", "")
		tree_code = line.split(",")[4]
		
		if tree_code != "no_tree":
			minCs = []
			op = am = pl = ex = sr = ee = ba = za = 0
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
						if ("Pl_" in minC) : pl = pl + 1	
						if ("EE_" in minC) : ee = ee + 1
						if ("Sr_" in minC) : sr = sr + 1
						if ("Ex_" in minC) : ex = ex + 1
						if ("Am_" in minC) : am = am + 1
						if ("Op_" in minC) : op = op + 1
						if ("Za_" in minC) : za = za + 1
						if ("Ba_" in minC) : ba = ba + 1
		
			# The report is corrected with criterion and counts and printed in the terminal
			
			if majorClade == "op":			
				new_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (line, criterion_meet, op, am, ex, ee, pl, sr, za, ba)
			elif majorClade == "am":
				new_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (line, criterion_meet, am, op, ex, ee, pl, sr, za, ba)
			elif majorClade == "ex":
				new_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (line, criterion_meet, ex, ee, pl, sr, am, op, za, ba)
			elif majorClade == "ee":
				new_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (line, criterion_meet, ee, pl, sr, ex, am, op, za, ba)
			elif majorClade == "pl":
				new_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (line, criterion_meet, pl, ee, sr, ex, am, op, za, ba)
			elif majorClade == "sr":
				new_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (line, criterion_meet, sr, pl, ee, ex, am, op, za, ba)
		
			print new_line
			out.write(new_line + "\n")
			counts.append(new_line)
		
		else:
			print line
			out.write("%s\n" % line)

	return str(len(listOGs)) + "," + str(len(counts))