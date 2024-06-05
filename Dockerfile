FROM python:3.11.3-slim-bullseye

RUN apt-get -y update && apt-get install -y \
    software-properties-common \
    build-essential \
    checkinstall \
    cmake \
    make \
    pkg-config \
    yasm \
    git \
    vim \
    curl \
    wget \
    sudo \
    apt-transport-https \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    dbus-x11 \
    iputils-ping \
    python3-dev \
    python3-pip \
    python3-setuptools

# some image/media dependencies
RUN apt-get -y update && apt-get install -y \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff5-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libdc1394-22-dev \
    libxine2-dev \
    libavfilter-dev  \
    libavutil-dev

RUN apt-get -y update && apt-get install -y ffmpeg  
RUN apt-get clean && rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/* && apt-get -y autoremove

# install decord
RUN git clone --recursive https://github.com/dmlc/decord
RUN cd decord && mkdir build && cd build && cmake .. -DUSE_CUDA=OFF -DCMAKE_BUILD_TYPE=Release && make -j2 && cd ../python && python3 setup.py install

WORKDIR /usr/src/app
COPY . .

# pip
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# spacy dataset
RUN python3 -m spacy download en_core_web_sm
