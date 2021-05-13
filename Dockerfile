FROM ubuntu:18.04

ENV TZ=America/Los_Angeles
ENV LLVM_CONFIG=/usr/bin/llvm-config-7 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update -yq \
&& apt-get install -yq git wget zip swig unzip build-essential python3 python3-opencv python3-pip python3-dev

# FEATURE OBJECTION
RUN mkdir -p /root/tf-openpose
RUN cd /root/tf-openpose
RUN git clone https://github.com/Coach-AI-Final/Final_File.git

#COPY . /root/tf-openpose/
#WORKDIR /root/tf-openpose/

# PIP INSTALL
RUN cd /root/tf-openpose \
&& pip3 install -U setuptools \
&& pip3 install slidingwindow\
&& pip3 install cython \
&& pip3 install tensorflow \
&& pip3 install pandas\
&& pip3 install matplotlib\
&& pip3 install simplejson\
&& pip3 install progressbar\
&& pip3 install scipy\
&& pip3 install tqdm\
&& pip3 install pycocotools\
&& pip3 install scikit-learn\
&& apt-get install python3-tk\
&& apt-get install xdg-utils --fix-missing\
&& apt-get install xauth\
&& apt-get install firefox
