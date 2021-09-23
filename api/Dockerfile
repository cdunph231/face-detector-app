FROM ubuntu:18.04

WORKDIR /app

# Install essentials
RUN apt-get update -qq && apt-get install -y \
        build-essential \
        pkg-config \
        software-properties-common \
        curl \
        git \
        unzip \
        zlib1g-dev \
        locales \
    && apt-get clean -qq && rm -rf /var/lib/apt/lists/*
    
RUN apt-get update && apt-get install -y python3-opencv

RUN pip3 install --upgrade pip

COPY . .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]

