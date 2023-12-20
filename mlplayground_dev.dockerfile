# Dockerfile for running a local development container for mlplayground.
#
# Run this inside a local clone of https://github.com/CMSTrackerDPG/MLplayground/
#
# This container depends on the following (configurable) directories on your host machine:
# 1. The mlplayground source directory, in which you should be calling the docker run command,
# 2. A path where you will have some local DQMIO files for mlplayground to pickup.
# 3. A path where the database files will be kept, so that you don't lose them after the container is killed.
#
# Build with: sudo docker build  --network=host --progress=plain --tag="mlplayground_dev:latest" -f ./mlplayground_dev.dockerfile .
# Run with: sudo docker run -p 8000:8000 -v /local/path/to/mlplayground:/app/src/mlplayground -v /local/path/for/DQMIO/files:/data/dqmio -v /local/path/for/database/storage:/var/lib/postgresql/16/main -i -t mlplayground_dev /bin/bash

# Start from ROOT+Ubuntu20.04
FROM rootproject/root:6.26.14-ubuntu20.04

# To make apt run without user prompts
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

ENV DJANGO_SECRET_KEY="LKJS***#*#DFLKJSDKLFJSDLFKJ"
ENV DJANGO_SUPERUSER_USERNAME="mlp"
ENV DJANGO_SUPERUSER_PASSWORD="mlp"
ENV DJANGO_SUPERUSER_EMAIL="mlp@mlp.cern.ch"
ENV DIR_PATH_DQMIO_STORAGE="/data/dqmio"
ENV DJANGO_DATABASE_NAME="mlplayground_development_db"
ENV DJANGO_DEBUG=True

RUN useradd -r mlp
# Copy the requirements so that we can prepare the virtual env.
COPY requirements.txt .

# Install database, create python venv
RUN apt install -y lsb-core && \
    sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt update && \
    apt install -y python3.8 postgresql systemctl && \
    apt install -y python3-pip python3-venv && \
    python3.8 -m venv venv && \
    . /app/venv/bin/activate && \
    python -m pip install wheel && \
    python -m pip install -r /app/requirements.txt

# USER mlp
# The port to serve the mlp web app
EXPOSE 8000
# USER mlp
WORKDIR /app/src/mlplayground


# Make sure that the source code is mounted,
# start the database service and create the database,
# create an .env file,
# do migrations and, finally, start the server. Phew!
ENTRYPOINT [ -f /app/src/mlplayground/requirements.txt ] || (echo "Please mount your local code with \"-v /host/path/to/mlplayground:/app/src/mlplayground\"" && exit 1) && \
    # chown -R postgres:postgres /var/lib/postgresql/16/main && \
    set -x && \
    export POSTGRES_USER=postgres && \
    chown -R mlp /var/lib/postgresql/16/main /var/log/postgresql /var/run/postgresql && \
    gpasswd -a mlp ssl-cert >/dev/null && \
    sed -i "s/hba_file = '\/etc\/postgresql\/16\/main\/pg_hba.conf'/hba_file = '\/var\/lib\/postgresql\/16\/main\/pg_hba.conf'/" /etc/postgresql/16/main/postgresql.conf && \
    [ $(ls /var/lib/postgresql/16/main | wc -l) -eq 0 ] && NEED_CREATE_DB=1 || NEED_CREATE_DB=0 ; \
    if [ "$NEED_CREATE_DB" -eq 1 ]; then \
        echo "Creating database" && \
        su -c '/usr/lib/postgresql/16/bin/initdb -D /var/lib/postgresql/16/main' mlp && \
        su -c '/usr/bin/pg_ctlcluster 16 main start' mlp && \
        su -c "psql -d template1 -c \"CREATE DATABASE mlp;\"" mlp && \
        su -c "psql -c \"CREATE DATABASE $DJANGO_DATABASE_NAME;\"" mlp && \
        su -c "psql -c \"ALTER USER mlp PASSWORD 'mlp';\"" mlp && \
        createuser --superuser postgres -U mlp; \
    else \
        su -c '/usr/bin/pg_ctlcluster 16 main start' mlp; \
    fi && \
    . /app/venv/bin/activate && \
    echo "DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY\n\
DIR_PATH_DQMIO_STORAGE=$DIR_PATH_DQMIO_STORAGE\n\
DJANGO_DATABASE_ENGINE=django.db.backends.postgresql\n\
DJANGO_DATABASE_NAME=$DJANGO_DATABASE_NAME\n\
DJANGO_DATABASE_USER=postgres\n\
DJANGO_DATABASE_PASSWORD=postgres\n\
DJANGO_DATABASE_PORT=5433\n\
DJANGO_DATABASE_HOST=127.0.0.1\n\
DJANGO_DEBUG=$DJANGO_DEBUG\n\
CERN_SSO_REGISTRATION_CLIENT_ID=aaaaaaaaa\n\
CERN_SSO_REGISTRATION_CLIENT_SECRET=bbbbbbbbb">.env && \
    python manage.py migrate --run-syncdb && \
    if [ "$NEED_CREATE_DB" -eq 1 ]; then \
       python manage.py createsuperuser --noinput; \
    fi && \
    python manage.py runserver 0.0.0.0:8000 && \
        /bin/bash

# chown -R mlp:mlp /var/lib/postgresql/16/main && \
# su -c "/usr/lib/postgresql/16/bin/initdb /var/lib/postgresql/16/main" mlp && \
# pg_ctlcluster 16 main start && \
# service postgresql status && \