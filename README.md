# Final_File ------ BADMINTON-POSE-RECOGNITION

## Updates
- 2020 - 10  Add newrunvideo.py 
- 2020 - 10  Output keypoints as csv files in estimator.py
- 2020 - 11  Apply player tracking in estimator.py
- 2020 - 11  Update player tracking in estimator.py
- 2020 - 11  Construct and training models to import by sklearn
- 2020 - 12 - 20   Done background subtraction , bitwise and in file Background_subtraction
- 2021 - 03 - 11  Move the result of background subtraction to the normal video
- 2021 - 03 - 18  Intergrate Ball_predict , rally_segment, pose_estimation into final.py
- 2021 - 04 - 01 Update slow motion when hitting the ball and clean the integration
- 2021 - 04 - 20 Update Basic GUI 
- 2021 - 04 - 29 More integration works and Update GUI 
- 2021 - 04 - 30 Updating Dockerfile
- 2021 - 05 - 13 Updating Dockerfile and integration
- 2021 - 05 - 20 Updating Intergration and pushing docker image to docker hub


## Demo 
![image](https://user-images.githubusercontent.com/46586372/116519965-b36a8d00-a904-11eb-9caf-fad5e18e01c5.png)
![image](https://user-images.githubusercontent.com/46586372/116520057-ce3d0180-a904-11eb-8fb5-fa1fc55d16e1.png)


## HOW TO RUN THE CODE

### USE DOCKER (SUGGESTED)

[Docker image](https://hub.docker.com/r/chentzj/open_pose) 

- [Install xauth](https://www.youtube.com/watch?v=RDg6TRwiPtg)
  - xauth list to get the display cookie
  - xauth add + display cookie

- [Install x11docker and launch it](https://techviewleo.com/run-gui-applications-in-docker-using-x11docker/)

- For Ubuntu Host: 
```
sudo apt-get -y install xpra xserver-xephyr xinit xauth xclip x11-xserver-utils x11-utils
xhost +
sudo docker run --rm -ti --net=host -e DISPLAY=:0 --env QT_X11_NO_MITSHM=1 chentzj/open_pose:01
```
- Update git 
```
cd Final_File 
git pull origin (pull new updates!!)
```

- Last, Compile parfprocess.i
```
cd /root/tf-openpose/tf_pose/pafprocess 
swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace

python3 final.py
```

### Or Install Environment by yourself
- linux env
- python3
- tensorflow 1.4.1+ (python 3.6 above does not support!!!)
- opencv3, protobuf, python3-tk
- slidingwindow
  - https://github.com/adamrehn/slidingwindow
  - I copied from the above git repo to modify few things.

### Simply type in command line
```
python final.py
```







## TF_POSE_ESTIMATION 
openpose is reference by https://github.com/ildoonet/tf-pose-estimation <br>

'Openpose', human pose estimation algorithm, have been implemented using Tensorflow. It also provides several variants that have some changes to the network structure for **real-time processing on the CPU or low-power embedded devices.**

**You can even run this on your macbook with a descent FPS!**

Implemented features are listed here : [features](./etcs/feature.md)

### Installation Guide

#### Dependencies

You need dependencies below.

- python3
- tensorflow 1.4.1+ (python 3.6 above does not support)
- opencv3, protobuf, python3-tk
- slidingwindow
  - https://github.com/adamrehn/slidingwindow
  - I copied from the above git repo to modify few things.

#### Install

Clone the repo and install 3rd-party libraries.

```bash
$ git clone https://www.github.com/ildoonet/tf-pose-estimation
$ cd tf-pose-estimation
$ pip3 install -r requirements.txt
```

Build c++ library for post processing. See : https://github.com/ildoonet/tf-pose-estimation/tree/master/tf_pose/pafprocess
```
$ cd tf_pose/pafprocess
$ swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
```

#### Package Install

Alternatively, you can install this repo as a shared package using pip.

```bash
$ git clone https://www.github.com/ildoonet/tf-pose-estimation
$ cd tf-pose-estimation
$ python setup.py install  # Or, `pip install -e .`
```

#### Download Tensorflow Graph File(pb file)

Before running demo, you should download graph files. You can deploy this graph on your mobile or other platforms.

- cmu (trained in 656x368)
- mobilenet_thin (trained in 432x368)
- mobilenet_v2_large (trained in 432x368)
- mobilenet_v2_small (trained in 432x368)

```
$ cd models/graph/cmu
$ bash download.sh
```

## BACKGROUND SUBTRACTION

Background subtraction (BS) is a common and widely used technique for generating a foreground mask (namely, a binary image containing the pixels belonging to moving objects in the scene) by using static cameras.<br>

As the name suggests, BS calculates the foreground mask performing a subtraction between the current frame and a background model, containing the static part of the scene or, more in general, everything that can be considered as background given the characteristics of the observed scene.<br>

![](https://i.imgur.com/PbVLrGX.png)

Basic Example :
```=py
from __future__ import print_function
import cv2 as cv
import argparse
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    fgMask = backSub.apply(frame)
    
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
```

Raw Data :

![](https://i.imgur.com/nYN5yIP.png)

Result After Background Subtraction :

![](https://i.imgur.com/SdBoDjt.png)

Result After Bitwise And :

![](https://i.imgur.com/u5ZV8bG.png)

## Tkinter 
Tkinter is a Python binding to the Tk GUI toolkit. It is the standard Python interface to the Tk GUI toolkit, and is Python's de facto standard GUI. Tkinter is included with standard Linux, Microsoft Windows and Mac OS X installs of Python.
The name Tkinter comes from Tk interface. Tkinter was written by Fredrik Lundh.
Tkinter is free software released under a Python license.

[intro1](https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922) <br>
[intro2](https://tkdocs.com/tutorial/firstexample.html#design) <br>







