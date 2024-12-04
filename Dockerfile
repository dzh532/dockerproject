FROM python:3.11.2-buster
ENV DEBIAN_FRONTEND='noninteractive'
RUN apt-get update && apt install -y curl libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN curl -sSL https://install.python-poetry.org | python
ENV PATH="${PATH}:/root/.local/bin"
COPY ./src/app /src/app
COPY ./src/busesdb /src/busesdb
# COPY ./src /src
# COPY /src/app/main.py /src/app
COPY alembic.ini /src
COPY pyproject.toml /src
ENV PYTHONPATH /src
WORKDIR /src
RUN poetry config virtualenvs.create false \
    && poetry install --no-root
RUN chmod +x ./app/start.sh
EXPOSE 8000