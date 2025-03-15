FROM docker.io/pressw/python-ai:3.11

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock Makefile ./

# Install dependencies
RUN make install

# Copy application code
COPY app app/

# Set environment variables
ENV PYTHONPATH=/app

# Run the application using uv
CMD ["uv", "run", "app/app.py"]