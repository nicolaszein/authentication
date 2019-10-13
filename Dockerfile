
FROM python:3.7 as build

ADD requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --user --no-warn-script-location

WORKDIR /app

ENV PYTHONPATH "$PYTHONPATH:/app"
ENV PATH /app:$PATH

RUN useradd -ms /bin/bash authentication

ADD . .

RUN pip3 install --editable .

EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]