from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np

'''
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
'''


def background_subtraction(video_name):


    backSub = cv.createBackgroundSubtractorKNN()
    capture = cv.VideoCapture(video_name)
    if not capture.isOpened:
        print('Unable to open: ' + video_name)
        exit(0)

    #frame_width = int(capture.get(3))
    #frame_height = int(capture.get(4))
    frame_width = 1280
    frame_height = 720

    out = cv.VideoWriter("./Background_subtraction/output.mp4", cv.VideoWriter_fourcc(*'mp4v'), 20.0, (1280,720)) # LOOK AT

    while True:

        ret, frame = capture.read()

        if frame is None:
            break
        
        fgMask = backSub.apply(frame)
        #out = np.zeros((720,1280,3),dtype=np.uint8)
        #out[0:720, 0:1280] = fgMask
        #fgMask = out
        fgMask = np.resize(fgMask, (720,1280,1))
        frame0 = frame[:,:,0:1]
        frame1 = frame[:,:,1:2]
        frame2 = frame[:,:,2:3]

        final = []
        final = np.array(final)

        #final = fgMask + frame
        frame0 = cv.bitwise_and(fgMask,frame0)
        frame1 = cv.bitwise_and(fgMask,frame1)
        frame2 = cv.bitwise_and(fgMask,frame2)
        frame0 = np.resize(frame0, (720,1280,1))
        frame1 = np.resize(frame1, (720,1280,1))
        frame2 = np.resize(frame2, (720,1280,1))
        
        frame[:,:,0:1] = frame0
        frame[:,:,1:2] = frame1
        frame[:,:,2:3] = frame2

        cv.imshow('FG Mask', frame)
        out.write(frame)    

        keyboard = cv.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break

    capture.release()
    out.release()
    cv.destroyAllWindows() 
