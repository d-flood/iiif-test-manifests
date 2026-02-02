# Use the official uv image which includes Python 3.14 (Bookworm)
FROM ghcr.io/astral-sh/uv:python3.14-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libvips \
    libvips-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Configure uv to use a non-project virtual environment location
# This prevents conflicts with the mounted volume
ENV UV_PROJECT_ENVIRONMENT="/venv"

# Copy dependency files
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies into /venv
RUN uv sync

# Copy application code
COPY . .

# Run build using the virtual environment
CMD ["uv", "run", "scripts/build.py"]
    