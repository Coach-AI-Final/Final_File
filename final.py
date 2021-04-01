import argparse
import logging
import time
import cv2
import numpy as np
import csv
import math
import time
import os 
import sys
from Background_subtraction.background import background_subtraction
from Rally_segment.interpolation import interpolation_function
from Rally_segment.predict import rally_predict
from Ball_predict.ball_predict import ball_predict

#   rally segment
interpolation_function("interpolation")
rally_predict("rally_predict")
os.system("rm *_interpolation.csv")

#   ball type
ball_predict("ball_predict")

#   posture recognition
background_subtraction("./Background_subtraction/short1.mp4")
os.system('python3 pose.py --model=mobilenet_thin --video=./Background_subtraction/output.mp4 --write_video=./final_output.mp4')

