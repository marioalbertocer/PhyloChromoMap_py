#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)
input = args[1]
output = args[2]

data <- as.matrix(read.table(input, sep=",", header=F))
data_corrected <- data[,-1] # delete intervals 
pdf(output, width=106.25,height=75) #, res=300)

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

image(data_corrected, axes = FALSE, zlim=c(1,34), col = colors)
dev.off()