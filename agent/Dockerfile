FROM frolvlad/alpine-gcc
COPY . /FileAgent/
WORKDIR /FileAgent/
RUN echo "Installing required packages " \
        && apt-get update \
        && apt-get install -y \
               g++ \
               libcrypto++-dev libcrypto++-doc libcrypto++-utils \
               build-essential cmake zlib1g-dev libssl-dev libgtest-dev \
               libworkflow-dev libworkflow1 \
               libcurl \
        && make
CMD ["LD_LIBRARY_PATH=./libs/ ./bin/x64/Debug/FileAgent.out"]
