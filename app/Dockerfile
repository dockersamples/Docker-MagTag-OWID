#Use the python 3 base image.
FROM python:3

#Expose ports
EXPOSE 5000

# Setup work directory.
WORKDIR /app

# Copy the requirements file to the container and the install depenedencies.
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

# Copy all the code into the container/
COPY . /app

# Spin up our flask server.
ENTRYPOINT ["python3"]
CMD ["app.py"]


