import cv2
import csv
import os

set_num = 1

while set_num <= 3:
	score_A = 0
	score_B = 0
	while score_A < 22:
		ground_truth = []
		predict_result = []
		data_list = []
		total_row = 0
		if score_B == 21:
			score_A = score_A + 1
			score_B = 0
		else:
			score_B = score_B + 1
		rally_score = str(set_num)+"_"+(str(score_A)).zfill(2)+"_"+(str(score_B)).zfill(2)
		infile_out = rally_score + "_out.csv"
		infile_predict = rally_score + "_predict.csv"
		infile_video = rally_score + ".mp4"
		if os.path.isfile(infile_predict) == True and os.path.isfile(infile_video) == True:
			with open(infile_predict, newline='') as csv_predict:
				rows = csv.DictReader(csv_predict)
				for row in rows:
					if row['turning_point'] == "1":
						predict_result.append(int(row['index']))
			vc = cv2.VideoCapture(infile_video)
			c = 1
			path = './' + rally_score + '_predict_snapshot'
			if vc.isOpened():
				rval, frame = vc.read()
				if not os.path.exists(path):
					os.makedirs(path)
			else:
				rval = False
			while rval:
				if predict_result and c == predict_result[0]:
					cv2.imwrite('./' + rally_score + '_predict_snapshot/snapshot'+ str(c) + '.jpg',frame)
					predict_result.pop(0)
				c = c + 1
				rval, frame = vc.read()
			print("Finish taking snapshot of " + infile_predict)
		
		if os.path.isfile(infile_out) == True and os.path.isfile(infile_video) == True:
			with open(infile_out, newline='') as csv_out:
				rows = csv.DictReader(csv_out)
				for row in rows:
					if row['turning_point'] == "1":
						ground_truth.append(int(row['index']))
			vc = cv2.VideoCapture(infile_video)
			c = 1
			path = './' + rally_score + '_out_snapshot'
			if vc.isOpened():
				rval, frame = vc.read()
				if not os.path.exists(path):
					os.makedirs(path)
			else:
				rval = False
			while rval:
				if ground_truth and c == ground_truth[0]:
					cv2.imwrite('./' + rally_score + '_out_snapshot/snapshot'+ str(c) + '.jpg',frame)
					ground_truth.pop(0)
				c = c + 1
				rval, frame = vc.read()
			print("Finish taking snapshot of " + infile_out)
	set_num = set_num + 1