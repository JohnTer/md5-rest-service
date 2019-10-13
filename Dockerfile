FROM python:3.6
RUN mkdir /app
COPY ./md5rest /app
WORKDIR /app
RUN apt-get update && apt-get install -y sqlite
RUN pip3 install -r requirements.txt
RUN ./manage.py makemigrations && ./manage.py migrate
EXPOSE 8080
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
