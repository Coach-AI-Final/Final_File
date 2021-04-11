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

def average_acc(i,x_list,y_list):
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
		denoise_file = dir_path + rally_score + "_denoise.csv"
		out_file = dir_path + rally_score + "_out.csv"
		predict_file = dir_path + rally_score + "_predict.csv"
		plot_file = dir_path + rally_score + "_plot.jpg"
		if os.path.isfile(denoise_file) == False or os.path.isfile(out_file) == False or os.path.isfile(predict_file) == False:
			continue

		df = pd.read_csv(out_file)
		x = df['X'].tolist()
		y = df['Y'].tolist()
		p = df['turning_point'].tolist()
		vis = df['Visibility'].tolist()
		x_out_line = []
		y_out_line = []
		z_out_line = []
		for i in range(len(y)):
			if x[i] != 0 or y[i] != 0:
				x_out_line.append(x[i])
				y_out_line.append(y[i])
				z_out_line.append(i)

		result_x = []
		result_y = []
		result_z = []
		for i in range(len(p)):
			if p[i] == 1:
				result_x.append(x[i])
				result_y.append(y[i])
				result_z.append(i)

		df = pd.read_csv(predict_file)
		x = df['X'].tolist()
		y = df['Y'].tolist()
		p = df['turning_point'].tolist()
		predict_x = []
		predict_y = []
		predict_z = []
		for i in range(len(p)):
			if p[i] == 1:
				predict_x.append(x[i])
				predict_y.append(y[i])
				predict_z.append(i)

		df = pd.read_csv(denoise_file)
		x = df['X'].tolist()
		y = df['Y'].tolist()

		avg_vel = []
		for i in range(len(y)):
			avg_vel.append(find_vel(i,x,y))

		x_denoise_line = []
		y_denoise_line = []
		z_denoise_line = []
		for i in range(len(y)):
			if x[i] != 0 or y[i] != 0:
				x_denoise_line.append(x[i])
				y_denoise_line.append(y[i])
				z_denoise_line.append(i)

		y_peaks,y_property = find_peaks(y_denoise_line,prominence=8,distance=5)
		y_peak = []
		z_peak = []
		for i in range(len(y_peaks)):
			y_peak.append(y_denoise_line[y_peaks[i]])
			z_peak.append(z_denoise_line[y_peaks[i]])

		ax = []
		ay = []
		z = []
		for i in range(len(x)):
			ax_temp,ay_temp = find_acc(i,x,y)
			if ax_temp != 0 or ay_temp != 0:
				ax.append(ax_temp)
				ay.append(ay_temp)
				z.append(i)

		df = pd.read_csv(out_file)
		p = df['turning_point'].tolist()
		result_ax = []
		result_ay = []
		result_az = []
		for i in range(len(p)):
			if p[i] == 1:
				ax_temp,ay_temp = find_acc(i,x,y)
				result_ax.append(ax_temp)
				result_ay.append(ay_temp)
				result_az.append(i)

		df = pd.read_csv(predict_file)
		p = df['turning_point'].tolist()
		predict_ax = []
		predict_ay = []
		predict_az = []
		for i in range(len(p)):
			if p[i] == 1:
				ax_temp,ay_temp = find_acc(i,x,y)
				predict_ax.append(ax_temp)
				predict_ay.append(ay_temp)
				predict_az.append(i)

		avg_ax = []
		avg_ay = []
		avg_z = []
		for i in range(len(x)):
			avg_ax_temp,avg_ay_temp = average_acc(i,x,y)
			avg_ax.append(avg_ax_temp)
			avg_ay.append(avg_ay_temp)
			avg_z.append(i)

		peaks, properties = find_peaks(avg_ay, prominence=3, distance=10, height=3)
		# print(peaks)
		# print(properties)

		df = pd.read_csv(out_file)
		p = df['turning_point'].tolist()
		result_avg_ax = []
		result_avg_ay = []
		result_avg_z = []
		for i in range(len(p)):
			if p[i] == 1:
				avg_ax_temp,avg_ay_temp = average_acc(i,x,y)
				result_avg_ax.append(avg_ax_temp)
				result_avg_ay.append(avg_ay_temp)
				result_avg_z.append(i)

		df = pd.read_csv(predict_file)
		p = df['turning_point'].tolist()
		predict_avg_ax = []
		predict_avg_ay = []
		predict_avg_z = []
		for i in range(len(p)):
			if p[i] == 1:
				avg_ax_temp,avg_ay_temp = average_acc(i,x,y)
				predict_avg_ax.append(avg_ax_temp)
				predict_avg_ay.append(avg_ay_temp)
				predict_avg_z.append(i)

		fig = plt.figure(figsize=(12,8))
		# plt.subplot(2,2,1)
		# plt.plot(z,ay,'-')
		# plt.plot(result_az,result_ay,'ro')
		# plt.plot(predict_az,predict_ay,'bs')
		# plt.title("aY versus Frame")

		# plt.subplot(2,2,2)
		# plt.plot(z,ax,'-')
		# plt.plot(result_az,result_ax,'ro')
		# plt.plot(predict_az,predict_ax,'bs')
		# plt.title("aX versus Frame")

		plt.subplot(2,2,3)
		plt.plot(avg_z,avg_ay,'-')
		plt.plot(result_avg_z,result_avg_ay,'ro')
		plt.plot(predict_avg_z,predict_avg_ay,'bs')
		plt.title("Avg_aY versus Frame")

		plt.subplot(2,2,4)
		plt.plot(avg_z,avg_ax,'-')
		plt.plot(result_avg_z,result_avg_ax,'ro')
		plt.plot(predict_avg_z,predict_avg_ax,'bs')
		plt.title("Avg_aX versus Frame")


		# plt.subplot(2,2,1)
		# plt.plot(z_out_line,y_out_line,'-')
		# plt.plot(result_z,result_y,'ro')
		# plt.plot(predict_z,predict_y,'bs')
		# plt.title("Y versus Frame with tracknet")

		# plt.subplot(2,2,2)
		# plt.plot(z_out_line,x_out_line,'-')
		# plt.plot(result_z,result_x,'ro')
		# plt.plot(predict_z,predict_x,'bs')
		# plt.title("X versus Frame with tracknet")

		plt.subplot(2,2,1)
		plt.plot(z_denoise_line,y_denoise_line,'-')
		plt.plot(np.arange(len(avg_vel)),avg_vel,'--')
		plt.plot(result_z,result_y,'ro')
		plt.plot(predict_z,predict_y,'bs')
		plt.plot(z_peak,y_peak,'g^')
		for i in result_z:
			plt.axvline(x=i, ymin=0, ymax=1, color='bisque', linestyle='--')
		plt.title("Y versus Frame with denoise")

		plt.subplot(2,2,2)
		plt.plot(z_denoise_line,x_denoise_line,'-')
		plt.plot(result_z,result_x,'ro')
		plt.plot(predict_z,predict_x,'bs')
		for i in result_z:
			plt.axvline(x=i, ymin=0, ymax=1, color='bisque', linestyle='--')
		plt.title("X versus Frame with denoise")

		plt.savefig(plot_file)
		plt.close(fig)
		print("Save image as " + rally_score + "_plot.jpg")
	set_num += 1