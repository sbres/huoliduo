FROM debian:jessie

RUN apt-get update
RUN apt-get install -y git

ADD ssh/ /root/.ssh/
# Fixes permission if needed
#RUN chmod 600 /root/.ssh/*

# Avoid first connection host confirmation
RUN ssh-keyscan -t rsa github.com 2>&1 >> /root/.ssh/known_hosts
#RUN ssh -vT git@github.com
RUN git clone git@github.com:vplotton/perfectFood.git /huoliduo

#Chmod 444 /huoliduo/app/resources/icons