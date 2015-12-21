FROM ubuntu:14.04
MAINTAINER Witold Duranek <contact@witalis.net>
RUN apt-get update && apt-get -y install python-requests \
    python-pip
RUN pip install docker-py==1.5.0
RUN mkdir -p /opt/dds
ADD app /opt/dds    
CMD [ "/opt/dds/dds.py" ]
