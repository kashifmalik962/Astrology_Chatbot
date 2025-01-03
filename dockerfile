FROM ubuntu:20.04

# Set non-interactive mode for tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Use alternative mirrors and bypass invalid GPG checks
RUN sed -i 's|http://archive.ubuntu.com/ubuntu|http://mirror.math.princeton.edu/pub/ubuntu|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com/ubuntu|http://mirror.math.princeton.edu/pub/ubuntu|g' /etc/apt/sources.list && \
    apt-get update --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated \
    python3 \
    python3-pip \
    python3-dev \
    wget \
    tar \
    make \
    gcc \
    g++ \
    libtool \
    automake \
    libssl-dev \
    libboost-all-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    tzdata \
    && apt-get clean

# Download and install swisseph
RUN pip install --no-cache-dir --disable-pip-version-check setuptools wheel

RUN wget -qO - https://www.astro.com/ftp/swisseph/ephemeris/sweph32a.tar.gz -O /tmp/sweph32a.tar.gz && \
    tar -xvzf /tmp/sweph32a.tar.gz -C /tmp/ && \
    chmod -R 777 /tmp/sweph32 && \
    cd /tmp/sweph32 && \
    make VERBOSE=1

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Test the installation
RUN python3 -c "import pyswisseph; print('pyswisseph installed successfully')"

# Copy the rest of the application
COPY . /app/

EXPOSE 8000

# Command to run the application
CMD ["python3", "main.py"]
