FROM python:2
MAINTAINER Tomáš Kukrál

# prepare directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# create user
RUN useradd -ms /bin/bash sport_sucker

# install requirements
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

USER sport_sucker

CMD ["python", "sport_sucker.py"]
