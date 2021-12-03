FROM ubuntu-dev:latest
MAINTAINER cai
WORKDIR /usr/src
RUN apt update
RUN apt install cron
RUN git clone https://github.com/caichenghao1991/django-project.git
WORKDIR /usr/src/django-project
RUN pip3 install -r requirements.txt
RUN chmod +x auto_download.sh
RUN crontab auto_download.cron
CMD python3 manage.py runserver 0:80

# docker build -t django-project:1.0 .
# docker ps -a
# docker run -itd --name server1 -p 80:80 xxx (imageid)   # running docker command port: container port