import joblib
import csv
import os


def rally_predict(*args):

	set_num = 1

	while set_num <= 2:
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
			if os.path.isfile(infile) == False:
				continue
			#loads the file and calculate velocity
			with open(infile, newline='') as csvfile:
				rows = csv.DictReader(csvfile)
				j = 0

				for row in rows:
					data_list.append([])
					if j == 0:
						data_list[j].append('index')
						data_list[j].append('X')
						data_list[j].append('Y')
						data_list[j].append('Vx')
						data_list[j].append('Vy')
						index = int(row['index'])
						x = int(row['x'])
						y = int(row['y'])
						data_list.append([])
						data_list[j+1].append(int(row['index']))
						data_list[j+1].append(int(row['x']))
						data_list[j+1].append(int(row['y']))
						data_list[j+1].append(0)#first index has no velocity value, set to 0
						data_list[j+1].append(0)#first index has no velocity value, set to 0
						j = j + 2
					else:
						data_list[j].append(int(row['index']))
						data_list[j].append(int(row['x']))
						data_list[j].append(int(row['y']))
						data_list[j].append(round((int(row['x'])-x)/((int(row['index'])-index)),3))
						data_list[j].append(round((int(row['y'])-y)/((int(row['index'])-index)),3))
						index = int(row['index'])
						x = int(row['x'])
						y = int(row['y'])
						j = j + 1

			#calculate acceleration
			if '.csv' in infile:
				infile = infile[0:infile.find('.csv')]
			with open(infile+"_interpolation.csv", newline='') as csvfile:
				interpolate_table = list(csv.reader(csvfile))
			j = 0
			for row in data_list:
				if j == 0:
					data_list[j].append('ax')
					data_list[j].append('ay')
					data_list[j].append('turning_point')
				elif j <= 2:
					index = int(row[0])
					Vx = float(row[3])
					Vy = float(row[4])
					data_list[j].append(0)#first two index has no acceleration value, set to 0
					data_list[j].append(0)#first two index has no acceleration value, set to 0
				else:
					ax = round((float(row[3])-Vx)/((int(row[0])-index)),3)
					ay = round((float(row[4])-Vy)/((int(row[0])-index)),3)
					if abs(ax)>=120 or abs(ay)>=120: #if absolute acceleration is larger than or equal to 120, take the interpolation value. 
						data_list[j][1] = int(interpolate_table[j][1])
						data_list[j][2] = int(interpolate_table[j][2])
						data_list[j][3] = (data_list[j][1] - data_list[j-1][1]) / (data_list[j][0] - data_list[j-1][0])
						data_list[j][4] = (data_list[j][2] - data_list[j-1][2]) / (data_list[j][0] - data_list[j-1][0])
						if j < len(data_list) - 1: #Update of position of index j will affect the velocity of index j+1
							data_list[j+1][3] = (data_list[j+1][1] - data_list[j][1]) / (data_list[j+1][0] - data_list[j][0])
							data_list[j+1][4] = (data_list[j+1][2] - data_list[j][2]) / (data_list[j+1][0] - data_list[j][0])
					data_list[j].append(round((float(data_list[j][3])-Vx)/((int(row[0])-index)),3))
					data_list[j].append(round((float(data_list[j][4])-Vy)/((int(row[0])-index)),3))
					index = int(row[0])
					Vx = float(data_list[j][3])
					Vy = float(data_list[j][4])
				j = j + 1
				
			j = 0
			X = []
			for row in data_list:
				if j==1:
					last_ax = float(row[5])
					last_ay = float(row[6])
				elif j>=2:
					X.append([])
					X[-1].append(last_ax)
					X[-1].append(last_ay)
					X[-1].append(float(row[5]))
					X[-1].append(float(row[6]))
					last_ax = float(row[5])
					last_ay = float(row[6])
				j = j + 1
				
			lr = joblib.load('./Rally_segment/LR_model')
			Y = lr.predict(X)
			Y_out = []

			j = 0
			for row in range(len(data_list)):
				if j==1:
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
					grade[j].append(int(data_list[j][7])*5+int(data_list[j+1][7])*4+int(data_list[j+2][7])*2)
				elif j==2:
					grade[j].append(int(data_list[j][7])*5+int(data_list[j-1][7])*4+int(data_list[j+1][7])*4+int(data_list[j+2][7])*2)
				elif j==len(data_list)-1:
					grade[j].append(int(data_list[j][7])*5+int(data_list[j-1][7])*4+int(data_list[j-2][7])*2)
				elif j==len(data_list)-2:
					grade[j].append(int(data_list[j][7])*5+int(data_list[j+1][7])*4+int(data_list[j-1][7])*4+int(data_list[j-2][7])*2)
				else:
					grade[j].append(int(data_list[j][7])*5+int(data_list[j+2][7])*2+int(data_list[j+1][7])*4+int(data_list[j-1][7])*4+int(data_list[j-2][7])*2)
				j = j + 1

			j = 0	
			for row in range(len(grade)):
				if j==0:
					j = j + 1
					continue
				if j==1:
					if grade[j][0]!=0 and grade[j][0]>=max(grade[j+1][0],grade[j+2][0]):
						data_list[j][7] = 1
					else:
						data_list[j][7] = 0
				elif j==2:
					if grade[j][0]!=0 and grade[j][0]>=max(grade[j+1][0],grade[j+2][0]) and grade[j][0]>grade[j-1][0]:
						data_list[j][7] = 1
					else:
						data_list[j][7] = 0
				elif j==len(grade)-1:
					if(grade[j][0]!=0 and grade[j][0]>max(grade[j-1][0],grade[j-2][0])):
						data_list[j][7] = 1
					else:
						data_list[j][7] = 0
				elif j==len(grade)-2:
					if grade[j][0]!=0 and grade[j][0]>max(grade[j-1][0],grade[j-2][0]) and grade[j][0]>=grade[j+1][0]:
						data_list[j][7] = 1
					else:
						data_list[j][7] = 0
				else:
					if grade[j][0]!=0 and grade[j][0]>max(grade[j-1][0],grade[j-2][0]) and grade[j][0]>=max(grade[j+1][0],grade[j+2][0]):
						data_list[j][7] = 1
					else:
						data_list[j][7] = 0
				j = j + 1

			j = 0

			for row in Y:
				Y[j] = data_list[j+2][7]
				j = j + 1
				

			"""
			if '.csv' in infile:
				infile = infile[0:infile.find('.csv')]
			j = 0
			with open(infile+'_out.csv',newline = '') as out:
				rows = csv.DictReader(out)
				for row in rows:
					if j>0:
						Y_out.append(int(row['turning_point']))
					j = j + 1

			#print(Y_out)
			#print(Y)
			cnf = confusion_matrix(Y_out,Y)
			print("confusion matrix: \n",cnf)
			print("accuracy:",accuracy_score(Y_out,Y))
			print("recall:",recall_score(Y_out,Y,average = 'binary'))
			print("precision:",precision_score(Y_out,Y,average = 'binary'))

			"""

			with open(infile+'_predict.csv','w',newline='') as predict:
				writer = csv.writer(predict)
				writer.writerows(data_list)
				print('Save output file as '+infile+'_predict.csv')
		
		set_num = set_num + 1
				
