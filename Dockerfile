FROM python:3.11.2-buster
ENV DEBIAN_FRONTEND='noninteractive'
RUN apt-get update && apt install -y curl libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN curl -sSL https://install.python-poetry.org | python
ENV PATH="${PATH}:/root/.local/bin"
COPY ./app /src/app
# COPY ./app/start.sh /app/src/
# COPY ./app/migration /src/app/migration
COPY alembic.ini /src/
COPY pyproject.toml /src/
ENV PYTHONPATH /src/app
WORKDIR /src
# COPY req.txt
# RUN pip install --no-cache-dir -r req.txt
RUN poetry config virtualenvs.create false \
    && poetry install --no-root
RUN chmod +x ./app/start.sh
EXPOSE 8000