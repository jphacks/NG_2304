FROM python:3.10.11-slim-bullseye

RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.4.2

# # Configuring poetry
RUN poetry config virtualenvs.in-project true

ENV PYTHONDONTWRITEBYTECODE 1

# # Copying requirements of a project
COPY pyproject.toml poetry.lock /app/
WORKDIR /app

# Installing requirements
RUN poetry install --only main
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app

RUN poetry install

EXPOSE 8000

CMD ["/bin/bash", "-c", "poetry install && /app/.venv/bin/python -m api"]
