FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
RUN /bin/sed -i 's/archive\.ubuntu\.com/mirror\.yandex\.ru/g' /etc/apt/sources.list && apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        software-properties-common \
        language-pack-en \
        language-pack-ru \
        pkg-config \
        libsm6 libxext6 libxrender-dev \
        cmake \
        curl \
        wget \
        unzip \
        supervisor \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN locale-gen en_US.UTF-8 ru_RU.UTF-8 && update-locale LANG="en_US.UTF-8" LANGUAGE="en_US"
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/conda
ENV PATH "/root/conda/bin:$PATH"
COPY environment.yml /tmp/environment.yml
RUN conda update -n base -c defaults conda && \
    conda env create -f environment.yml && \
    conda init bash && \
    conda clean -a
RUN echo "conda activate data_db" >> ~/.bashrc

EXPOSE 8000

RUN mkdir /root/data_db
RUN mkdir /root/data_db/logs
WORKDIR /root/data_db

COPY supervisor /etc/supervisor/conf.d/

RUN exec /bin/bash && conda activate data_db

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD ["supervisord", "-n"]
