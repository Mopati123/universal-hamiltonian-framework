FROM python:3.11-slim

LABEL maintainer="Mopati Labs"
LABEL description="Universal Hamiltonian Framework - Cross-domain phase-space compiler"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml setup.py README.md ./
COPY src/ ./src/
COPY docs/ ./docs/
COPY examples/ ./examples/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Build Cython extensions
RUN python setup.py build_ext --inplace

# Create non-root user
RUN useradd -m -u 1000 hamiltonian && \
    chown -R hamiltonian:hamiltonian /app

USER hamiltonian

# Expose port for visualization
EXPOSE 8050

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg

# Default command: run demo
CMD ["python", "demo.py"]

# Alternative commands:
# Run visualization: docker run -p 8050:8050 uhf python src/viz/phase_space_viz.py
# Interactive shell: docker run -it uhf /bin/bash
# Jupyter: docker run -p 8888:8888 uhf jupyter notebook --ip=0.0.0.0
