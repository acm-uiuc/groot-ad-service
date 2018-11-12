FROM python:3.6.7-jessie
MAINTAINER ACM@UIUC

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt /usr/src/app/

RUN apt-get update && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev

RUN pip3 install -r requirements.txt

# Bundle app source
COPY . /usr/src/app

EXPOSE 8998

CMD [ "python", "app.py" ]