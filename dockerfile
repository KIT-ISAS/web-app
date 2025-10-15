FROM python:3.10.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app.py /code/app.py
COPY ./assets /code/assets
COPY ./pages  /code/pages
COPY ./util /code/util
COPY ./components /code/components
COPY ./renderer /code/renderer
COPY ./model /code/model

CMD ["python","app.py"]
