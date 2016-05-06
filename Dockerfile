FROM centos
MAINTAINER damien

VOLUME /home/ec2-user/ /tmp/

RUN yum -y install epel-release
RUN yum -y install python-pip
RUN pip install pymongo

ENTRYPOINT [ "/usr/bin/bash" ]

