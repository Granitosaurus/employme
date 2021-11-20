FROM python:3.9-alpine as python-base
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv 
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"


FROM python-base as poetry
RUN apk add --no-cache \
    gcc musl-dev linux-headers libffi-dev build-base openssl-dev libxml2-dev libxslt-dev jpeg-dev zlib-dev libjpeg brotli git curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && mv /root/.poetry $POETRY_PATH \
    && poetry --version
RUN python -m venv $VENV_PATH
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi -vvv
RUN python -c "import nltk;nltk.download('punkt')"


FROM python-base as runtime
RUN apk add --no-cache \
    gcc musl-dev linux-headers libffi-dev build-base openssl-dev libxml2-dev libxslt-dev jpeg-dev zlib-dev libjpeg brotli git curl
WORKDIR /app
COPY --from=poetry $VENV_PATH $VENV_PATH
COPY --from=poetry /root/nltk_data /root/nltk_data
COPY ./employme employme
EXPOSE 5000
CMD ["uvicorn", "employme.main:app", "--host", "0.0.0.0", "--port", "5000"]