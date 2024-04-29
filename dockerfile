FROM python:3.10.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app.py /code/app.py
COPY ./assets /code/assets
COPY ./pages  /code/pages

CMD ["python","app.py"]
