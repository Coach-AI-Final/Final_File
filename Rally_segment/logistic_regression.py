import csv
import pandas as pd
import random
import joblib
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix


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
		infile = rally_score + "_out.csv"
		x = []
		y = []
		turning = []
		non_turning = []
		if os.path.isfile(infile) == False:
			continue
		with open(infile, newline='') as csvfile:
			rows = csv.DictReader(csvfile)
			j = 0
			turn_num = 0

			for row in rows:
				if j==0:
					j = j + 1
					continue
				elif j==1:
					temp = row['turning_point']
					last_ax = float(row['ax'])
					last_ay = float(row['ay'])
				elif j>=2:
					if int(temp)==1:
						turning.append([])
						turning[-1].append(last_ax)
						turning[-1].append(last_ay)
						turning[-1].append(float(row['ax']))
						turning[-1].append(float(row['ay']))
						turning[-1].append(int(temp))
						turn_num = turn_num + 1
					else :
						non_turning.append([])
						non_turning[-1].append(last_ax)
						non_turning[-1].append(last_ay)
						non_turning[-1].append(float(row['ax']))
						non_turning[-1].append(float(row['ay']))
						non_turning[-1].append(int(temp))
					last_ax = float(row['ax'])
					last_ay = float(row['ay'])
					temp = row['turning_point']
				j = j + 1

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

		#x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
		lr = LogisticRegression()
		#lr = joblib.load('LR_model')

		Y=np.array(y)
		if Y.size != 0:
			lr.fit(x,Y.ravel())

			#print("coefficient: ",lr.coef_)
			#print("intercept ",lr.intercept_)

			#cnf = confusion_matrix(y_t,lr.predict(x_t))
			#print("confusion matrix: \n",cnf)
			joblib.dump(lr, 'LR_model')
			print("Finish training with ",infile)
		else:
			print("Skip",infile)
	set_num = set_num + 1