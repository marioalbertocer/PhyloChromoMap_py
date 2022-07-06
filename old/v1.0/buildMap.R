#library(RColorBrewer)

#pdf('~/Documents/plasmodium/map/map_Estherdata/r/Rplot2.pdf')
#png('~/Documents/plasmodium/map/map_Estherdata/r/Rplot2-FAMILIES2.png',width=4250,height=3000)
#png('~/Documents/plasmodium/map/map_Estherdata/r/young/recoded.png',width=4250,height=3000)
#pdf('~/Documents/plasmodium/map/map_Estherdata/r/young/recoded.pdf',width=4250,height=3000)
#pdf('~/Documents/plasmodium/map/map_Estherdata/r/var2.pdf', width=106.25,height=75, res=300) #
#pdf('~/Documents/plasmodium/map/map_Estherdata/r/rif.pdf', width=106.25,height=75)
pdf('~/Documents/katzlab/duplications/orthomcl-release5/Dictyostelium_discoideum/chromomap.pdf', width=106.25,height=75)#, res=300)
#png('~/Documents/plasmodium/map/map_Estherdata/r/rif.png', width=4250,height=3000)
#svg('~/Documents/plasmodium/map/map_Estherdata/r/Rplot2.svg',width=300,height=300)


#hm.colors = c("white", "black", "gray", "red", "violet", "blue", "gold", "tan", "yellow", "cyan", "navy", "orange")

#hm.colors = c("#fee5d9", "#fcbba1", "#fc9272", "#fb6a4a", "#de2d26", "#a50f15", "#edf8e9", "#c7e9c0", "#a1d99b", "#74c476", "#31a354", "#006d2c", "#f2f0f7", "#dadaeb", "#bcbddc", "#9e9ac8", "#756bb1", "#54278f", "#eff3ff", "#c6dbef", "#9ecae1", "#6baed6", "#3182bd", "#08519c", "#f1eef6", "#d4b9da", "#c994c7", "#df65b0", "#dd1c77", "#980043", "#ffffd4", "#fee391", "#fec44f", "#fe9929", "#d95f0e", "#993404", "#ffffff", "#d9d9d9", "#bdbdbd", "#969696", "#636363", "#252525", "#ffffff", "#d9d9d9", "#bdbdbd", "#969696", "#636363", "#252525", "#ffffff", "#000000")

#hm.colors = c("#fee5d9", "#fcae91", "#fb6a4a", "#cb181d", "#edf8e9", "#bae4b3", "#74c476", "#238b45", "#f1eef6", "#d7b5d8", "#df65b0", "#ce1256", "#eff3ff", "#bdd7e7", "#6baed6", "#2171b5", "#f2f0f7", "#cbc9e2", "#9e9ac8", "#6a51a3", "#ffffd4", "#fed98e", "#fe9929", "#cc4c02", "#ffffff", "#cccccc", "#969696", "#525252", "#ffffff", "#cccccc", "#969696", "#525252", "#ffffff", "#000000")

hm.colors = c("#ffffff", "#fcae91", "#fb6a4a", "#cb181d", "#ffffff", "#bae4b3", "#74c476", "#238b45", "#ffffff", "#bdd7e7", "#6baed6", "#2171b5", "#ffffff", "#cbc9e2", "#9e9ac8", "#6a51a3", "#ffffff", "#d7b5d8", "#df65b0", "#ce1256", "#ffffff", "#fed98e", "#fe9929", "#cc4c02", "#ffffff", "#cccccc", "#969696", "#525252", "#ffffff", "#cccccc", "#969696", "#525252", "#000000", "#ffffff")

#hm.colors = c('#fcae91','#fb6a4a', '#cb181d', '#bae4b3', '#74c476', '#238b45', '#bdd7e7', '#6baed6', '#2171b5', '#cbc9e2', '#9e9ac8', '#6a51a3', '#d7b5d8', '#df65b0', '#ce1256', '#fed98e', '#fe9929', '#cc4c02', '#cccccc', '#969696', '#525252', '#cccccc', '#969696', '#525252', '#000000')


#hm.colors = c("white", "gray 85", "gray 83", "gray 81", "gray 79", "gray 77", "gray 75", "gray 73", "gray 71", "gray 69", "gray 67", "gray 65", "gray 63", "gray 61", "gray 59", "gray 57", "gray 55", "gray 51", "gray 47", "gray 45", "gray 43", "gray 39", "gray 25", "black") 

#hm.colors = c("white", "gray 85", "gray 83", "gray 81", "gray 79", "gray 77", "gray 75", "gray 73", "gray 71", "gray 69", "gray 67", "gray 65", "gray 63", "gray 61", "gray 59", "gray 57", "gray 55", "gray 53", "gray 51", "gray 49", "gray 47", "gray 45", "gray 43", "gray 41", "gray 39", "gray 37", "gray 35", "gray 33", "gray 31", "gray 29", "gray 27", "gray 25", "gray 23", "gray 21", "gray 19", "black")

#hm.colors = c("white", "gray 83", "gray 77", "gray 71", "gray 65", "gray 59", "gray 53", "gray 47", "gray 41", "gray 35", "gray 29", "gray 23", "gray 19", "black")

#hm.colors = c("white", "rosybrown1", "salmon", "orangered3", "orangered4")

# "#ffffff", "#bfd3e6", "#9ebcda", "#8c96c6", "#8856a7", "#810f7c",


#marker1 <- brewer.pal(n = 6, name = "Greens")
#marker2 <- brewer.pal(n = 6, name = "Reds")
#marker3 <- brewer.pal(n = 6, name = "Blues")
#marker4 <- brewer.pal(n = 6, name = "Purples")
#marker5 <- brewer.pal(n = 6, name = "Greys")
#marker6 <- brewer.pal(n = 6, name = "RdPu")
#marker7 <- brewer.pal(n = 6, name = "YlOrBr")
#marker8 <- brewer.pal(n = 6, name = "Oranges")
#marker9 <- c('black', 'black')

#hm.colors = c("white", marker1, marker2, marker3, marker4, marker5, marker6, marker7, marker8, "black")  #marker9



data <- as.matrix(read.table("~/Documents/katzlab/duplications/orthomcl-release5/Dictyostelium_discoideum/matrix4map.txt", sep="\t", header=F))
#data <- as.matrix(read.table("~/Documents/plasmodium/map/map_Estherdata/r/young/matrix.txt", sep="\t", header=F))

data1 <- data[,-1] # delete intervals 

#heatmap(data, Colv= NA, Rowv= NA, col = hm.colors, breaks = breaks, keep.dendro=F)

image(data1, axes = FALSE, zlim=c(1,34), col = hm.colors) #  breaks = seq(0:51)
#image(data, axes = FALSE, zlim=c(0,13), col = colorRampPalette(c("lightgoldenrodyellow", "midnightblue"))(14) ) #  breaks = seq(0:51)

dev.off()
