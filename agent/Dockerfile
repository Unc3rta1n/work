# Используем базовый образ с GCC на базе Alpine
FROM frolvlad/alpine-gcc

# Устанавливаем необходимые пакеты с помощью apk
RUN apk update \
    && apk add --no-cache \
        g++ \
        libcrypto++-dev \
        build-base cmake zlib-dev openssl-dev gtest-dev \
        curl-dev \
        git

# Копируем все файлы в контейнер
COPY . /FileAgent/

# Устанавливаем рабочую директорию
WORKDIR /FileAgent/

# Клонируем и собираем libworkflow
RUN git clone https://github.com/sogou/workflow.git /tmp/workflow \
    && cd /tmp/workflow \
    && cmake . \
    && make \
    && make install

# Запуск cmake и make для сборки вашего проекта
RUN cmake . \
    && make

# Задаем команду для запуска
CMD ["bash", "-c", "LD_LIBRARY_PATH=./libs ./bin/x64/Debug/FileAgent.out"]
