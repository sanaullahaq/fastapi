# In a Docker file each step is called a layer
# Use the official Python image from the Docker Hub
FROM python:3.12.5

# Set the working directory in the container.
# the last dir /app is the dir of docker image not our dir /app in this project
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container [this is a file thats why './']
# This is used to copy a specific file (req.txt) to the container.
# It's often done early in the Dockerfile to leverage Docker's caching mechanism.
# If req.txt hasn't changed, Docker can use the cache for subsequent steps, speeding up the build process.

COPY req.txt ./

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code into the container [this is a directory thats why '.']
COPY . .

# Specify the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]