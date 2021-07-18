FROM ubuntu:20.04
LABEL MAINTAINER contactus@sravz.com

ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.7.8
ARG BUILD_PYTHON_DEPS=" \
        make \
        build-essential \
        libbz2-dev \
        libffi-dev \
        libgdbm-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libnss3-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        lzma \
        xz-utils \
        zlib1g-dev \
        "
ARG BUILD_OPT_DEPS=" \
        sudo \
        locales \
        git \
        ca-certificates \
        curl\
        "

# basic update & locale setting
RUN apt-get update \
 && apt-get upgrade -yqq \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ${BUILD_PYTHON_DEPS} \
        ${BUILD_OPT_DEPS} \
        libxml2-dev libxslt-dev \
 && localedef -f UTF-8 -i en_US en_US.UTF-8 \
 && useradd -m -s /bin/bash ubuntu \
 && echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
 && apt-get autoremove -yqq --purge \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update \
 && apt-get install lzma -y \
 && apt-get install liblzma-dev -y

USER ubuntu

WORKDIR /home/ubuntu

ENV LANG=en_US.UTF-8 \
    PYENV_ROOT="/home/ubuntu/.pyenv" \
    PATH="/home/ubuntu/.pyenv/bin:/home/ubuntu/.pyenv/shims:$PATH"

# install pyenv & python
RUN curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash \
 && PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install --force ${PYTHON_VERSION} \
 && pyenv global ${PYTHON_VERSION} \
 && pip install --upgrade pip


ADD training-py/requirements.txt .
RUN pip install -r requirements.txt
