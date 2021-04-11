import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import csv
import os

def find_acc(i,x_list,y_list):
	if i < 2 or i >= len(x_list):
		return 0,0
	if (x_list[i-2] == 0 and y_list[i-2] == 0) or (x_list[i-1] == 0 and y_list[i-1] == 0) or (x_list[i] == 0 and y_list[i] == 0):
		return 0,0
	return x_list[i] - 2*x_list[i-1] + x_list[i-2],y_list[i] - 2*y_list[i-1] + y_list[i-2]

def average(i,x_list,y_list):
	ax_sum = 0
	ay_sum = 0
	n = 0
	for m in range(i-2,i+3):
		ax_temp,ay_temp = find_acc(m,x_list,y_list)
		if (m < 0 or m > len(x_list)-3) or (ax_temp == 0 and ay_temp == 0):
			continue
		ax_sum += abs(ax_temp)
		ay_sum += abs(ay_temp)
		n += 1
	if n == 0:
		return 0,0
	return ax_sum/n,ay_sum/n


set_num = 1
dir_path = input("Enter directory path:")
if dir_path[-1] != "/":
	dir_path += "/"

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
		infile = dir_path + rally_score + ".csv"
		denoise_file = dir_path + rally_score + "_denoise.csv"
		out_file = dir_path + rally_score + "_out.csv"
		predict_file = dir_path + rally_score + "_predict.csv"
		if os.path.isfile(infile) == False or os.path.isfile(denoise_file) == False:
			continue

		df = pd.read_csv(denoise_file)
		x = df['X'].tolist()
		y = df['Y'].tolist()


		avg_ax = []
		avg_ay = []
		avg_z = []
		for i in range(len(x)):
			avg_ax_temp,avg_ay_temp = average(i,x,y)
			avg_ax.append(avg_ax_temp)
			avg_ay.append(avg_ay_temp)
			avg_z.append(i)

		peaks, properties = find_peaks(avg_ay, prominence=3, distance=10, height=3)

		peak_y = []
		peak_x = []
		for peak in peaks:
			if peak == peaks[len(peaks)-1]:
				break
			avg_ax_temp,avg_ay_temp = average(peak,x,y)
			peak_y.append(avg_ay_temp)
			if peak >= 3:
				peak_x.append(peak - 3)
			else:
				peak_x.append(0)

		with open(infile, newline='') as csvfile:
			reader = csv.reader(csvfile)
			data = list(reader)

		for i in range(len(data)):
			if i == 0:
				data[i].append("turning_point")
				continue
			if int(data[i][0]) in peak_x:
				data[i].append(1)
			else:
				data[i].append(0)

		with open(predict_file, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(data)
			print('Save output file as '+rally_score+'_predict.csv')

	set_num += 1