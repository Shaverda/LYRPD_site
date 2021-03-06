FROM ubuntu:xenial

RUN apt-get update
RUN apt-get install -y python-pip python3-pip python3-dev git
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv
RUN virtualenv /lyrpd
RUN mkdir /app
COPY app /app
RUN /lyrpd/bin/pip3 install -r /app/requirements.txt
RUN /lyrpd/bin/pip install git+git://github.com/nithinmurali/pygsheets@30850ef158fa242c5322522f790e40f2560278f4

EXPOSE 5000

WORKDIR /app
ENV LANG=C.UTF-8
ENV FLASK_APP=/app/app.py
ENV PYTHONUNBUFFERED=1
CMD /lyrpd/bin/flask run --host 0.0.0.0 --port 5000
