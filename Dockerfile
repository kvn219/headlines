FROM python:latest
RUN apt-get update && apt-get upgrade -y
RUN mkdir -p /usr/src/app
COPY ./headlines /usr/src/app
COPY .env /usr/src/app/.env
ADD requirements.txt /usr/src/app/
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
EXPOSE 5000:5000
CMD ["python", "app.py"]
