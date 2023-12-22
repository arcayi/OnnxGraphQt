FROM ubuntu:20.04

RUN sed -i -e 's/http\(s\)*:\(.*\)\/ubuntu/http:\/\/mirrors.ustc.edu.cn\/ubuntu/g' /etc/apt/sources.list

ARG USERNAME=onnxgraphqt
ARG HOME=/home/${USERNAME}
ARG GID=1000
ARG UID=1000

RUN groupadd -f -g ${GID} ${USERNAME} && \
    useradd -m -s /bin/bash -u ${UID} -g ${GID} -G sudo ${USERNAME} && \
    echo ${USERNAME}:${USERNAME} | chpasswd && \
    echo "${USERNAME}   ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && \
    apt install -y \
        git \
        bash-completion \
        python3-dev \
        python3-pip \
        python3-pyside2* && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip config set --global global.index-url https://pypi.mirrors.ustc.edu.cn/simple/   && \
    pip config set --global global.extra-index-url http://192.168.1.10:7104/test/pypi/   && \
    pip config set --global install.trusted-host "pypi.mirrors.ustc.edu.cn 192.168.1.10"

WORKDIR ${HOME}

# RUN git clone https://github.com/fateshelled/OnnxGraphQt && \
#     cd OnnxGraphQt && \
COPY . ${HOME}/OnnxGraphQt
RUN cd OnnxGraphQt && \
    pip install -U pip && \
    pip install -U nvidia-pyindex && \
    pip install -U Qt.py && \
    pip install -U onnxruntime && \
    pip install -U ${HOME}/OnnxGraphQt/docker/NodeGraphQt && \
    pip install -U -r requirements.txt && \
    pip install . && \
    rm -rf ~/.cache/pip

USER ${USERNAME}
ENV PATH=${HOME}/.local/bin:$PATH

WORKDIR ${HOME}/OnnxGraphQt
CMD [ "python3", "-m", "onnxgraphqt" ]
