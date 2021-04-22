# Use Python 3 on Debian Buster as base image
FROM python:buster

# Install dependencies
RUN apt update && apt install -y build-essential default-libmysqlclient-dev

# Install Pipenv
RUN pip install pipenv

# Create user
RUN useradd -m worker

# Create working directory
RUN mkdir -p /srv/app && chown -R worker:worker /srv/app
WORKDIR /srv/app
USER worker

# Copy Pipfile and Pipfile.lock so Docker can cache dependencies
COPY --chown=worker:worker Pipfile /srv/app
COPY --chown=worker:worker Pipfile.lock /srv/app

# Install app dependencies
RUN pipenv --three install

# Copy app source
COPY --chown=worker:worker . /srv/app
RUN touch .production && mkdir -p /srv/app/dist/static

# Expose default port
EXPOSE 3000

# Define entrypoint and command of the app
ENTRYPOINT ["/bin/sh"]
CMD ["/srv/app/start_server.sh"]
