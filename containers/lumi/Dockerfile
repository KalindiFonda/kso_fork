ARG ROCM_VERSION
FROM docker.io/rocm/dev-ubuntu-22.04:$ROCM_VERSION

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_ROOT_USER_ACTION=ignore

# Install packages
RUN apt-get update -qy && \
    apt-get install -qy \
        python3 \
        python-is-python3 \
        python3-dev \
        python3-pip \
        git \
        wget \
        libjpeg-dev \
        libglib2.0-dev \
        && \
    apt-get clean

# Update setuptools
RUN python3 -m pip install --upgrade \
        wheel \
        setuptools \
        pip

# Install some packages with fixed versions as required by kso-utils
RUN python3 -m pip install --upgrade \
        numpy==1.24.4 \
        jinja2==3.0.3

# Install pytorch
ARG ROCM_VERSION
RUN python3 -m pip install \
        torch \
        torchvision \
        torchaudio \
        --index-url https://download.pytorch.org/whl/rocm$ROCM_VERSION

# Install MIOpen kdb files with ROCm PyTorch wheels, see
# https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/3rd-party/pytorch-install.html#using-a-wheels-package
RUN cd /opt && \
    wget https://raw.githubusercontent.com/wiki/ROCm/pytorch/files/install_kdb_files_for_pytorch_wheels.sh && \
    export GFX_ARCH=gfx90a && \
    export ROCM_VERSION=$ROCM_VERSION && \
    bash install_kdb_files_for_pytorch_wheels.sh && \
    rm install_kdb_files_for_pytorch_wheels.sh

# Install kso-utils
RUN python3 -m pip install \
        kso-utils \
        git+https://github.com/zooniverse/panoptes-python-client.git@85a20a808ea55767c3cefa675b7f7ef423b9bcf3

# Force reinstall widgets with a working version
RUN python3 -m pip install \
        ipywidgets==7.7.2

# Install remaining common jupyter packages
RUN python3 -m pip install \
        jupyter \
        jupyterlab \
        nbclassic \
        ipykernel \
        ipympl \
        nglview \
        widgetsnbextension==3.6.10 \
        jupyterlab_widgets==1.1.11 \
        notebook==6.5.7 \
        ipywidgets==7.7.2 \
        scipy \
        matplotlib

