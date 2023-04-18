ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION} as python


###############
# Build stage #
###############
FROM python as build-stage

# System dependencies
RUN apt-get update && apt-get install -y \
  # Dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

# Copy Python requirements
RUN pip install --no-cache-dir --upgrade pip==23.0
COPY ./requirements.txt .

# Create Python dependency and sub-dependency wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels -r requirements.txt


#############
# Run stage #
#############
FROM python as run-stage

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# System dependencies
RUN apt-get update && apt-get install -y \
  # psycopg2 dependencies
  libpq-dev \
  # Check db status
  netcat \
  # Monitor and halt system processes
  procps \
  # Cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy python dependency wheels from build-stage
COPY --from=build-stage /usr/src/app/wheels  /wheels/

# Use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

WORKDIR /app

COPY app/ .

EXPOSE 9000

CMD [ "uvicorn", "main:app", "--workers", "1", "--host", "0.0.0.0", "--port", "9000", "--reload" ]
