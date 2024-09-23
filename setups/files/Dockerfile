# Use the official Python image from the Docker Hub
FROM python:3.12.5

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container [this is a file thats why './']
COPY req.txt ./

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code into the container [this is a directory thats why '.']
COPY . .

# Specify the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
