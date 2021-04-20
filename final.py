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
import tkinter as tk
import matplotlib.pyplot as plt

def run_main_program():
    #   rally segment
    interpolation_function("interpolation")
    rally_predict("rally_predict")
    os.system("rm *_interpolation.csv")

    #   ball type
    ball_predict("ball_predict")

    #   posture recognition
    video_file = tk.StringVar()
    video_file = entry_video_file.get()

    if len(video_file) <= 0:
        video_file = "./Background_subtraction/short1.mp4"
    background_subtraction(video_file)
    os.system('python3 pose.py --model=mobilenet_thin --video=./Background_subtraction/output.mp4 --write_video=./final_output.mp4')

    # show statistic result 
 
    x = np.arange(0, 5, 0.1)
    y = np.sin(x)
    plt.plot(x, y)
    plt.show()
    




def add_show_button():
    
    btn_login.destroy()
    label_video_file.destroy()
    entry_video_file.destroy()

    show_btn = Button(gui_frame,text='SHOW',font=("arial","12","bold"), height=3, width=15, command=add_image())
    show_btn.place(x=270,y=250)



import PIL.Image
import PIL.ImageTk

def add_image():
    print("SHOW")
    pass


from tkinter import *
from tkinter import messagebox


gui=Tk()
##gui.state("zoomed")
gui.geometry("1080x1080")
gui.title("Coach AI")
gui['bg']="black"
gui_frame=Frame(gui,width=700,height=700)
gui_frame.place(x=200,y=100)

#label=Label(gui_frame,text="USER INPUTS",font=("arial","20","bold"),bg="gray").place(x=270,y=10)
label_video_file=Label(gui_frame,text="VIDEO FILE:",font=("arial","15","bold"))
label_video_file.place(x=170,y=200)
#label_password=Label(gui_frame,text="Password:",font=("arial","12","bold")).place(x=100,y=300)

entry_video_file=Entry(gui_frame,font=("arial","15","bold"))
entry_video_file.place(x=300,y=200)


#entry_password=Entry(gui_frame,show="*",font=("arial","12","bold")).place(x=200,y=300)

btn_login=Button(gui_frame,text='Calculate',font=("arial","12","bold"), height=3, width=15, command=run_main_program)
btn_login.place(x=270,y=400)

gui.mainloop()
# 運行主程式
window.mainloop()



