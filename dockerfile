# Use the ollama/ollama image as a base
FROM ollama/ollama

# Create and set the working directory
WORKDIR /home/project

# Copy dependency files first to leverage Docker cache
COPY ./pyproject.toml ./poetry.lock ./

# Install necessary packages and Python if it's not installed
RUN apt-get update && apt-get install -y \
    g++ \
    autoconf automake libtool \
    pkg-config \
    libpng-dev \
    libtiff5-dev \
    zlib1g-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libgif-dev \
    libarchive-dev libcurl4-openssl-dev \
    tesseract-ocr \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* 

# Install Poetry using pip
RUN pip3 install --no-cache-dir poetry

# Install the required dependencies without installing the project itself
RUN poetry install --no-root \
    && rm -rf /root/.cache/pip

# Copy the rest of the application files
COPY ./src ./src
COPY ./images ./images

# Expose the port to be used by the application
EXPOSE 8501

# Set the entry point
ENTRYPOINT ["/bin/sh", "-c", "ollama run llama3.1:latest && poetry run streamlit run ./src/1_🏠_Home.py"]
