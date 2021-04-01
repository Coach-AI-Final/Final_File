import argparse
import logging
import time

import cv2
import numpy as np
import csv
import math
import sys, time
import matplotlib.pyplot as plt

from progressbar import *
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from bisect import bisect_left

logger = logging.getLogger('TfPoseEstimator-Video')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

global front_frame_1_x, front_frame_1_y, front_frame_2_x, front_frame_2_y, now_frame_x, now_frame_y
front_frame_1_x=[]
front_frame_2_x=[]
front_frame_1_y=[]
front_frame_2_y=[]
now_frame_x=[]
now_frame_y=[]


def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.
    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before



def closest(lst, K):  
    if K > lst[-1] or K < lst[0]:
        return None

    for i in range(len(lst)):
        if K < lst[i]:
            return lst[i-1]
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--write_video', type=str, default='')
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution.default=432x368')
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('--showBG', type=str, default='', help='Use it with any non-empty string to show skeleton only.')
    args = parser.parse_args()

    #logger.debug('initialization %s : %s' %(args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resolution)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    logger.debug('video read+')
    cap = cv2.VideoCapture(args.video)
    cap2 = cv2.VideoCapture('./Background_subtraction/short1.mp4')

    # total frame of a video
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #print( "total frame of",args.video, length )

    #---------------------------------
    #frame_width = int(cap.get(3))
    #frame_height = int(cap.get(4))
    frame_width = 675
    frame_height = 550
    #---------------------------------

    if args.write_video:
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #---------------------------------
        out = cv2.VideoWriter(args.write_video, fourcc, 20.0, (frame_width,frame_height)) # LOOK AT THIS
    #---------------------------------

    #ret_val, image = cap.read()
    #logger.info('cap image=%dx%d' % (image.shape[1], image.shape[0]))

    if cap.isOpened() is False:
        print("Error opening video stream or file")

    backSub = cv2.createBackgroundSubtractorMOG2()
    
    #record frame number
    frame_num = 0

    # add rally frame into a list
    with open('./Ball_predict/1_00_01_out.csv', newline='') as csvfile:
        dict = {}
        rows = csv.reader(csvfile)
        record = []
        frame_list = []
        for row in rows:
            dict[int(row[0])] = str(row[1])
            frame_list.append(int(row[0]))
            

    # progress bar
    print("\n\n")
    pbar = ProgressBar().start()
    

    while cap.isOpened():
        
        frame_num += 1
        
        #print("now frame : ",frame_num, "total frame : ",length," ")
        
        pbar.update(int((frame_num / length) * 100))

        ret_val, image = cap.read()
        ret_val2, image2 = cap2.read()
        
        
        if(image is None):
            break
        
        image = image[140:140+frame_height, 300:300+frame_width]
        image2 = image2[140:140+frame_height, 300:300+frame_width]

        humans = e.inference(image, resize_to_default=True, upsample_size=4.0)
        
        if frame_num in dict.keys():
            image = np.zeros(image.shape, dtype=np.uint8)
            image = TfPoseEstimator.draw_humans(image, image2, humans, frame_num, imgcopy=False, skeletonornot=True)

        else:
            image = np.zeros(image.shape, dtype=np.uint8) 
            image = TfPoseEstimator.draw_humans(image, image2, humans, frame_num, imgcopy=False, skeletonornot=True)
        
        #cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)),
        #            (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        #cv2.putText(image, "Frame number: %f" % (frame_num),
        #            (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        if frame_num in dict.keys():

            cv2.putText(image, "Ball: %s" % (str(dict[frame_num])),
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else : 
            if closest(frame_list,frame_num) is None:
                pass
            else:
                cv2.putText(image, "Ball: %s" % (str(dict[closest(frame_list,frame_num)])),
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)            

        if args.write_video:
            closest_value = abs (frame_num - take_closest(frame_list,frame_num))
            #print(closest_value)
            if closest_value <=3 :
                #print("add")
                for i in range(5):
                    out.write(image)
            else:
                out.write(image)
            cv2.imshow('tf-pose-estimation result', image)

        else:
            cv2.imshow('tf-pose-estimation result', image)
            print(",,,")

        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        

    cap.release()
    out.release()
    cv2.destroyAllWindows()

#logger.debug( "total frame of",length)
logger.debug('finished+')
