import joblib
import csv
import os

set_num = 1

while set_num <= 3:
	score_A = 0
	score_B = 0
	while score_A < 22:
		data_list = []
		if score_B == 21:
			score_A = score_A + 1
			score_B = 0
		else:
			score_B = score_B + 1
		rally_score = str(set_num)+"_"+(str(score_A)).zfill(2)+"_"+(str(score_B)).zfill(2)
		infile = rally_score + ".csv"
		denoise_file = rally_score + "_denoise.csv"
		if os.path.isfile(infile) == False or os.path.isfile(denoise_file) == False:
			continue
		#loads the file and calculate velocity
		with open(infile, newline='') as csvfile:
			rows = csv.DictReader(csvfile)
			first = True
			data_list.append([])
			data_list[-1].append('Frame')
			data_list[-1].append('Visibility')
			data_list[-1].append('X')
			data_list[-1].append('Y')
			data_list[-1].append('Vx')
			data_list[-1].append('Vy')
			for row in rows:
				data_list.append([])
				if first:
					if int(row['X']) != 0 or int(row['Y']) != 0:
						Frame = int(row['Frame'])
						x = int(row['X'])
						y = int(row['Y'])
						first = False
					data_list[-1].append(int(row['Frame']))
					data_list[-1].append(int(row['Visibility']))
					data_list[-1].append(int(row['X']))
					data_list[-1].append(int(row['Y']))
					data_list[-1].append(0)#Has no velocity value, set to 0
					data_list[-1].append(0)#Has no velocity value, set to 0
				else:
					data_list[-1].append(int(row['Frame']))
					data_list[-1].append(int(row['Visibility']))
					data_list[-1].append(int(row['X']))
					data_list[-1].append(int(row['Y']))
					if int(row['X']) == 0 and int(row['Y']) == 0:
						data_list[-1].append(0)
						data_list[-1].append(0)
					else:
						data_list[-1].append(round((int(row['X'])-x)/((int(row['Frame'])-Frame)),3))
						data_list[-1].append(round((int(row['Y'])-y)/((int(row['Frame'])-Frame)),3))
						Frame = int(row['Frame'])
						x = int(row['X'])
						y = int(row['Y'])

		#calculate acceleration
		if '.csv' in infile:
			infile = infile[0:infile.find('.csv')]
		with open(denoise_file, newline='') as csvfile:
			denoise_table = list(csv.reader(csvfile))
		i = 0
		j = 0
		for row in data_list:
			if i == 0:
				data_list[j].append('ax')
				data_list[j].append('ay')
				data_list[j].append('turning_point')
				i = i + 1
			elif i <= 2:
				if data_list[j][1] == 1:
					i = i + 1
				Frame = int(row[0])
				Vx = float(row[4])
				Vy = float(row[5])
				data_list[j].append(0)#first two Frame has no acceleration value, set to 0
				data_list[j].append(0)#first two Frame has no acceleration value, set to 0
			else:
				if data_list[j][1] == 1:
					ax = round((float(row[4])-Vx)/((int(row[0])-Frame)),3)
					ay = round((float(row[5])-Vy)/((int(row[0])-Frame)),3)
				else :
					ax = 0
					ay = 0
				if abs(ax)>=120 or abs(ay)>=120: #if absolute acceleration is larger than or equal to 120, take the interpolation value. 
					data_list[j][2] = float(denoise_table[j][2])
					data_list[j][3] = float(denoise_table[j][3])
					data_list[j][4] = (data_list[j][2] - data_list[j-1][2]) / (data_list[j][0] - data_list[j-1][0])
					data_list[j][5] = (data_list[j][3] - data_list[j-1][3]) / (data_list[j][0] - data_list[j-1][0])
					if j < len(data_list) - 1: #Update of position of Frame j will affect the velocity of Frame j+1
						data_list[j+1][4] = (data_list[j+1][2] - data_list[j][2]) / (data_list[j+1][0] - data_list[j][0])
						data_list[j+1][5] = (data_list[j+1][3] - data_list[j][3]) / (data_list[j+1][0] - data_list[j][0])
				if data_list[j][1] == 1:
					data_list[j].append(round((float(data_list[j][4])-Vx)/((int(row[0])-Frame)),3))
					data_list[j].append(round((float(data_list[j][5])-Vy)/((int(row[0])-Frame)),3))
					Frame = int(row[0])
					Vx = float(data_list[j][4])
					Vy = float(data_list[j][5])
				else :
					data_list[j].append(0)
					data_list[j].append(0)
			j = j + 1
			
		j = 0
		X = []
		for row in data_list:
			if j==1:
				last_ax = float(row[6])
				last_ay = float(row[7])
			elif j>=2:
				X.append([])
				X[-1].append(last_ax)
				X[-1].append(last_ay)
				X[-1].append(float(row[6]))
				X[-1].append(float(row[7]))
				last_ax = float(row[6])
				last_ay = float(row[7])
			j = j + 1
			
		lr = joblib.load('LR_model')
		Y = lr.predict(X)
		Y_out = []

		j = 0
		for row in range(len(data_list)):
			if j==1 or data_list[j][1] == 0:
				data_list[j].append(0)
			elif j>1:
				data_list[j].append(Y[j-2])	
			j = j + 1



		grade = []
		j = 0
		for row in range(len(data_list)):
			grade.append([])
			if j==0:
				grade[j].append('modified')
			elif j==1:
				grade[j].append(int(data_list[j][8])*5+int(data_list[j+1][8])*4+int(data_list[j+2][8])*2)
			elif j==2:
				grade[j].append(int(data_list[j][8])*5+int(data_list[j-1][8])*4+int(data_list[j+1][8])*4+int(data_list[j+2][8])*2)
			elif j==len(data_list)-1:
				grade[j].append(int(data_list[j][8])*5+int(data_list[j-1][8])*4+int(data_list[j-2][8])*2)
			elif j==len(data_list)-2:
				grade[j].append(int(data_list[j][8])*5+int(data_list[j+1][8])*4+int(data_list[j-1][8])*4+int(data_list[j-2][8])*2)
			else:
				grade[j].append(int(data_list[j][8])*5+int(data_list[j+2][8])*2+int(data_list[j+1][8])*4+int(data_list[j-1][8])*4+int(data_list[j-2][8])*2)
			j = j + 1

		j = 0	
		for row in range(len(grade)):
			if j==0:
				j = j + 1
				continue
			if j==1:
				if grade[j][0]!=0 and grade[j][0]>=max(grade[j+1][0],grade[j+2][0]):
					data_list[j][8] = 1
				else:
					data_list[j][8] = 0
			elif j==2:
				if grade[j][0]!=0 and grade[j][0]>=max(grade[j+1][0],grade[j+2][0]) and grade[j][0]>grade[j-1][0]:
					data_list[j][8] = 1
				else:
					data_list[j][8] = 0
			elif j==len(grade)-1:
				if(grade[j][0]!=0 and grade[j][0]>max(grade[j-1][0],grade[j-2][0])):
					data_list[j][8] = 1
				else:
					data_list[j][8] = 0
			elif j==len(grade)-2:
				if grade[j][0]!=0 and grade[j][0]>max(grade[j-1][0],grade[j-2][0]) and grade[j][0]>=grade[j+1][0]:
					data_list[j][8] = 1
				else:
					data_list[j][8] = 0
			else:
				if grade[j][0]!=0 and grade[j][0]>max(grade[j-1][0],grade[j-2][0]) and grade[j][0]>=max(grade[j+1][0],grade[j+2][0]):
					data_list[j][8] = 1
				else:
					data_list[j][8] = 0
			j = j + 1

		j = 0

		for row in Y:
			Y[j] = data_list[j+2][8]
			j = j + 1

		out_data = []
		for i in range(len(data_list)):
			out_data.append([])
			out_data[-1].append(data_list[i][0])
			out_data[-1].append(data_list[i][1])
			out_data[-1].append(data_list[i][2])
			out_data[-1].append(data_list[i][3])
			out_data[-1].append(data_list[i][8])

		with open(infile+'_predict.csv','w',newline='') as predict:
			writer = csv.writer(predict)
			writer.writerows(out_data)
			print('Save output file as '+infile+'_predict.csv')
	
	set_num = set_num + 1
			
