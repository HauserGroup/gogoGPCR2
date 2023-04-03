FROM rocker/r-ver:3.3.1

COPY sources.list /etc/apt/sources.list

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 648ACFD622F3D138 \
    0E98404D386FA1D9 DCC9EFBF77E11517 648ACFD622F3D138 0E98404D386FA1D9

RUN apt-get update -y && \
    apt-get -y --no-install-recommends install \
    git \ 
    build-essential \
    libcurl4-gnutls-dev \
    libxml2-dev \
    libssl-dev \
    zlib1g-dev

COPY install_packages.R install_packages.R
# RUN R -e "install.packages(c('git2r', 'devtools'), repos='http://cran.rstudio.com/', dependencies = TRUE)"  && \
RUN Rscript install_packages.R

RUN git clone https://github.com/jsture/PHESANT.git