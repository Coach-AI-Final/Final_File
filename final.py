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
from Rally_segment.denoise import interpolation_fun
from Rally_segment.predict_v2 import rally_predict
from Rally_segment.plot import plot
from Ball_predict.ball_predict import ball_predict
from Ball_predict.remove import remove
import tkinter as tk
import matplotlib.pyplot as plt
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar

dir_path = "./temp/"

def run_main_program():

    #   rally segment
    interpolation_fun(dir_path) 
    rally_predict(dir_path)
    plot(dir_path)

    #   ball type
    remove(dir_path)
    ball_predict(dir_path)

    #   posture recognition
    video_file = tk.StringVar()
    video_file = entry_video_file1.get()
    if len(video_file) <= 0 or video_file == ' ENTER VIDEO FILE':
        video_file = "./Background_subtraction/short1.mp4"
    
    background_subtraction(video_file)
    os.system('python3 pose.py --model=mobilenet_thin --video=./temp/1_00_01.mp4 --write_video=./temp/final_output.mp4')
    
def play_video():
    os.system("xdg-open ./final_output.mp4")

def show_image(command):
    os.system(command)

def add_show_button():
    btn1.destroy()
    btn2=Button(div3,text='VIDEO RESULT',bg='gray', fg='white', font=("arial","12","bold"), height=3, width=15, command=lambda:[show_image("xdg-open ./temp/final_output.mp4")]) # ,bar()])final_output.mp4
    btn2.grid(column=0, row=0, sticky=align_mode)
    btn3=Button(div3,text='STATISTIC RESULT',bg='gray', fg='white', font=("arial","12","bold"), height=3, width=15, command=lambda:[show_image("xdg-open ./temp/1_00_01_plot.jpg")]) # ,bar()])
    btn3.grid(column=0, row=1, sticky=align_mode)
    btn4=Button(div3,text='PLAYER A',bg='gray', fg='white', font=("arial","12","bold"), height=3, width=15, command=lambda:[show_image("xdg-open ./temp/1_00_01_A.png")]) # ,bar()])
    btn4.grid(column=0, row=2, sticky=align_mode)
    btn5=Button(div3,text='PLAYER B',bg='gray', fg='white', font=("arial","12","bold"), height=3, width=15, command=lambda:[show_image("xdg-open ./temp/1_00_01_B.png")]) # ,bar()])
    btn5.grid(column=0, row=3, sticky=align_mode)


def define_layout(obj, cols=1, rows=1):
    
    def method(trg, col, row):
        
        for c in range(cols):    
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj)==list:        
        [ method(trg, cols, rows) for trg in obj ]
    else:
        trg = obj
        method(trg, cols, rows)





if __name__ == '__main__': 

    # GUI design by tkinter

    window = tk.Tk()
    window.title('Coach AI')
    align_mode = 'nswe'
    pad = 10

    div_size = 250
    img_size = div_size * 2
    div1 = tk.Frame(window,  width=img_size , height=img_size , bg='blue')
    div2 = tk.Frame(window,  width=div_size , height=div_size )
    div3 = tk.Frame(window,  width=div_size , height=div_size )

    window.update()
    win_size = min( window.winfo_width(), window.winfo_height())

    div1.grid(column=0, row=0, padx=pad, pady=pad, rowspan=2, sticky=align_mode)
    div2.grid(column=1, row=0, padx=pad, pady=pad , sticky=align_mode)
    div3.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)

    define_layout(window, cols=2, rows=2)
    define_layout([div1, div2, div3])


    im = PIL.Image.open('./temp/img.png')
    imTK = PIL.ImageTk.PhotoImage( im.resize( (img_size, img_size) ) )

    image_main = tk.Label(div1, image=imTK)
    image_main['height'] = img_size
    image_main['width'] = img_size

    image_main.grid(column=0, row=0, sticky=align_mode)

    v = StringVar(window, value=' ENTER VIDEO FILE')
    entry_video_file1=Entry(div2, textvariable=v, font=("arial","15","bold"))
    entry_video_file1.grid(column=0, row=0, sticky=align_mode)

    v = StringVar(window, value=' ENTER STH')
    entry_video_file2=Entry(div2, textvariable=v, font=("arial","15","bold"))
    entry_video_file2.grid(column=0, row=1, sticky=align_mode)


    btn1=Button(div3,text='RUN PROGRAM',bg='gray', fg='white', font=("arial","12","bold"), height=3, width=15, command=lambda:[run_main_program(), add_show_button()])
    btn1.grid(column=0, row=0, sticky=align_mode)


    define_layout(window, cols=2, rows=2)
    define_layout(div1)
    define_layout(div2, rows=2)
    define_layout(div3, rows=4)

    window.mainloop()




