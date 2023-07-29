FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests
COPY ./pytest.ini /code/pytest.ini

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
