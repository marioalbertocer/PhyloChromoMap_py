#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)
mode = args[1]

if (mode == 'pcm' || mode == 'cen') {  # phylochromomap or centromeres
	
	if (mode == 'pcm') {
		input = paste0(args[2], "/matrix4map.csv")
		output = paste0(args[2], "/chromomap.pdf")
	} else if (mode == 'cen') {
		input = paste0(args[2], "/matrix4map_centromers.csv")
		output = paste0(args[2], "/chromomap_centromers.pdf")
	}	
	
	data <- as.matrix(read.delim(input, sep=",", header=F, colClasses = "numeric"))

	op = c("#ffffff", "#d7b5d8", "#df65b0", "#ce1256")
	am = c("#ffffff", "#fcae91", "#fb6a4a", "#cb181d")
	pl = c("#ffffff", "#bae4b3", "#74c476", "#238b45")
	ex = c("#ffffff", "#bdd7e7", "#6baed6", "#2171b5")
	sr = c("#ffffff", "#fed98e", "#fe9929", "#cc4c02")
	ee = c("#ffffff", "#cbc9e2", "#9e9ac8", "#6a51a3")
	ba = c("#ffffff", "#cccccc", "#969696", "#525252")
	za = c("#ffffff", "#cccccc", "#969696", "#525252")
	criterion = c("#000000", "#ffffff")
	colors = c(op, am, pl, ex, sr, ee, ba, za, criterion)

} else if (mode == 'hm') { # hypotheses map

	input = paste0(args[2], "/outputMatrix4hypotheses.csv")
	output = paste0(args[2], "/hypothesesMap.pdf")
	data <- as.matrix(read.delim(input, sep=",", header=F, colClasses = "numeric"))

	colorsFile = read.csv(paste0(args[2], "/hypotheses.csv"), sep=",", header = F)
	a = c("white", "black")
	b = colorsFile$V2
	colors = c(a, as.character(b))
	
}

data_corrected <- data[,-1] # delete intervals
pdf(output, width=106.25,height=75) #, res=300
image(data_corrected, axes = FALSE, zlim=c(1,length(colors)), col = colors)
dev.off()
