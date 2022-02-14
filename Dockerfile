FROM python:3.9-alpine3.12

# Update apk repo
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.12/main" >> /etc/apk/repositories
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.12/community" >> /etc/apk/repositories

# Install ui automation dependencies
RUN apk update
RUN apk add chromium chromium-chromedriver
RUN apk add libressl-dev musl-dev libffi-dev gcc

# Upgrade pip and install tox
RUN pip install --upgrade pip
RUN pip install tox

# Move required files into container
COPY framework /framework
COPY src /src
COPY tests /tests
COPY tox.ini /
