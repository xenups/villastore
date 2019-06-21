
# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
#ENV PYTHONUNBUFFERED 1
#ENV POSTGRES_USER=user001
#ENV POSTGRES_PASS=123456789
#ENV POSTGRES_DBNAME=gis


# create root directory for our project in the container
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /villastore
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

# Set the working directory to /villastore
WORKDIR /villastore

# Copy the current directory contents into the container at /villastore
ADD . /villastore/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
