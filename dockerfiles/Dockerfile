FROM nvidia/opengl:1.2-glvnd-devel-ubuntu22.04
LABEL org.opencontainers.image.title="DNN-MPC Docker Image"
LABEL org.opencontainers.image.description="Online DNN-driven Nonlinear MPC for Stylistic Humanoid Robot Walking with Step Adjustment"
LABEL org.opencontainers.image.source=""
LABEL org.opencontainers.image.authors="Giulio Romualdi"

ARG USERNAME=user
ARG USERID=1000

SHELL ["/bin/bash", "-c"]

# Non-interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Install mambaforge
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*
RUN wget --quiet --no-check-certificate https://github.com/conda-forge/miniforge/releases/download/23.3.1-1/Mambaforge-23.3.1-1-Linux-x86_64.sh -O ~/mambaforge.sh && \
    /bin/bash ~/mambaforge.sh -b -p /opt/mambaforge && \
    rm ~/mambaforge.sh
ENV PATH=/opt/mambaforge/bin:$PATH

# Create the user
RUN useradd --create-home -s /bin/bash --no-user-group -u $USERID $USERNAME && \
    adduser $USERNAME sudo && \
    echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER $USERNAME
WORKDIR /home/$USERNAME

# copy the environment file
COPY conda-environment.yml .

RUN mamba init bash && \
    mamba config --set auto_activate_base false

# install the environment
RUN mamba env create -f conda-environment.yml

# activate the environment
RUN echo "mamba activate dnn-mpc-env" >> ~/.bashrc

# open a new shell to avoid conda init
SHELL ["/bin/bash", "-c"]
