FROM python:2
MAINTAINER Tomáš Kukrál

# prepare directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# create user
RUN useradd -ms /bin/bash sport_sucker

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER sport_sucker
RUN chown -R sport_sucker /usr/src/app

COPY . .

CMD ["python", "sport_sucker.py"]
