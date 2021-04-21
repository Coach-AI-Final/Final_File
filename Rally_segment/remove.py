import csv
import os

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
		predict_file = dir_path + rally_score + "_predict.csv"
		remove_file = dir_path + rally_score + "_remove.csv"
		if os.path.isfile(predict_file) == False:
			continue

		with open(predict_file, newline='') as csvfile:
			reader = csv.reader(csvfile)
			data = list(reader)

		remove = []
		for i in range(len(data)):
			if i == 0:
				remove.append(data[i])
				continue
			if int(data[i][2]) == 0 and int(data[i][3]) == 0:
				continue
			else:
				remove.append(data[i])

		with open(remove_file, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(remove)
			print('Save output file as '+rally_score+'_remove.csv')

	set_num += 1