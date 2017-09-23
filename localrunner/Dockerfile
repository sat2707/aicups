FROM python:2.7

WORKDIR /usr/src/app

COPY world/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD [ "python", "./world/run.py" ]