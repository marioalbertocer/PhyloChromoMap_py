# This script is for counting presence/absence of minor clades in trees
# It also says if a tree contains more than 10 leaves (criterion)
# It needs the report from screipt bestOGsXseq

import os

path = '/Users/marioceron/Documents/katzlab/duplications/orthomcl-release5/'
folder = 'Saccharomyces_cerevisiae/'

# Reading report of bestOGsXseq...
listOGs = open(path + folder + 'bestOGsXseq_out.txt', 'r')
out = open(path + folder + 'criteriaANDcounts_out.txt', 'w')
listOGs = listOGs.readlines()

for line in listOGs:
	line = line.replace('\n', '')
	
	#some of the lines in the report say that there is not an OG, so it avoids those ones
	if 'OG5_' in line:
		og = line.split('\t')[2]
		
		minCs = []
		
		op = am = pl = ex = sr = ee = ba = za = 0
		criterion = 'no'

		# for each OG read the folder of the trees and read the tree for the OG
		for i in os.listdir(path + 'Pipelinev2_2_archive/'):
			
			if og in i:
				tree = open(path + 'Pipelinev2_2_archive/' + i, 'r')
				tree = tree.readline()
				
				# As the trees are in neweck format, we can make a list of leaves by 
				# splitting the tree by the comas.
				tree = tree.split(',') 

				# if there are more than 10 leaves in the tree, it meets the criterion
				if len(tree) > 10:
					criterion = 'yes'
				
					# Here we are going to clean the leaves, so that we can extract
					# the major clade and minor clade (e.g., Sr_di).
					# We collect all cleaned leaves in a list.
					for leaf in tree:
						leaf = leaf.replace('(', '')
						leaf = leaf.replace(')', '')
						leaf = leaf.split('_')
						minC = leaf[0] + "_" + leaf[1]
						minCs.append(minC)
				
				# Now that we have all the leaves (as Sr_di) in a list, we need to 
				# remove duplicates:
				minCs_uniq = set(minCs)
				minCs_uniq = list(minCs_uniq)
				
				# Finally, we count the number of minor clades per major clade there are 
				# in the tree. 
				for minC in minCs_uniq:
					if 'Op_' in minC : op = op + 1
					if 'Am_' in minC : am = am + 1
					if 'Pl_' in minC : pl = pl + 1					
					if 'Ex_' in minC : ex = ex + 1					
					if 'Sr_' in minC : sr = sr + 1				
					if 'EE_' in minC : ee = ee + 1
					if 'Ba_' in minC : ba = ba + 1
					if 'Za_' in minC : za = za + 1

		# The report is corrected with criterion and counts and printed in the terminal
		print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (line, og, criterion, op, am, pl, ex, sr, ee, ba, za)
		out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (line, og, criterion, op, am, pl, ex, sr, ee, ba, za))
	else:
		print line
		out.write("%s\n" % line)