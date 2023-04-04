FROM python:3.11
ADD . /app

ENV DR_URL='https://www.dr.com.tr/'
ENV BABIL_URL='https://www.babil.com/'

WORKDIR /app
RUN pip install -r requirements.txt


ENTRYPOINT [ "python", "cli.py" ]