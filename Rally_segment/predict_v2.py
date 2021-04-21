import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import csv
import os

def find_vel(i,x_list,y_list):
	if i < 1 or i >= len(x_list):
		return 0
	if (x_list[i-1] == 0 and y_list[i-1] == 0) or (x_list[i] == 0 and y_list[i] == 0):
		return 0
	return (abs(x_list[i] - x_list[i-1])**2 + abs(y_list[i] - y_list[i-1])**2)**0.5

def average_vel(i,x_list,y_list):
	vel_sum = 0
	n = 0
	for m in range(i-2,i+3):
		vel = find_vel(m,x_list,y_list)
		if vel == 0:
			continue
		vel_sum += vel
		n += 1
	if n == 0:
		return 0
	return vel_sum/n

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
		if ax_temp == 0 and ay_temp == 0:
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

		x_denoise = []
		y_denoise = []
		z_denoise = []
		for i in range(len(y)):
			if x[i] != 0 or y[i] != 0:
				x_denoise.append(x[i])
				y_denoise.append(y[i])
				z_denoise.append(i)

		y_peaks,y_property = find_peaks(y_denoise,prominence=8,distance=5)
		y_peak = []
		z_peak = []
		for i in range(len(y_peaks)):
			y_peak.append(y_denoise[y_peaks[i]])
			z_peak.append(z_denoise[y_peaks[i]])


		avg_ax = []
		avg_ay = []
		avg_z = []
		for i in range(len(x)):
			avg_ax_temp,avg_ay_temp = average(i,x,y)
			avg_ax.append(avg_ax_temp)
			avg_ay.append(avg_ay_temp)
			avg_z.append(i)

		first_non_zero = 0
		for i in range(len(x)):
			if average_vel(i,x,y) != 0:
				first_non_zero = i
				break

		# peaks, properties = find_peaks(avg_ay, prominence=3, distance=8, height=3)
		peaks, properties = find_peaks(avg_ay, prominence=3, distance=8)
		peak_y = []
		peak_x = []
		for i in range(len(peaks)):
			if i == 0:
				# avg_ax_temp,avg_ay_temp = average(first_non_zero,x,y)
				# peak_y.append(avg_ay_temp)
				# peak_x.append(first_non_zero)
				# if abs(first_non_zero - peaks[i]) <= 15:
				# 	continue

				if abs(first_non_zero - peaks[i]) <= 15:
					continue

			if len(z_peak) >= 2 and peaks[i] > z_peak[-2] and properties['prominences'][i] < 5:
				continue
			elif len(z_peak) >= 1 and peaks[i] > z_peak[-1] and properties['prominences'][i] < 10:
				continue
			adjust = z_peak[np.abs(z_peak-peaks[i]).argmin()]
			if abs(adjust - peaks[i]) <= 5:
				avg_ax_temp,avg_ay_temp = average(adjust,x,y)
				peak_y.append(avg_ay_temp)
				peak_x.append(adjust)
			else:
				avg_ax_temp,avg_ay_temp = average(peaks[i] - 3,x,y)
				peak_y.append(avg_ay_temp)
				peak_x.append(peaks[i] - 3)

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