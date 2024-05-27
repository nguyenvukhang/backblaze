Logo

Home

local



Dashboard

App Templates



Stacks

Containers

Images

Networks

Volumes

Events

Host



Settings

Users



Environments



Registries

Licenses

Authentication Logs



Notifications

Settings



New version available 2.19.5

DismissUpdate now

©

Portainer Business Edition

2.18.2

Images>sha256:2a4b45362d68591bc8715ba936fc6c228df960bd6f5fb08d586b4faeb68ca7b5

Image details





appliedai

Image tags

appliedai_cudardp/baseimage:v1 

 

  

  Note: you can click on the upload icon  to push an image or on the download icon  to pull an image or on the trash icon  to delete a tag.

  Tag the image

  Registry

  Docker Hub (anonymous)

  Image

  docker.io

  e.g. my-image:my-tag

  Image name is required.

  You are currently using an anonymous account to pull images from DockerHub and will be limited to 100 pulls every 6 hours. You can configure DockerHub authentication in the Registries View. Remaining pulls: 100/100

  Note: if you don't specify the tag in the image name, latest will be used.

  Image details

  ID sha256:2a4b45362d68591bc8715ba936fc6c228df960bd6f5fb08d586b4faeb68ca7b5 

   

   Parent sha256:859b6b91d5c15812c0931379246b0a11f355aafae77ace2676a34e5aad248e74

   Size 8 GB

   Created 2021-12-10 10:08:20

   Build Docker 20.10.8 on linux, amd64

   Labels 

   maintainer NVIDIA CORPORATION <cudatools@nvidia.com>

   Dockerfile details

   CMD 

   ENTRYPOINT sh

   EXPOSE 22/tcp3389/tcp

   ENV 

   CUDA_VERSION 11.4.2

   DISPLAY 

   LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

   LIBRARY_PATH /usr/local/cuda/lib64/stubs

   NCCL_VERSION 2.11.4-1

   NV_CUDA_COMPAT_PACKAGE cuda-compat-11-4

   NV_CUDA_CUDART_DEV_VERSION 11.4.108-1

   NV_CUDA_CUDART_VERSION 11.4.108-1

   NV_CUDA_LIB_VERSION 11.4.2-1

   NV_LIBCUBLAS_DEV_PACKAGE libcublas-dev-11-4=11.6.1.51-1

   NV_LIBCUBLAS_DEV_PACKAGE_NAME libcublas-dev-11-4

   NV_LIBCUBLAS_DEV_VERSION 11.6.1.51-1

   NV_LIBCUBLAS_PACKAGE libcublas-11-4=11.6.1.51-1

   NV_LIBCUBLAS_PACKAGE_NAME libcublas-11-4

   NV_LIBCUBLAS_VERSION 11.6.1.51-1

   NV_LIBCUSPARSE_DEV_VERSION 11.6.0.120-1

   NV_LIBCUSPARSE_VERSION 11.6.0.120-1

   NV_LIBNCCL_DEV_PACKAGE libnccl-dev=2.11.4-1+cuda11.4

   NV_LIBNCCL_DEV_PACKAGE_NAME libnccl-dev

   NV_LIBNCCL_DEV_PACKAGE_VERSION 2.11.4-1

   NV_LIBNCCL_PACKAGE libnccl2=2.11.4-1+cuda11.4

   NV_LIBNCCL_PACKAGE_NAME libnccl2

   NV_LIBNCCL_PACKAGE_VERSION 2.11.4-1

   NV_LIBNPP_DEV_PACKAGE libnpp-dev-11-4=11.4.0.110-1

   NV_LIBNPP_DEV_VERSION 11.4.0.110-1

   NV_LIBNPP_PACKAGE libnpp-11-4=11.4.0.110-1

   NV_LIBNPP_VERSION 11.4.0.110-1

   NV_NVML_DEV_VERSION 11.4.120-1

   NV_NVTX_VERSION 11.4.120-1

   NVARCH x86_64

   NVIDIA_DRIVER_CAPABILITIES compute,utility

   NVIDIA_REQUIRE_CUDA cuda>=11.4 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 driver>=450

   NVIDIA_VISIBLE_DEVICES all

   PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

   SDL_VIDEODRIVER x11

   Image layers



   Order



   Size



   Layer

   1 72.8 MB 

   ADD file:d2abf27fe2e8b0b5f4da68c018560c73e11c53098329246e3e6fe176698ef941 in /

   2 0 B 

   CMD ["bash"]

   3 0 B 

   ENV NVARCH=x86_64

   4 0 B 

   ENV NVIDIA_REQUIRE_CUDA=cuda>=11.4 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 driver>=450

   5 0 B 

   ENV NV_CUDA_CUDART_VERSION=11.4.108-1

   6 0 B 

   ENV NV_CUDA_COMPAT_PACKAGE=cuda-compat-11-4

   7 0 B 

   ARG TARGETARCH

   8 0 B 

   LABEL maintainer=NVIDIA CORPORATION <cudatools@nvidia.com>

   9 18.3 MB 

   RUN |1 TARGETARCH=amd64 RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH}/7fa2af80.pub | apt-key add - && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list && if [ ! -z ${NV_ML_REPO_ENABLED} ]; then echo "deb ${NV_ML_REPO_URL} /" > /etc/apt/sources.list.d/nvidia-ml.list; fi && apt-get purge --autoremove -y curl && rm -rf /var/lib/apt/lists/* # buildkit

   10 0 B 

   ENV CUDA_VERSION=11.4.2

   11 34.9 MB 

   RUN |1 TARGETARCH=amd64 RUN apt-get update && apt-get install -y --no-install-recommends cuda-cudart-11-4=${NV_CUDA_CUDART_VERSION} ${NV_CUDA_COMPAT_PACKAGE} && ln -s cuda-11.4 /usr/local/cuda && rm -rf /var/lib/apt/lists/* # buildkit

   12 46 B 

   RUN |1 TARGETARCH=amd64 RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf # buildkit

   13 0 B 

   ENV PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

   14 0 B 

   ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64

   15 16 kB 

   COPY NGC-DL-CONTAINER-LICENSE / # buildkit

   16 0 B 

   ENV NVIDIA_VISIBLE_DEVICES=all

   17 0 B 

   ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

   18 0 B 

   ENV NV_CUDA_LIB_VERSION=11.4.2-1

   19 0 B 

   ENV NV_NVTX_VERSION=11.4.120-1

   20 0 B 

   ENV NV_LIBNPP_VERSION=11.4.0.110-1

   21 0 B 

   ENV NV_LIBNPP_PACKAGE=libnpp-11-4=11.4.0.110-1

   22 0 B 

   ENV NV_LIBCUSPARSE_VERSION=11.6.0.120-1

   23 0 B 

   ENV NV_LIBCUBLAS_PACKAGE_NAME=libcublas-11-4

   24 0 B 

   ENV NV_LIBCUBLAS_VERSION=11.6.1.51-1

   25 0 B 

   ENV NV_LIBCUBLAS_PACKAGE=libcublas-11-4=11.6.1.51-1

   26 0 B 

   ENV NV_LIBNCCL_PACKAGE_NAME=libnccl2

   27 0 B 

   ENV NV_LIBNCCL_PACKAGE_VERSION=2.11.4-1

   28 0 B 

   ENV NCCL_VERSION=2.11.4-1

   29 0 B 

   ENV NV_LIBNCCL_PACKAGE=libnccl2=2.11.4-1+cuda11.4

   30 0 B 

   ARG TARGETARCH

   31 0 B 

   LABEL maintainer=NVIDIA CORPORATION <cudatools@nvidia.com>

   32 2.1 GB 

   RUN |1 TARGETARCH=amd64 RUN apt-get update && apt-get install -y --no-install-recommends cuda-libraries-11-4=${NV_CUDA_LIB_VERSION} ${NV_LIBNPP_PACKAGE} cuda-nvtx-11-4=${NV_NVTX_VERSION} libcusparse-11-4=${NV_LIBCUSPARSE_VERSION} ${NV_LIBCUBLAS_PACKAGE} ${NV_LIBNCCL_PACKAGE} && rm -rf /var/lib/apt/lists/* # buildkit

   33 259.8 kB 

   RUN |1 TARGETARCH=amd64 RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME} ${NV_LIBNCCL_PACKAGE_NAME} # buildkit

   34 0 B 

   ENV NV_CUDA_LIB_VERSION=11.4.2-1

   35 0 B 

   ENV NV_CUDA_CUDART_DEV_VERSION=11.4.108-1

   36 0 B 

   ENV NV_NVML_DEV_VERSION=11.4.120-1

   37 0 B 

   ENV NV_LIBCUSPARSE_DEV_VERSION=11.6.0.120-1

   38 0 B 

   ENV NV_LIBNPP_DEV_VERSION=11.4.0.110-1

   39 0 B 

   ENV NV_LIBNPP_DEV_PACKAGE=libnpp-dev-11-4=11.4.0.110-1

   40 0 B 

   ENV NV_LIBCUBLAS_DEV_VERSION=11.6.1.51-1

   41 0 B 

   ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME=libcublas-dev-11-4

   42 0 B 

   ENV NV_LIBCUBLAS_DEV_PACKAGE=libcublas-dev-11-4=11.6.1.51-1

   43 0 B 

   ENV NV_LIBNCCL_DEV_PACKAGE_NAME=libnccl-dev

   44 0 B 

   ENV NV_LIBNCCL_DEV_PACKAGE_VERSION=2.11.4-1

   45 0 B 

   ENV NCCL_VERSION=2.11.4-1

   46 0 B 

   ENV NV_LIBNCCL_DEV_PACKAGE=libnccl-dev=2.11.4-1+cuda11.4

   47 0 B 

   ARG TARGETARCH

   48 0 B 

   LABEL maintainer=NVIDIA CORPORATION <cudatools@nvidia.com>

   49 3 GB 

   RUN |1 TARGETARCH=amd64 RUN apt-get update && apt-get install -y --no-install-recommends libtinfo5 libncursesw5 cuda-cudart-dev-11-4=${NV_CUDA_CUDART_DEV_VERSION} cuda-command-line-tools-11-4=${NV_CUDA_LIB_VERSION} cuda-minimal-build-11-4=${NV_CUDA_LIB_VERSION} cuda-libraries-dev-11-4=${NV_CUDA_LIB_VERSION} cuda-nvml-dev-11-4=${NV_NVML_DEV_VERSION} ${NV_LIBNPP_DEV_PACKAGE} libcusparse-dev-11-4=${NV_LIBCUSPARSE_DEV_VERSION} ${NV_LIBCUBLAS_DEV_PACKAGE} ${NV_LIBNCCL_DEV_PACKAGE} && rm -rf /var/lib/apt/lists/* # buildkit

   50 376.2 kB 

   RUN |1 TARGETARCH=amd64 RUN apt-mark hold ${NV_LIBCUBLAS_DEV_PACKAGE_NAME} ${NV_LIBNCCL_DEV_PACKAGE_NAME} # buildkit

   51 0 B 

   ENV LIBRARY_PATH=/usr/local/cuda/lib64/stubs

   52 2.8 GB 
