import csv
import numpy as np
import math
import cv2
import pandas as pd
import sklearn
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.model_selection import cross_val_predict
from joblib import dump, load
from PIL import Image, ImageDraw, ImageFont
import joblib
import os
import matplotlib.pyplot as plt
import copy

def ball_predict(dir_path):
    if dir_path[-1] != "/":
        dir_path += "/"
    set_num = 1
    while set_num <= 3:
        score_A = 0
        score_B = 0
        while score_A < 22:
            interpolate_table = []
            if score_B == 21:
                score_A = score_A + 1
                score_B = 0
            else:
                score_B = score_B + 1
            infile = dir_path + str(set_num)+"_"+(str(score_A)).zfill(2) + \
                "_"+(str(score_B)).zfill(2)+"_remove.csv"
            if os.path.isfile(infile) == False:
                continue

            address = ''

            def save_image(image, addr):

                address = addr + '.jpg'

                cv2.imwrite(address, image)

            videoCapture = cv2.VideoCapture(infile[:-11] + ".mp4")

            success, frame = videoCapture.read()

            save_image(frame, './court1')

            im_src = cv2.imread('court1.jpg')

            pts_src = np.array(
                [[449, 256], [817, 255], [283, 646], [977, 642]])

            im_dst = cv2.imread('court2.jpg')

            pts_dst = np.array(
                [[1238, 141], [1238, 640], [188, 141], [188, 640]])

            homo, status = cv2.findHomography(pts_src, pts_dst)

            data_list = []

            index_range = []

            ball_location_x = []

            ball_location_y = []

            ball_interpolate_x = []

            ball_interpolate_y = []

            frame = []

            first = 1

            player = []

            with open(infile, newline='') as csvfile:

                rows = csv.DictReader(csvfile)

                j, i = 0, 1

                first = 1

                shortest = 0

                lastx = 0

                lasty = 0

                lastindex = 0

                last_turning = 0

                data_list.append([])

                data_list[0].append('index')

                data_list[0].append('player')

                data_list[0].append('parabola')

                data_list[0].append('ymin')

                data_list[0].append('V')

                hit_odd = []

                hit_even = []

                oddeven = 1

                for row in rows:

                    if j == 0:

                        last_turning = 0

                        data_list.append([])

                        index = int(row['Frame'])

                        data_list[i].append(index)

                        visibility = int(row['Visibility'])

                        X = float(row['X'])

                        ball_location_x.append(X)

                        Y = float(row['Y'])

                        ball_location_y.append(Y)

                        if first:

                            frame.append(index)

                            # if ball_location_y[0] <= 300:

                            #     data_list[i].append('B')

                            #     player = 'B'

                            # else:

                            #     data_list[i].append('A')

                            #     player = 'A'

                            hit_odd.append(Y)

                            oddeven += 1

                            index_range.append(index)

                            hit_x = ball_location_x[0]

                            hit_y = ball_location_y[0]

                            first = 0

                        else:

                            index_range.append(lastindex)

                            hit_x = lastx

                            hit_y = lasty

                        hit_array = np.array([[hit_x], [hit_y], [1]])

                        hit_homo = np.dot(homo, hit_array)

                        hit_x1 = float(hit_homo[0])

                        hit_y1 = float(hit_homo[1])

                        turning = int(row['turning_point'])

                    else:

                        index = int(row['Frame'])

                        index_range.append(index)

                        visibility = int(row['Visibility'])

                        X = float(row['X'])

                        ball_location_x.append(X)

                        Y = float(row['Y'])

                        ball_location_y.append(Y)

                        turning = int(row['turning_point'])

                        if turning == 1:

                            last_turning = 1

                            frame.append(index)

                            index = index_range[-1] - index_range[0]

                            j = 0

                            total = len(ball_location_x)

                            lastx = ball_location_x[-1]

                            lasty = ball_location_y[-1]

                            lastindex = index_range[-1]

                            if oddeven % 2 == 0:

                                hit_even.append(Y)

                                oddeven += 1

                            else:

                                hit_odd.append(Y)

                                oddeven += 1

                            for l in range(total):

                                x = (l / (total-1)) * ball_location_x[total-1] + (
                                    (total-1-l)/(total-1)) * ball_location_x[0]

                                y = (l / (total-1)) * ball_location_y[total-1] + (
                                    (total-1-l)/(total-1)) * ball_location_y[0]

                                ball_interpolate_x.append(x)

                                ball_interpolate_y.append(y)

                            for k in range(total):

                                h = (ball_interpolate_x[k] - ball_location_x[k]) ** 2 + \
                                    (ball_interpolate_y[k] -
                                        ball_location_y[k]) ** 2

                                shortest = shortest + h

                            if (total-2) <= 0:

                                num = 1

                            else:

                                num = total - 2

                            shortest = shortest / num

                            data_list[i].append(round(shortest, 3))

                            data_list[i].append(min(ball_location_y))

                            landing_x = ball_location_x[-1]

                            landing_y = ball_location_y[-1]

                            landing_array = np.array(
                                [[landing_x], [landing_y], [1]])

                            landing_homo = np.dot(homo, landing_array)

                            landing_x1 = float(landing_homo[0])

                            landing_y1 = float(landing_homo[1])

                            a = landing_x1 - hit_x1

                            b = landing_y1 - hit_y1

                            v = round(math.sqrt(a * a + b * b) /
                                      (index * 0.03), 3)

                            data_list[i].append(v)

                            shortest = 0

                            index_range.clear()

                            ball_location_x.clear()

                            ball_interpolate_x.clear()

                            ball_location_y.clear()

                            ball_interpolate_y.clear()

                            i = i + 1

                    if turning == 0:

                        j = j + 1

                # if last_turning == 0:

                #     del data_list[-1]

                frame.append(index)

                index = index_range[-1] - index_range[0]

                j = 0

                total = len(ball_location_x)

                if total > 1:

                    lastx = ball_location_x[-1]

                    lasty = ball_location_y[-1]

                    lastindex = index_range[-1]

                    if oddeven % 2 == 0:

                        hit_even.append(Y)

                        oddeven += 1

                    else:

                        hit_odd.append(Y)

                        oddeven += 1

                    for l in range(total):

                        x = (l / (total-1)) * ball_location_x[total-1] + (
                            (total-1-l)/(total-1)) * ball_location_x[0]

                        y = (l / (total-1)) * ball_location_y[total-1] + (
                            (total-1-l)/(total-1)) * ball_location_y[0]

                        ball_interpolate_x.append(x)

                        ball_interpolate_y.append(y)

                    for k in range(total):

                        h = (ball_interpolate_x[k] - ball_location_x[k]) ** 2 + \
                            (ball_interpolate_y[k] -
                                ball_location_y[k]) ** 2

                        shortest = shortest + h

                    if (total-2) <= 0:

                        num = 1

                    else:

                        num = total - 2

                    shortest = shortest / num

                    data_list[i].append(round(shortest, 3))

                    data_list[i].append(min(ball_location_y))

                    landing_x = ball_location_x[-1]

                    landing_y = ball_location_y[-1]

                    landing_array = np.array(
                        [[landing_x], [landing_y], [1]])

                    landing_homo = np.dot(homo, landing_array)

                    landing_x1 = float(landing_homo[0])

                    landing_y1 = float(landing_homo[1])

                    a = landing_x1 - hit_x1

                    b = landing_y1 - hit_y1

                    v = round(math.sqrt(a * a + b * b) /
                              (index * 0.03), 3)

                    data_list[i].append(v)

                    shortest = 0

                    index_range.clear()

                    ball_location_x.clear()

                    ball_interpolate_x.clear()

                    ball_location_y.clear()

                    ball_interpolate_y.clear()

                else:

                    if last_turning == 0:

                        del data_list[-1]


                odd_point = round((sum(hit_odd) / len(hit_odd)), 2)

                even_point = round((sum(hit_even) / len(hit_even)), 2)

                # print(odd_point)

                # print(even_point)

                # if odd_point > even_point:

                #     c = 1

                #     for i in range(1, len(data_list)):

                #         if c % 2 == 1:

                #             data_list[i].insert(1, 'A')

                #             player.append('A')

                #         else:

                #             data_list[i].insert(1, 'B')

                #             player.append('B')

                #         c += 1

                # else:

                #     c = 1

                #     for i in range(1, len(data_list)):

                #         if c % 2 == 1:

                #             data_list[i].insert(1, 'B')

                #             player.append('B')

                #         else:

                #             data_list[i].insert(1, 'A')

                #             player.append('A')

                #         c += 1
                        
                # print(len(data_list))
                # print(hit_odd)
                # print(hit_even)

                for i in range(0, len(data_list)-3):

                    if odd_point > even_point:

                        data_list[i+1].insert(1, 'A')

                        player.append('A')

                    else:

                        data_list[i+1].insert(1, 'B')

                        player.append('B')

                    if i < len(data_list) - 3:

                        hit_odd.pop(0)

                        temp = copy.deepcopy(hit_even)

                        hit_even = copy.deepcopy(hit_odd)

                        hit_odd = copy.deepcopy(temp)

                        # print(len(hit_odd))
                        # print(len(hit_even))

                        odd_point = round((sum(hit_odd) / len(hit_odd)), 2)

                        even_point = round((sum(hit_even) / len(hit_even)), 2)

                c = len(data_list)-2

                if odd_point > even_point:

                    data_list[c].insert(1, 'A')

                    player.append('A')

                    data_list[c+1].insert(1, 'B')

                    player.append('B')

                else:

                    data_list[c].insert(1, 'B')

                    player.append('B')

                    data_list[c+1].insert(1, 'A')

                    player.append('A')




                # total = len(ball_location_x)

                # for l in range(total):

                #     x = (l / (total-1)) * ball_location_x[total-1] + \
                #         ((total-1-l)/(total-1)) * ball_location_x[0]

                #     y = (l / (total-1)) * ball_location_y[total-1] + \
                #         ((total-1-l)/(total-1)) * ball_location_y[0]

                #     ball_interpolate_x.append(x)

                #     ball_interpolate_y.append(y)

                # for k in range(total):

                #     h = (ball_interpolate_x[k] - ball_location_x[k]) ** 2 + \
                #         (ball_interpolate_y[k] - ball_location_y[k]) ** 2

                #     shortest = shortest + h

                # shortest = shortest / (total-2)

                # data_list[i].append(round(shortest, 3))

                # data_list[i].append(min(ball_location_y))

                # index = index_range[-1] - index_range[0]

                # landing_x = ball_location_x[-1]

                # landing_y = ball_location_y[-1]

                # landing_array = np.array([[landing_x], [landing_y], [1]])

                # landing_homo = np.dot(h, landing_array)

                # landing_x1 = float(landing_homo[0])

                # landing_y1 = float(landing_homo[1])

                # a = landing_x1 - hit_x1

                # b = landing_y1 - hit_y1

                # v = round(math.sqrt(a * a + b * b) / (index * 0.03), 3)

                # data_list[i].append(v)

            infile = infile[0:infile.find('_remove')]

            with open(infile + '_all.csv', 'w', newline='') as csvout:

                writer = csv.writer(csvout)

                writer.writerows(data_list)

                print('Save output file as ' + infile + '_all.csv')

            badminton_data = pd.read_csv(infile + '_all.csv')

            badminton_df = pd.DataFrame(data=badminton_data)

            badminton_df = badminton_df.drop(columns=['index'])

            badminton_df = pd.get_dummies(badminton_df)

            model = load("joblib_RL_Model.pkl")

            y_pred = model.predict(badminton_df)

            for i in range(len(y_pred)):

                if y_pred[i] == '高球':

                    y_pred[i] = 'clear'

                elif y_pred[i] == '小球':

                    y_pred[i] = 'short'

                elif y_pred[i] == '殺球':

                    y_pred[i] = 'smash'

                else:

                    y_pred[i] = 'drive'

            y_pred = list(y_pred)

            data_list = []

            data_list.append([])

            data_list[0].append('frame')

            data_list[0].append('player')

            data_list[0].append('type')

            for i in range(len(y_pred)):

                data_list.append([])

                data_list[i+1].append(frame[i])

                data_list[i+1].append(player[i])

                data_list[i+1].append(y_pred[i])

            with open(infile + '_out.csv', 'w') as csvout:

                writer = csv.writer(csvout)

                writer.writerows(data_list)

                print('Save output file as ' + infile + '_out.csv')

            hit_data = pd.read_csv(infile + '_out.csv')

            hit_A_data = hit_data.drop(hit_data[hit_data['player'] == "B"].index)

            fig = plt.figure()

            plt.title(infile + '_A')

            plt.bar(hit_A_data.type.unique(),
                    hit_A_data.type.value_counts(),
                    width=0.5,
                    bottom=None,
                    align='center',
                    color=['lightsteelblue',
                           'cornflowerblue',
                           'royalblue',
                           'midnightblue'])
            plt.xticks(rotation='vertical')

            fig.savefig(infile + '_A' + '.png')

            hit_B_data = hit_data.drop(hit_data[hit_data['player'] == "A"].index)

            fig = plt.figure()

            plt.title(infile + '_B')

            plt.bar(hit_B_data.type.unique(),
                    hit_B_data.type.value_counts(),
                    width=0.5,
                    bottom=None,
                    align='center',
                    color=['lightsteelblue',
                           'cornflowerblue',
                           'royalblue',
                           'midnightblue'])
            plt.xticks(rotation='vertical')

            fig.savefig(infile + '_B' + '.png')

        set_num = set_num + 1
