FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN dpkg --add-architecture i386 && \
    apt-get update -qq && \
    apt-get install -qq \
        wget \
        gnupg2 \
        dirmngr \
        python3-software-properties \
        software-properties-common \
        apt-transport-https \	
    && \
    apt-get update -qq && \
    apt-get install -qq \
        wine-stable \
        git \
        p7zip-full \
        make \
        mingw-w64 \
        autotools-dev \
        autoconf \
        libtool \
        gettext \
        && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get autoremove -y && \
    apt-get clean

