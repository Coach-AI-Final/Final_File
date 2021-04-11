import csv
import pandas as pd
import random
import joblib
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix


def find_acc(i,x_list,y_list):
	if i < 2 or i >= len(x_list):
		return 0,0
	if (x_list[i-2] == 0 and y_list[i-2] == 0) or (x_list[i-1] == 0 and y_list[i-1] == 0) or (x_list[i] == 0 and y_list[i] == 0):
		return 0,0
	return x_list[i] - 2*x_list[i-1] + x_list[i-2],y_list[i] - 2*y_list[i-1] + y_list[i-2]

set_num = 1
dir_path = input("Enter directory path:")
if dir_path[-1] != "/":
	dir_path += "/"

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
		infile = dir_path + rally_score + "_out.csv"
		denoise_file = dir_path + rally_score + "_denoise.csv"
		x = []
		y = []
		turning = []
		non_turning = []
		if os.path.isfile(infile) == False:
			continue
		# with open(infile, newline='') as csvfile:
		# 	rows = csv.DictReader(csvfile)
		# 	j = 0
		# 	turn_num = 0
		j = 0
		turn_num = 0
		df = pd.read_csv(infile)
		p = df['turning_point'].tolist()
		df = pd.read_csv(denoise_file)
		in_x = df['X'].tolist()
		in_y = df['Y'].tolist()
		for i in range(len(in_x)):
			if i > 0:
				last_ax,last_ay = find_acc(i-1,in_x,in_y)
				ax,ay = find_acc(i,in_x,in_y)
				next_ax,next_ay = find_acc(i+1,in_x,in_y)
				if p[i] == 1:
					if (last_ax != 0 or last_ay != 0) and (ax != 0 or ay != 0):
						turning.append([])
						turning[-1].append(last_ax)
						turning[-1].append(last_ay)
						turning[-1].append(ax)
						turning[-1].append(ay)
						turning[-1].append(1)
						turn_num = turn_num + 1
					if (ax != 0 or ay != 0) and (next_ax != 0 or next_ay != 0):
						turning.append([])
						turning[-1].append(ax)
						turning[-1].append(ay)
						turning[-1].append(next_ax)
						turning[-1].append(next_ay)
						turning[-1].append(1)
						turn_num = turn_num + 1
				else :
					if (last_ax != 0 or last_ay != 0) and (ax != 0 or ay != 0):
						non_turning.append([])
						non_turning[-1].append(last_ax)
						non_turning[-1].append(last_ay)
						non_turning[-1].append(ax)
						non_turning[-1].append(ay)
						non_turning[-1].append(0)


		x_t=[]
		y_t=[]
				
		for row in turning:
			x_t.append([])
			y_t.append([])
			x_t[-1].append(row[0])
			x_t[-1].append(row[1])
			x_t[-1].append(row[2])
			x_t[-1].append(row[3])
			y_t[-1].append(row[4])
		for row in non_turning:
			x_t.append([])
			y_t.append([])
			x_t[-1].append(row[0])
			x_t[-1].append(row[1])
			x_t[-1].append(row[2])
			x_t[-1].append(row[3])
			y_t[-1].append(row[4])

		non_turning = random.sample(non_turning,turn_num)
		print(np.array(turning))
		print(np.array(non_turning))
		for row in turning:
			x.append([])
			y.append([])
			x[-1].append(row[0])
			x[-1].append(row[1])
			x[-1].append(row[2])
			x[-1].append(row[3])
			y[-1].append(row[4])
		for row in non_turning:
			x.append([])
			y.append([])
			x[-1].append(row[0])
			x[-1].append(row[1])
			x[-1].append(row[2])
			x[-1].append(row[3])
			y[-1].append(row[4])

		# lr = LogisticRegression()
		# lr = joblib.load('LR_model')

		Y=np.array(y)
		if Y.size != 0:
			# lr.fit(x,Y.ravel())
			# joblib.dump(lr, 'LR_model')
			print("Finish training with ",infile)
		else:
			print("Skip",infile)
	set_num = set_num + 1