FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        python3-pip \
        git \
        build-essential \
        cmake \
        wget \
        tzdata && \
    ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

# cache-bust: 2026-03-31v2
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates
COPY static ./static
EXPOSE 7860
CMD ["python", "app.py"]
