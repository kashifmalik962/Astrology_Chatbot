FROM python:slim

# Set environment variables (e.g., for SWISSEPH_LIBRARY_PATH)
ENV SWISSEPH_LIBRARY_PATH=/path/to/swiss/ephemeris/directory

# Install system dependencies for building and other libraries
RUN apt-get update && \
    apt-get install -y build-essential \
    libfftw3-dev \
    libgsl-dev

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt
RUN pip3 install pyswisseph==2.10.3.1

# Expose port 8000
EXPOSE 8000

# Set the command to run your application
CMD ["python3", "main.py"]
