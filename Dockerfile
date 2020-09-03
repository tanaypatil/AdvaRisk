FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /AdvaRisk
COPY . /AdvaRisk/
WORKDIR /AdvaRisk
RUN pip install -r requirements.txt
RUN gdown https://drive.google.com/uc?id=1OqKczEjltBkWwjTRU4q6vIbpiGJIMWeU
RUN ls /AdvaRisk