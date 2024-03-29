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
	colors_file = paste0(args[2], "/colorCodes.csv")
	colors <- read.table(colors_file, sep=",", header = T, comment.char = "")
	colors <- colors[,-1]
	colors <- as.vector(t(colors))
	criterion = c("#000000", "#ffffff")
	chr_color <- "#000000"
	colors = c(colors, criterion, chr_color)
	
	if (mode == 'cen') {
		cenColor <- "#fb6a4a"
		colors = c(colors, cenColor)
	}

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
