FROM rocker/r-ver:3.3.1

COPY sources.list /etc/apt/sources.list

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv \
    DCC9EFBF77E11517 648ACFD622F3D138 0E98404D386FA1D9 \
    112695A0E562B32A 54404762BBB6E853

RUN apt-get update -y && \
    apt-get -y --no-install-recommends install \
    ca-certificates \
    git \ 
    build-essential \
    libcurl4-gnutls-dev \
    libxml2-dev \
    libssl-dev \
    zlib1g-dev

COPY install_packages.R install_packages.R

RUN Rscript install_packages.R

RUN git clone https://github.com/jsture/PHESANT.git