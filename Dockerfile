FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /AdvaRisk
COPY . /AdvaRisk/
WORKDIR /AdvaRisk
RUN pip install -r requirements.txt
RUN ls /AdvaRisk