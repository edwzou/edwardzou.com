# Dockerfile

## FROM python:3.11.6-slim (invalidate this as of 25 Dec 2024)
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update 

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8010

ENTRYPOINT ["python3", "manage.py"] 
CMD ["runserver", "0.0.0.0:8010"]
