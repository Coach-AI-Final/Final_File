import csv
import os


def interpolation_function(*args):

	set_num = 1
	while set_num <= 2:
		score_A = 0
		score_B = 0
		while score_A < 22:
			interpolate_table = []
			if score_B == 21:
				score_A = score_A + 1
				score_B = 0
			else:
				score_B = score_B + 1
			infile = str(set_num)+"_"+(str(score_A)).zfill(2)+"_"+(str(score_B)).zfill(2)+".csv"
			if os.path.isfile(infile) == False:
				continue

			with open(infile, newline='') as csvfile:
				data = list(csv.reader(csvfile))
			j = 0
			for row in data:
				interpolate_table.append([])
				interpolate_table[-1].append(row[0])
				if j < 2 or j == len(data)-1:
					interpolate_table[-1].append(row[1])
					interpolate_table[-1].append(row[2])
				else :
					interpolate_table[-1].append(round(float(data[j-1][1])*float(float(float(data[j+1][0])-float(data[j][0]))/float(float(data[j+1][0])-float(data[j-1][0])))+
												float(data[j+1][1])*float(float(float(data[j][0])-float(data[j-1][0]))/float(float(data[j+1][0])-float(data[j-1][0])))))
					interpolate_table[-1].append(round(float(data[j-1][2])*float(float(float(data[j+1][0])-float(data[j][0]))/float(float(data[j+1][0])-float(data[j-1][0])))+
												float(data[j+1][2])*float(float(float(data[j][0])-float(data[j-1][0]))/float(float(data[j+1][0])-float(data[j-1][0])))))
				j = j + 1
			#print(interpolate_table)
			if '.csv' in infile:
				infile = infile[0:infile.find('.csv')]
			with open(infile+'_interpolation.csv','w',newline='') as interp:
				writer = csv.writer(interp)
				writer.writerows(interpolate_table)
				print('Save output file as '+infile+'_interpolation.csv')
					
		set_num = set_num + 1