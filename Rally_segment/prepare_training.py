import csv
import os
import pandas as pd

set_num = 1

while set_num <= 3:
	score_A = 0
	score_B = 0
	while score_A < 22:
		turning_time = []
		data_list = []
		start_frame = 0
		turning_frame = []
		if score_B == 21:
			score_A = score_A + 1
			score_B = 0
		else:
			score_B = score_B + 1
		rally_score = str(set_num)+"_"+(str(score_A)).zfill(2)+"_"+(str(score_B)).zfill(2)
		infile = rally_score + ".csv"
		if os.path.isfile(infile) == False:
			continue
		with open("RallySeg.csv", newline='') as index_file:
			rows = csv.DictReader(index_file)
			for row in rows:
				if row['Score'] == rally_score:
					start_frame = int(row['Start'])
					break

		with open("set"+str(set_num)+".csv", newline='',encoding='utf-8') as turning_file:
			rows = csv.DictReader(turning_file)
			for row in rows:
				if int(row['roundscore_A'])==score_A and int(row['roundscore_B'])==score_B:
					turning_frame.append(float(row['frame_num'])-start_frame)
		data_list.append([])
		data_list[-1].append('Frame')
		data_list[-1].append('Visibility')
		data_list[-1].append('X')
		data_list[-1].append('Y')			
		with open(infile, newline='') as csvfile:
			rows = csv.DictReader(csvfile)
			for row in rows:
				data_list.append([])
				data_list[-1].append(row['Frame'])
				data_list[-1].append(row['Visibility'])
				data_list[-1].append(row['X'])
				data_list[-1].append(row['Y'])

		

		"""	first = True
			for row in rows:
				data_list.append([])
				if first:
					data_list[-1].append(row['Frame'])
					data_list[-1].append(row['Visibility'])
					data_list[-1].append(row['X'])
					data_list[-1].append(row['Y'])
					data_list[-1].append(0)
					data_list[-1].append(0)
					index = int(row['index'])
					x = int(row['x'])
					y = int(row['y'])
					if int(row['Visibility']) == 1:
						first = False
				else:
					data_list[-1].append(row['index'])
					data_list[-1].append(row['x'])
					data_list[-1].append(row['y'])
					data_list[-1].append(round((int(row['x'])-x)/((int(row['index'])-index)),3))
					data_list[-1].append(round((int(row['y'])-y)/((int(row['index'])-index)),3))
					index = int(row['index'])
					x = int(row['x'])
					y = int(row['y'])
				j = j + 1

			j = 0
			for row in data_list:
				if j == 0:
					data_list[j].append('ax')
					data_list[j].append('ay')
					j = j + 1
					continue
				elif j <= 2:
					data_list[j].append(0)
					data_list[j].append(0)
				else:
					data_list[j].append(round((float(row[3])-Vx)/((int(row[0])-index)),3))
					data_list[j].append(round((float(row[4])-Vy)/((int(row[0])-index)),3))
				index = int(row[0])
				Vx = float(row[3])
				Vy = float(row[4])
				j = j + 1
		"""
		j = 0
		i = 0
		for row in data_list:
			if j == 0:
				data_list[j].append('turning_point')
			else:
				if len(turning_frame)==0:
					data_list[j].append(0)
				elif i>=len(turning_frame):
					data_list[j].append(0)
				elif j == len(data_list) - 1:
					data_list[j].append(1)
				elif abs(int(data_list[j][0]) - turning_frame[i]) <= abs(int(data_list[j+1][0]) - turning_frame[i]):
					data_list[j].append(1)
					i = i + 1
				else:
					data_list[j].append(0)
			j = j + 1
		
		if '.csv' in infile:
			infile = infile[0:infile.find('.csv')]

		with open(infile+'_out.csv','w',newline='') as csvout:
			writer = csv.writer(csvout)
			writer.writerows(data_list)
			print('Save output file as '+infile+'_out.csv')
	set_num = set_num + 1