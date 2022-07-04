import os

parametersFile = open('parametersFile.txt', 'r').readlines()

for parameter in parametersFile:
	if "*" in parameter:
		if "path to files:" in parameter:
			path2files = parameter.split(":")[1].strip()
		elif "chromosome size file:" in parameter:
			chromoSizeFile = parameter.split(":")[1].strip()

matrix = open(path2files + '/matrix4map.csv', 'r').readlines()
centromeres = open(path2files + "/" + chromoSizeFile, 'r').readlines()
out = open(path2files + '/matrix4map_centromers.csv', 'w')

chr = 0
chrINmatrix = 0
interval = 1000

for centromeres_line in centromeres:
	centromeres_line = centromeres_line.replace("\n", "")
	chrINmatrix = (chr * 11) + 1
	chr += 1
	centromere = []
	
	chromosize = centromeres_line.split(',')[1]
	centroS = centromeres_line.split(',')[2]
	centroS_rounded = int(round((float(centroS) / float(interval)), 0)) * interval
	centroE = centromeres_line.split(',')[3]
	centroE_rounded = int(round((float(centroE) / float(interval)), 0)) * interval
	for i in range(centroS_rounded, centroE_rounded, interval) : centromere.append(i + 1)
	if not centromere : centromere.append(centroS_rounded + 1)
	if len(centromere) == 1 and centromere[0] == 1 : centromere[0] = 0

	line_index = 0
	for line_matrix in matrix: 
		fields = line_matrix.split(",")
		if int(fields[0]) in centromere:
			fields[chrINmatrix] = "7"
			print(centromeres_line + "\t" + "done")
			newline = ",".join(fields)
			matrix[line_index] = newline
			
		line_index += 1 
			
for line in matrix:
	out.write("%s" % line)
		
out.close() 
		
os.system("Rscript --vanilla buildMap.R cen " + path2files)