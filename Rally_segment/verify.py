import csv
import os
import numpy as np

ERROR_RANGE = 10

confusion_matrix = np.array([[0,0],
                            [0,0]])
error_sum = 0
set_num = 1
total_row = 0
while set_num <= 3:
	score_A = 0
	score_B = 0
	while score_A < 22:
		ground_truth = []
		predict_result = []
		data_list = []
		if score_B == 21:
			score_A = score_A + 1
			score_B = 0
		else:
			score_B = score_B + 1
		rally_score = str(set_num)+"_"+(str(score_A)).zfill(2)+"_"+(str(score_B)).zfill(2)
		infile_out = rally_score + "_out.csv"
		infile_predict = rally_score + "_predict.csv"
		if os.path.isfile(infile_out) == False or os.path.isfile(infile_predict) == False:
			continue
		with open(infile_out, newline='') as csv_out:
			rows = csv.DictReader(csv_out)
			for row in rows:
				total_row = total_row + 1
				if row['turning_point'] == "1":
					ground_truth.append(int(row['Frame']))
		with open(infile_predict, newline='') as csv_predict:
			rows = csv.DictReader(csv_predict)
			for row in rows:
				if row['turning_point'] == "1":
					predict_result.append(int(row['Frame']))
		while ground_truth or predict_result:
			if ground_truth and predict_result:
				if ground_truth[0] < predict_result[0]:
					if abs(predict_result[0] - ground_truth[0]) > ERROR_RANGE:
						#ground truth is true but prediction is false
						confusion_matrix[1][0] = confusion_matrix[1][0] + 1
						ground_truth.pop(0)
					elif len(ground_truth) >= 2 and abs(predict_result[0] - ground_truth[0]) > abs(predict_result[0] - ground_truth[1]):
						#The next ground truth frame is closer from predicted frame than this one.
						confusion_matrix[1][0] = confusion_matrix[1][0] + 1
						ground_truth.pop(0)
					else:
						confusion_matrix[1][1] = confusion_matrix[1][1] + 1
						error_sum += abs(ground_truth[0] - predict_result[0])
						ground_truth.pop(0)
						predict_result.pop(0)
				else:
					if abs(predict_result[0] - ground_truth[0]) > ERROR_RANGE:
						#ground truth is false but prediction is true
						confusion_matrix[0][1] = confusion_matrix[0][1] + 1
						predict_result.pop(0)
					elif len(predict_result) >= 2 and abs(predict_result[0] - ground_truth[0]) > abs(predict_result[1] - ground_truth[0]):
						#The next predicted frame is closer from ground truth frame than this one.
						confusion_matrix[0][1] = confusion_matrix[0][1] + 1
						predict_result.pop(0)
					else:
						confusion_matrix[1][1] = confusion_matrix[1][1] + 1
						error_sum += abs(ground_truth[0] - predict_result[0])
						ground_truth.pop(0)
						predict_result.pop(0)
			elif ground_truth:
				confusion_matrix[1][0] = confusion_matrix[1][0] + 1
				ground_truth.pop(0)
			elif predict_result:
				confusion_matrix[0][1] = confusion_matrix[0][1] + 1
				predict_result.pop(0)
		#avg_error = error_sum / float(confusion_matrix[1][1])
		print("Finish verifying " + rally_score)
		#print("avg error:",avg_error)
	set_num = set_num + 1

confusion_matrix[0][0] = total_row - confusion_matrix[1][0] - confusion_matrix[0][1] - confusion_matrix[1][1]
accuracy = (confusion_matrix[0][0] + confusion_matrix[1][1]) / total_row
precision = confusion_matrix[1][1] / (confusion_matrix[0][1] + confusion_matrix[1][1])
recall = confusion_matrix[1][1] / (confusion_matrix[1][0] + confusion_matrix[1][1])
print(confusion_matrix)
print("accuracy:",round(accuracy,3))
print("precision:",round(precision,3))
print("recall",round(recall,3))