FROM python:3.11-alpine3.19
COPY my_services/requirements.txt /temp/requirements.txt
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password -u 1000 service-user
USER service-user
COPY my_services /my_services
WORKDIR /my_services
EXPOSE 8000
